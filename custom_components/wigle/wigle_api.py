"""Wigle API client with enhanced error handling and retry logic.

This module provides a robust API client for interacting with the Wigle.net API,
including authentication, rate limiting, error handling, and automatic retry logic.
"""
from __future__ import annotations

import asyncio
import base64
import logging
import time
from typing import Any, Dict

import aiohttp

from .const import (
    MAX_REQUESTS_PER_HOUR,
    REQUEST_TIMEOUT_SECONDS,
    WIGLE_API_BASE,
    WIGLE_PROFILE_ENDPOINT,
    WIGLE_USER_STATS_ENDPOINT,
)

_LOGGER: logging.Logger = logging.getLogger(__name__)


class WigleAPIError(Exception):
    """Base exception for Wigle API errors.
    
    Raised when an API request fails with a generic error.
    """

    pass


class WigleAuthError(WigleAPIError):
    """Exception for authentication errors.
    
    Raised when API credentials are invalid or authentication fails.
    """

    pass


class WigleRateLimitError(WigleAPIError):
    """Exception for rate limit errors.
    
    Raised when the API rate limit (100 requests/hour) is exceeded.
    """

    pass


class WigleAPI:
    """Wigle API client with enhanced error handling.
    
    Provides methods for authenticating with the Wigle API and fetching
    user statistics with automatic retry logic and rate limiting.
    
    Attributes:
        username: The Wigle username.
        api_name: The API credential name (starts with AID).
        api_token: The API credential token.
        session: The aiohttp ClientSession for making HTTP requests.
    """

    def __init__(
        self,
        username: str,
        api_name: str,
        api_token: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Initialize the API client.
        
        Args:
            username: The Wigle username.
            api_name: The API credential name (starts with AID).
            api_token: The API credential token.
            session: The aiohttp ClientSession for making HTTP requests.
        """
        self.username: str = username
        self.api_name: str = api_name
        self.api_token: str = api_token
        self.session: aiohttp.ClientSession = session
        self._auth_header: str = self._create_auth_header(api_name, api_token)
        self._last_request_time: float = 0.0
        self._request_count: int = 0
        self._max_requests_per_hour: int = MAX_REQUESTS_PER_HOUR

    def _create_auth_header(self, api_name: str, api_token: str) -> str:
        """Create basic auth header using API Name and API Token.
        
        Args:
            api_name: The API credential name.
            api_token: The API credential token.
            
        Returns:
            A properly formatted HTTP Basic Authorization header string.
            
        Note:
            Credentials are masked in logs for security.
        """
        credentials: str = f"{api_name}:{api_token}"
        encoded_credentials: str = base64.b64encode(
            credentials.encode()
        ).decode()
        return f"Basic {encoded_credentials}"

    async def _rate_limit_check(self) -> None:
        """Check and enforce rate limiting.
        
        Tracks requests and enforces a maximum of 100 requests per hour.
        Raises WigleRateLimitError if the limit is exceeded.
        
        Raises:
            WigleRateLimitError: If the rate limit has been exceeded.
        """
        current_time: float = time.time()

        # Reset counter every hour
        if current_time - self._last_request_time > 3600:
            self._request_count = 0
            self._last_request_time = current_time

        if self._request_count >= self._max_requests_per_hour:
            wait_time: float = 3600 - (current_time - self._last_request_time)
            _LOGGER.warning(
                f"Rate limit reached, waiting {wait_time:.0f} seconds"
            )
            raise WigleRateLimitError(
                f"Rate limit exceeded, retry in {wait_time:.0f} seconds"
            )

        self._request_count += 1

    async def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """Make an authenticated request to the Wigle API.
        
        Args:
            endpoint: The API endpoint path (e.g., "/stats/user").
            params: Optional query parameters for the request.
            
        Returns:
            The JSON response data from the API.
            
        Raises:
            WigleAuthError: If authentication fails (401).
            WigleRateLimitError: If rate limit is exceeded (429).
            WigleAPIError: For other HTTP errors or invalid responses.
        """
        await self._rate_limit_check()

        url: str = f"{WIGLE_API_BASE}{endpoint}"
        headers: Dict[str, str] = {
            "Accept": "application/json",
            "Authorization": self._auth_header,
            "User-Agent": f"HomeAssistant-Wigle/{self.username}",
        }

        _LOGGER.debug(f"Making request to {url} with params: {params}")

        try:
            async with self.session.get(
                url,
                headers=headers,
                params=params,
                timeout=REQUEST_TIMEOUT_SECONDS,
            ) as response:
                response_text: str = await response.text()

                if response.status == 401:
                    raise WigleAuthError("Invalid API credentials")
                elif response.status == 429:
                    raise WigleRateLimitError("Rate limit exceeded")
                elif response.status == 200:
                    try:
                        data: Dict[str, Any] = await response.json()
                        if data.get("success"):
                            return data
                        else:
                            error_msg: str = data.get(
                                "message", "API returned success=false"
                            )
                            _LOGGER.error(f"API error: {error_msg}")
                            raise WigleAPIError(f"API error: {error_msg}")
                    except ValueError as e:
                        _LOGGER.error(f"Invalid JSON response: {response_text}")
                        raise WigleAPIError(f"Invalid JSON response: {e}") from e
                else:
                    _LOGGER.error(f"HTTP {response.status}: {response_text}")
                    raise WigleAPIError(
                        f"HTTP {response.status}: {response_text}"
                    )

        except asyncio.TimeoutError as e:
            raise WigleAPIError("Request timeout") from e
        except aiohttp.ClientError as err:
            raise WigleAPIError(f"Connection error: {err}") from err

    async def _make_request_with_retry(
        self,
        endpoint: str,
        params: Dict[str, Any] | None = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """Make request with exponential backoff retry.
        
        Automatically retries failed requests with exponential backoff,
        except for authentication and rate limit errors.
        
        Args:
            endpoint: The API endpoint path.
            params: Optional query parameters.
            max_retries: Maximum number of retry attempts (default: 3).
            
        Returns:
            The JSON response data from the API.
            
        Raises:
            WigleAuthError: If authentication fails (not retried).
            WigleRateLimitError: If rate limit is exceeded (not retried).
            WigleAPIError: If all retry attempts fail.
        """
        last_exception: WigleAPIError | None = None

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

                wait_time: float = (
                    (2 ** attempt) + (attempt * 0.1)
                )  # Exponential backoff
                _LOGGER.warning(
                    f"Request failed (attempt {attempt + 1}/{max_retries}), "
                    f"retrying in {wait_time:.1f}s: {e}"
                )
                await asyncio.sleep(wait_time)

        raise last_exception or WigleAPIError("Max retries exceeded")

    async def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get user statistics.
        
        Args:
            username: The Wigle username.
            
        Returns:
            The user statistics response from the API.
        """
        params: Dict[str, str] = {"user": username}
        return await self._make_request(WIGLE_USER_STATS_ENDPOINT, params)

    async def get_user_stats_with_retry(
        self, username: str
    ) -> Dict[str, Any]:
        """Get user statistics with retry logic.
        
        Args:
            username: The Wigle username.
            
        Returns:
            The user statistics response from the API.
        """
        params: Dict[str, str] = {"user": username}
        return await self._make_request_with_retry(
            WIGLE_USER_STATS_ENDPOINT, params
        )

    async def get_profile(self) -> Dict[str, Any]:
        """Get user profile information.
        
        Returns:
            The user profile response from the API.
        """
        return await self._make_request(WIGLE_PROFILE_ENDPOINT)

    async def test_connection(self) -> bool:
        """Test the API connection.
        
        Attempts to fetch the user profile to verify API credentials
        and network connectivity.
        
        Returns:
            True if connection is successful, False otherwise.
        """
        try:
            await self.get_profile()
            return True
        except Exception as err:
            _LOGGER.error(f"Connection test failed: {err}")
            return False

    async def get_detailed_stats(self, username: str) -> Dict[str, Any]:
        """Get detailed statistics with additional processing.
        
        Fetches user statistics and computes additional metrics such as
        percentage of WiFi with GPS coordinates and rank improvements.
        
        Args:
            username: The Wigle username.
            
        Returns:
            The statistics response with computed metrics.
            
        Raises:
            WigleAPIError: If the API request fails.
        """
        try:
            stats: Dict[str, Any] = (
                await self.get_user_stats_with_retry(username)
            )

            # Add computed fields
            statistics: Dict[str, Any] = stats.get("statistics", {})

            # Calculate WiFi GPS percentage
            wifi_total: int = statistics.get("discoveredWiFi", 0)
            wifi_gps: int = statistics.get("discoveredWiFiGPS", 0)

            if wifi_total > 0:
                statistics["wifi_gps_percentage"] = round(
                    (wifi_gps / wifi_total) * 100, 2
                )
            else:
                statistics["wifi_gps_percentage"] = 0

            # Calculate rank improvements
            current_rank: int | None = statistics.get("rank")
            prev_rank: int | None = statistics.get("prevRank")
            if current_rank and prev_rank:
                statistics["rank_improvement"] = prev_rank - current_rank
                statistics["rank_improvement_percentage"] = (
                    round(
                        ((prev_rank - current_rank) / prev_rank) * 100, 2
                    )
                    if prev_rank > 0
                    else 0
                )

            # Calculate monthly improvements
            monthly_rank: int | None = statistics.get("monthRank")
            prev_monthly_rank: int | None = statistics.get("prevMonthRank")
            if monthly_rank and prev_monthly_rank:
                statistics["monthly_rank_improvement"] = (
                    prev_monthly_rank - monthly_rank
                )

            stats["statistics"] = statistics
            return stats

        except Exception as err:
            _LOGGER.error(
                f"Failed to get detailed stats for {username}: {err}"
            )
            raise