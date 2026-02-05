"""Support for Wigle WiFi Network Statistics sensors.

This module provides sensor entities for tracking Wigle WiFi network statistics,
including rank, discovered networks, cell towers, and Bluetooth devices.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, SENSOR_TYPES

_LOGGER: logging.Logger = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Wigle sensors from a config entry.
    
    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry.
        async_add_entities: Callback to add entities.
    """
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ]
    username: str = config_entry.data[CONF_USERNAME]

    entities: list[WigleSensor] = []

    # Add all sensor types
    for sensor_key, sensor_config in SENSOR_TYPES.items():
        entities.append(
            WigleSensor(
                coordinator=coordinator,
                sensor_key=sensor_key,
                sensor_config=sensor_config,
                username=username,
            )
        )

    async_add_entities(entities)


class WigleSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Wigle sensor.
    
    Provides access to Wigle statistics data including rankings, network
    discovery counts, and other metrics from the Wigle.net API.
    
    Attributes:
        coordinator: The data update coordinator.
        _sensor_key: The unique sensor identifier.
        _sensor_config: Configuration dictionary for this sensor.
        _username: The Wigle username being monitored.
    """

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        sensor_key: str,
        sensor_config: dict[str, Any],
        username: str,
    ) -> None:
        """Initialize the sensor.
        
        Args:
            coordinator: The data update coordinator.
            sensor_key: The unique sensor identifier.
            sensor_config: Configuration dictionary for this sensor.
            username: The Wigle username.
        """
        super().__init__(coordinator)
        self._sensor_key: str = sensor_key
        self._sensor_config: dict[str, Any] = sensor_config
        self._username: str = username

        # Use translation key for the entity name
        self._attr_translation_key: str = sensor_config["translation_key"]
        self._attr_unique_id: str = f"wigle_{username}_{sensor_key}"
        self._attr_icon: str = sensor_config["icon"]
        self._attr_native_unit_of_measurement: str | None = (
            sensor_config["unit"]
        )
        self._attr_device_class: str | None = sensor_config["device_class"]

        # Set has_entity_name to True to use translation system
        self._attr_has_entity_name: bool = True

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this Wigle account.
        
        Returns:
            Dictionary containing device identifiers and metadata.
        """
        return {
            "identifiers": {(DOMAIN, self._username)},
            "name": f"Wigle Account ({self._username})",
            "manufacturer": "Wigle.net",
            "model": "WiFi Network Statistics",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor.
        
        Returns:
            The current sensor value from the API data, or None if unavailable.
        """
        if not self.coordinator.data:
            return None

        statistics: dict[str, Any] = self.coordinator.data.get(
            "statistics", {}
        )

        # Map sensor keys to API response keys
        key_mapping: dict[str, str] = {
            "rank": "rank",
            "month_rank": "monthRank",
            "discovered_wifi_gps": "discoveredWiFiGPS",
            "discovered_wifi": "discoveredWiFi",
            "discovered_cell_gps": "discoveredCellGPS",
            "discovered_cell": "discoveredCell",
            "discovered_bt_gps": "discoveredBtGPS",
            "discovered_bt": "discoveredBt",
            "total_wifi_locations": "totalWiFiLocations",
        }

        api_key: str | None = key_mapping.get(self._sensor_key)
        if api_key:
            return statistics.get(api_key)

        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes.
        
        Returns:
            Dictionary of additional attributes specific to the sensor type.
        """
        if not self.coordinator.data:
            return {}

        statistics: dict[str, Any] = self.coordinator.data.get(
            "statistics", {}
        )

        attributes: dict[str, Any] = {}

        # Add some common attributes for all sensors
        if "userName" in statistics:
            attributes["username"] = statistics["userName"]

        if "discoveredWiFiGPSPercent" in statistics:
            attributes["wifi_gps_percentage"] = statistics[
                "discoveredWiFiGPSPercent"
            ]

        # Add rank-specific attributes
        if self._sensor_key == "rank":
            if "prevRank" in statistics:
                attributes["previous_rank"] = statistics["prevRank"]
                attributes["rank_change"] = (
                    statistics.get("prevRank", 0)
                    - statistics.get("rank", 0)
                )

        elif self._sensor_key == "month_rank":
            if "prevMonthRank" in statistics:
                attributes["previous_month_rank"] = statistics[
                    "prevMonthRank"
                ]
                attributes["month_rank_change"] = (
                    statistics.get("prevMonthRank", 0)
                    - statistics.get("monthRank", 0)
                )

        # Add first/last activity dates
        if "first" in statistics:
            attributes["first_activity"] = statistics["first"]
        if "last" in statistics:
            attributes["last_activity"] = statistics["last"]

        return attributes

    @property
    def available(self) -> bool:
        """Return if entity is available.
        
        Returns:
            True if the coordinator has successfully updated data.
        """
        return self.coordinator.last_update_success