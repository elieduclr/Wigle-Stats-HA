"""The Wigle WiFi Network Statistics integration."""
from __future__ import annotations

import asyncio
from datetime import timedelta
import logging

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady, ServiceValidationError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_API_NAME, CONF_API_TOKEN
from .wigle_api import WigleAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR]

# Services
SERVICE_FORCE_UPDATE = "force_update"
SERVICE_SET_RANK_GOAL = "set_rank_goal"
SERVICE_RESET_STATISTICS = "reset_statistics"

# Service schemas
FORCE_UPDATE_SCHEMA = vol.Schema({
    vol.Required("username"): cv.string,
})

SET_RANK_GOAL_SCHEMA = vol.Schema({
    vol.Required("username"): cv.string,
    vol.Required("goal"): vol.All(vol.Coerce(int), vol.Range(min=1)),
    vol.Optional("monthly_goal"): vol.All(vol.Coerce(int), vol.Range(min=1)),
})

RESET_STATISTICS_SCHEMA = vol.Schema({
    vol.Required("username"): cv.string,
})


class WigleDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Wigle data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        wigle_api: WigleAPI,
        username: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.wigle_api = wigle_api
        self.username = username
        self._consecutive_errors = 0
        self._last_successful_data = None
        
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{username}",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint with robust error handling."""
        try:
            # Try to get user stats with retry logic built into the API client
            data = await self.wigle_api.get_user_stats_with_retry(self.username)
            
            # Reset error counter on success
            self._consecutive_errors = 0
            self._last_successful_data = data
            
            _LOGGER.debug(f"Successfully updated data for {self.username}")
            return data
            
        except Exception as err:
            self._consecutive_errors += 1
            
            # If we have recent successful data and haven't had too many consecutive errors,
            # return the last known good data instead of failing completely
            if self._consecutive_errors <= 3 and self._last_successful_data:
                _LOGGER.warning(
                    f"Error updating Wigle data for {self.username} (attempt {self._consecutive_errors}), "
                    f"using cached data: {err}"
                )
                return self._last_successful_data
            
            # After too many consecutive failures, raise the error
            _LOGGER.error(
                f"Failed to update Wigle data for {self.username} after {self._consecutive_errors} attempts: {err}"
            )
            raise UpdateFailed(f"Error communicating with API: {err}")


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Wigle WiFi Network Statistics from a config entry."""
    
    # Get update interval from options (default 1 hour)
    update_interval_minutes = entry.options.get("update_interval", 60)
    update_interval = timedelta(minutes=update_interval_minutes)
    
    wigle_api = WigleAPI(
        username=entry.data[CONF_USERNAME],
        api_name=entry.data[CONF_API_NAME],
        api_token=entry.data[CONF_API_TOKEN],
        session=async_get_clientsession(hass)
    )
    
    coordinator = WigleDataUpdateCoordinator(
        hass, wigle_api, entry.data[CONF_USERNAME], update_interval
    )
    
    # Fetch initial data so we have data when entities subscribe
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        _LOGGER.error(f"Failed to connect to Wigle API for {entry.data[CONF_USERNAME]}")
        raise
    
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    
    # Register services only once (for the first entry)
    if len(hass.data[DOMAIN]) == 1:
        await async_setup_services(hass)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Set up options update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for the Wigle integration."""
    
    async def async_force_update(call: ServiceCall) -> None:
        """Force update of Wigle data."""
        username = call.data["username"]
        
        coordinator = None
        for entry_id, coord in hass.data[DOMAIN].items():
            config_entry = hass.config_entries.async_get_entry(entry_id)
            if config_entry and config_entry.data.get(CONF_USERNAME) == username:
                coordinator = coord
                break
        
        if not coordinator:
            raise ServiceValidationError(f"No Wigle integration found for username: {username}")
        
        _LOGGER.info(f"Forcing update for {username}")
        await coordinator.async_request_refresh()

    async def async_set_rank_goal(call: ServiceCall) -> None:
        """Set rank goal for user."""
        username = call.data["username"]
        goal = call.data["goal"]
        monthly_goal = call.data.get("monthly_goal")
        
        config_entry = None
        coordinator = None
        for entry_id, coord in hass.data[DOMAIN].items():
            entry = hass.config_entries.async_get_entry(entry_id)
            if entry and entry.data.get(CONF_USERNAME) == username:
                config_entry = entry
                coordinator = coord
                break
        
        if not config_entry:
            raise ServiceValidationError(f"No Wigle integration found for username: {username}")
        
        # Update options
        new_options = dict(config_entry.options)
        new_options["rank_goal"] = goal
        if monthly_goal:
            new_options["monthly_rank_goal"] = monthly_goal
        
        hass.config_entries.async_update_entry(
            config_entry, options=new_options
        )
        
        _LOGGER.info(f"Set rank goal {goal} for {username}")
        if monthly_goal:
            _LOGGER.info(f"Set monthly rank goal {monthly_goal} for {username}")
        
        # Force update to refresh goal-related sensors
        await coordinator.async_request_refresh()

    async def async_reset_statistics(call: ServiceCall) -> None:
        """Reset cached statistics and force fresh data retrieval."""
        username = call.data["username"]
        
        coordinator = None
        for entry_id, coord in hass.data[DOMAIN].items():
            config_entry = hass.config_entries.async_get_entry(entry_id)
            if config_entry and config_entry.data.get(CONF_USERNAME) == username:
                coordinator = coord
                break
        
        if not coordinator:
            raise ServiceValidationError(f"No Wigle integration found for username: {username}")
        
        # Reset cached data and error counters
        coordinator._last_successful_data = None
        coordinator._consecutive_errors = 0
        
        _LOGGER.info(f"Reset statistics cache for {username}")
        await coordinator.async_request_refresh()

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_FORCE_UPDATE,
        async_force_update,
        schema=FORCE_UPDATE_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_RANK_GOAL,
        async_set_rank_goal,
        schema=SET_RANK_GOAL_SCHEMA,
    )
    
    hass.services.async_register(
        DOMAIN,
        SERVICE_RESET_STATISTICS,
        async_reset_statistics,
        schema=RESET_STATISTICS_SCHEMA,
    )


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options change."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Unregister services if this is the last entry
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_FORCE_UPDATE)
            hass.services.async_remove(DOMAIN, SERVICE_SET_RANK_GOAL)
            hass.services.async_remove(DOMAIN, SERVICE_RESET_STATISTICS)
    
    return unload_ok