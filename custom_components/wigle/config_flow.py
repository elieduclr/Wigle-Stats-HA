"""Config flow for Wigle WiFi Network Statistics integration.

This module handles the configuration flow for setting up and managing
the Wigle integration in Home Assistant.
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .const import CONF_API_NAME, CONF_API_TOKEN, DOMAIN, SENSOR_TYPES
from .wigle_api import WigleAPI, WigleAuthError, WigleAPIError

_LOGGER: logging.Logger = logging.getLogger(__name__)

# Schema for the initial setup step
STEP_USER_DATA_SCHEMA: vol.Schema = vol.Schema(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_API_NAME): cv.string,
        vol.Required(CONF_API_TOKEN): cv.string,
    }
)


async def validate_input(
    hass: HomeAssistant, data: dict[str, Any]
) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Args:
        hass: The Home Assistant instance.
        data: Dictionary with values from STEP_USER_DATA_SCHEMA.

    Returns:
        Dictionary with validated data and title.

    Raises:
        CannotConnect: If connection test fails.
        InvalidAuth: If credentials are invalid.
    """
    session = async_get_clientsession(hass)
    api: WigleAPI = WigleAPI(
        data[CONF_USERNAME],
        data[CONF_API_NAME],
        data[CONF_API_TOKEN],
        session,
    )

    if not await api.test_connection():
        raise InvalidAuth()

    # Test getting user stats
    try:
        stats: dict[str, Any] = await api.get_user_stats(
            data[CONF_USERNAME]
        )
        username: str = stats.get("user", data[CONF_USERNAME])
    except WigleAuthError as err:
        _LOGGER.error(f"Authentication failed: {err}")
        raise InvalidAuth() from err
    except Exception as err:
        _LOGGER.error(f"Failed to get user stats: {err}")
        raise CannotConnect() from err

    # Return info that you want to store in the config entry.
    return {"title": f"Wigle - {username}", "username": username}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Wigle WiFi Network Statistics.
    
    Manages user input for adding and configuring Wigle integration entries.
    """

    VERSION: int = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step.
        
        Args:
            user_input: User input from the form if provided.
            
        Returns:
            A FlowResult dict for either showing the form or creating the entry.
        """
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors: dict[str, str] = {}

        try:
            info: dict[str, Any] = await validate_input(
                self.hass, user_input
            )
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

            return self.async_create_entry(
                title=info["title"], data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlowHandler:
        """Get the options flow for this handler.
        
        Args:
            config_entry: The configuration entry.
            
        Returns:
            An OptionsFlowHandler instance.
        """
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handle Wigle options.
    
    Manages advanced configuration options for an existing integration entry.
    """

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow.
        
        Args:
            config_entry: The configuration entry.
        """
        self._config_entry: config_entries.ConfigEntry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options.
        
        Args:
            user_input: User input from the form if provided.
            
        Returns:
            A FlowResult dict for either showing the form or creating entry.
        """
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Create sensor selection options
        sensor_options: dict[str, str] = {
            key: config["translation_key"]
            for key, config in SENSOR_TYPES.items()
        }

        options_schema: vol.Schema = vol.Schema(
            {
                vol.Optional(
                    "update_interval",
                    default=self._config_entry.options.get(
                        "update_interval", 60
                    ),
                ): vol.All(
                    vol.Coerce(int), vol.Range(min=30, max=1440)
                ),
                vol.Optional(
                    "rank_goal",
                    default=self._config_entry.options.get("rank_goal", 0),
                ): vol.All(vol.Coerce(int), vol.Range(min=0)),
                vol.Optional(
                    "monthly_rank_goal",
                    default=self._config_entry.options.get(
                        "monthly_rank_goal", 0
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=0)),
                vol.Optional(
                    "enabled_sensors",
                    default=self._config_entry.options.get(
                        "enabled_sensors", list(SENSOR_TYPES.keys())
                    ),
                ): cv.multi_select(sensor_options),
                vol.Optional(
                    "notifications_enabled",
                    default=self._config_entry.options.get(
                        "notifications_enabled", False
                    ),
                ): bool,
                vol.Optional(
                    "notification_rank_threshold",
                    default=self._config_entry.options.get(
                        "notification_rank_threshold", 100
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1)),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            description_placeholders={
                "update_interval_desc": "Update interval in minutes (30-1440)",
                "rank_goal_desc": "Target global rank (0 = disabled)",
                "monthly_rank_goal_desc": "Target monthly rank (0 = disabled)",
                "sensors_desc": "Select which sensors to enable",
                "notifications_desc": "Enable rank change notifications",
                "threshold_desc": "Minimum rank change for notifications",
            },
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""

    pass


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""

    pass