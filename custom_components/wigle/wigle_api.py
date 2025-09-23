"""Wigle API client with enhanced error handling and retry logic."""
from __future__ import annotations

import asyncio
import aiohttp
import base64
import logging
from typing import Any, Dict

from .const import WIGLE_API_BASE, WIGLE_USER_STATS_ENDPOINT, WIGLE_PROFILE_ENDPOINT

_LOGGER = logging.getLogger(__name__)


class WigleAPIError(Exception):
    """Base exception for Wigle API errors."""
    pass


class WigleAuthError(WigleAPIError):
    """Exception for authentication errors."""
    pass


class WigleRateLimitError(WigleAPIError):
    """Exception for rate limit errors."""
    pass


class WigleAPI:
    """Wigle API client with enhanced error handling."""
    
    def __init__(self, username: str, api_name: str, api_token: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.username = username
        self.api_name = api_name
        self.api_token = api_token
        self.session = session
        self._auth_header = self._create_auth_header(api_name, api_token)
        self._last_request_time = 0
        self._request_count = 0
        self._max_requests_per_hour = 100  # Wigle API limit
    
    def _create_auth_header(self, api_name: str, api_token: str) -> str:
        """Create basic auth header using API Name and API Token."""
        credentials = f"{api_name}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    async def _rate_limit_check(self) -> None:
        """Check and enforce rate limiting."""
        import time
        current_time = time.time()
        
        # Reset counter every hour
        if current_time - self._last_request_time > 3600:
            self._request_count = 0
            self._last_request_time = current_time
        
        if self._request_count >= self._max_requests_per_hour:
            wait_time = 3600 - (current_time - self._last_request_time)
            _LOGGER.warning(f"Rate limit reached, waiting {wait_time:.0f} seconds")
            raise WigleRateLimitError(f"Rate limit exceeded, retry in {wait_time:.0f} seconds")
        
        self._request_count += 1
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an authenticated request to the Wigle API."""
        await self._rate_limit_check()
        
        url = f"{WIGLE_API_BASE}{endpoint}"
        headers = {
            "Accept": "application/json",
            "Authorization": self._auth_header,
            "User-Agent": f"HomeAssistant-Wigle/{self.username}",
        }
        
        _LOGGER.debug(f"Making request to {url} with params: {params}")
        
        try:
            async with self.session.get(url, headers=headers, params=params, timeout=30) as response:
                response_text = await response.text()
                
                if response.status == 401:
                    raise WigleAuthError("Invalid API credentials")
                elif response.status == 429:
                    raise WigleRateLimitError("Rate limit exceeded")
                elif response.status == 200:
                    try:
                        data = await response.json()
                        if data.get("success"):
                            return data
                        else:
                            error_msg = data.get("message", "API returned success=false")
                            _LOGGER.error(f"API error: {error_msg}")
                            raise WigleAPIError(f"API error: {error_msg}")
                    except ValueError as e:
                        _LOGGER.error(f"Invalid JSON response: {response_text}")
                        raise WigleAPIError(f"Invalid JSON response: {e}")
                else:
                    _LOGGER.error(f"HTTP {response.status}: {response_text}")
                    raise WigleAPIError(f"HTTP {response.status}: {response_text}")
                    
        except asyncio.TimeoutError:
            raise WigleAPIError("Request timeout")
        except aiohttp.ClientError as err:
            raise WigleAPIError(f"Connection error: {err}")
    
    async def _make_request_with_retry(self, endpoint: str, params: Dict[str, Any] = None, max_retries: int = 3) -> Dict[str, Any]:
        """Make request with exponential backoff retry."""
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return await self._make_request(endpoint, params)
            except WigleRateLimitError:
                # Don't retry rate limit errors
                raise
            except WigleAuthError:
                # Don't retry auth errors
                raise
            except WigleAPIError as e:
                last_exception = e
                if attempt == max_retries - 1:
                    break
                
                wait_time = (2 ** attempt) + (attempt * 0.1)  # Exponential backoff with jitter
                _LOGGER.warning(f"Request failed (attempt {attempt + 1}/{max_retries}), retrying in {wait_time:.1f}s: {e}")
                await asyncio.sleep(wait_time)
        
        raise last_exception or WigleAPIError("Max retries exceeded")
    
    async def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get user statistics."""
        params = {"user": username}
        return await self._make_request(WIGLE_USER_STATS_ENDPOINT, params)
    
    async def get_user_stats_with_retry(self, username: str) -> Dict[str, Any]:
        """Get user statistics with retry logic."""
        params = {"user": username}
        return await self._make_request_with_retry(WIGLE_USER_STATS_ENDPOINT, params)
    
    async def get_profile(self) -> Dict[str, Any]:
        """Get user profile."""
        return await self._make_request(WIGLE_PROFILE_ENDPOINT)
    
    async def test_connection(self) -> bool:
        """Test the API connection."""
        try:
            await self.get_profile()
            return True
        except Exception as err:
            _LOGGER.error(f"Connection test failed: {err}")
            return False
    
    async def get_detailed_stats(self, username: str) -> Dict[str, Any]:
        """Get detailed statistics with additional processing."""
        try:
            stats = await self.get_user_stats_with_retry(username)
            
            # Add computed fields
            statistics = stats.get("statistics", {})
            
            # Calculate percentages and trends
            wifi_total = statistics.get("discoveredWiFi", 0)
            wifi_gps = statistics.get("discoveredWiFiGPS", 0)
            
            if wifi_total > 0:
                statistics["wifi_gps_percentage"] = round((wifi_gps / wifi_total) * 100, 2)
            else:
                statistics["wifi_gps_percentage"] = 0
            
            # Calculate rank improvements
            current_rank = statistics.get("rank", 0)
            prev_rank = statistics.get("prevRank", 0)
            if current_rank and prev_rank:
                statistics["rank_improvement"] = prev_rank - current_rank
                statistics["rank_improvement_percentage"] = round(((prev_rank - current_rank) / prev_rank) * 100, 2) if prev_rank > 0 else 0
            
            # Calculate monthly improvements
            monthly_rank = statistics.get("monthRank", 0)
            prev_monthly_rank = statistics.get("prevMonthRank", 0)
            if monthly_rank and prev_monthly_rank:
                statistics["monthly_rank_improvement"] = prev_monthly_rank - monthly_rank
            
            stats["statistics"] = statistics
            return stats
            
        except Exception as err:
            _LOGGER.error(f"Failed to get detailed stats for {username}: {err}")
            raise