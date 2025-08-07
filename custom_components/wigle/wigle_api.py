"""Wigle API client."""
from __future__ import annotations

import asyncio
import aiohttp
import base64
import logging
from typing import Any, Dict

from .const import WIGLE_API_BASE, WIGLE_USER_STATS_ENDPOINT, WIGLE_PROFILE_ENDPOINT

_LOGGER = logging.getLogger(__name__)


class WigleAPI:
    """Wigle API client."""
    
    def __init__(self, username: str, api_name: str, api_token: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self.username = username
        self.api_name = api_name
        self.api_token = api_token
        self.session = session
        self._auth_header = self._create_auth_header(api_name, api_token)
    
    def _create_auth_header(self, api_name: str, api_token: str) -> str:
        """Create basic auth header using API Name and API Token."""
        credentials = f"{api_name}:{api_token}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded_credentials}"
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make an authenticated request to the Wigle API."""
        url = f"{WIGLE_API_BASE}{endpoint}"
        headers = {
            "Accept": "application/json",
            "Authorization": self._auth_header,
        }
        
        _LOGGER.debug(f"Making request to {url}")
        
        try:
            async with self.session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        return data
                    else:
                        raise Exception(f"API returned success=false: {data}")
                else:
                    text = await response.text()
                    raise Exception(f"HTTP {response.status}: {text}")
                    
        except aiohttp.ClientError as err:
            raise Exception(f"Connection error: {err}")
    
    async def get_user_stats(self, username: str) -> Dict[str, Any]:
        """Get user statistics."""
        params = {"user": username}
        return await self._make_request(WIGLE_USER_STATS_ENDPOINT, params)
    
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