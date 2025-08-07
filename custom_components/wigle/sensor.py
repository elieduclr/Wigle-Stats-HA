"""Support for Wigle WiFi Network Statistics sensors."""
from __future__ import annotations

from datetime import datetime
import logging
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

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Wigle sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    username = config_entry.data[CONF_USERNAME]
    
    entities = []
    
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
    """Representation of a Wigle sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        sensor_key: str,
        sensor_config: dict,
        username: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._sensor_config = sensor_config
        self._username = username
        self._attr_name = f"Wigle {sensor_config['name']}"
        self._attr_unique_id = f"wigle_{username}_{sensor_key}"
        self._attr_icon = sensor_config["icon"]
        self._attr_native_unit_of_measurement = sensor_config["unit"]
        self._attr_device_class = sensor_config["device_class"]

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this Wigle account."""
        return {
            "identifiers": {(DOMAIN, self._username)},
            "name": f"Wigle Account ({self._username})",
            "manufacturer": "Wigle.net",
            "model": "WiFi Network Statistics",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
            
        statistics = self.coordinator.data.get("statistics", {})
        
        # Map sensor keys to API response keys
        key_mapping = {
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
        
        api_key = key_mapping.get(self._sensor_key)
        if api_key:
            return statistics.get(api_key)
        
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
            
        statistics = self.coordinator.data.get("statistics", {})
        
        attributes = {}
        
        # Add some common attributes for all sensors
        if "userName" in statistics:
            attributes["username"] = statistics["userName"]
            
        if "discoveredWiFiGPSPercent" in statistics:
            attributes["wifi_gps_percentage"] = statistics["discoveredWiFiGPSPercent"]
            
        # Add rank-specific attributes
        if self._sensor_key == "rank":
            if "prevRank" in statistics:
                attributes["previous_rank"] = statistics["prevRank"]
                attributes["rank_change"] = statistics.get("prevRank", 0) - statistics.get("rank", 0)
                
        elif self._sensor_key == "month_rank":
            if "prevMonthRank" in statistics:
                attributes["previous_month_rank"] = statistics["prevMonthRank"]
                attributes["month_rank_change"] = statistics.get("prevMonthRank", 0) - statistics.get("monthRank", 0)
        
        # Add first/last activity dates
        if "first" in statistics:
            attributes["first_activity"] = statistics["first"]
        if "last" in statistics:
            attributes["last_activity"] = statistics["last"]
            
        return attributes

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success