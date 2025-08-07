"""Config flow for Wigle WiFi Network Statistics integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, CONF_API_NAME, CONF_API_TOKEN
from .wigle_api import WigleAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_API_NAME): cv.string,
        vol.Required(CONF_API_TOKEN): cv.string,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.
    
    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    session = async_get_clientsession(hass)
    api = WigleAPI(data[CONF_USERNAME], data[CONF_API_NAME], data[CONF_API_TOKEN], session)
    
    if not await api.test_connection():
        raise InvalidAuth
        
    # Test getting user stats
    try:
        stats = await api.get_user_stats(data[CONF_USERNAME])
        username = stats.get("user", data[CONF_USERNAME])
    except Exception as err:
        _LOGGER.error(f"Failed to get user stats: {err}")
        raise CannotConnect
    
    # Return info that you want to store in the config entry.
    return {"title": f"Wigle - {username}", "username": username}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wigle WiFi Network Statistics."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            # Check if already configured
            await self.async_set_unique_id(info["username"])
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""