"""Support for Wigle binary sensors."""
from __future__ import annotations

from datetime import datetime, timedelta
import logging
from typing import Any

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

BINARY_SENSOR_TYPES = {
    "active_this_month": {
        "translation_key": "active_this_month",
        "icon": "mdi:calendar-check",
        "device_class": None,
    },
    "rank_improved": {
        "translation_key": "rank_improved", 
        "icon": "mdi:trending-up",
        "device_class": None,
    },
    "goal_reached": {
        "translation_key": "goal_reached",
        "icon": "mdi:target",
        "device_class": None,
    },
    "active_this_week": {
        "translation_key": "active_this_week",
        "icon": "mdi:calendar-week",
        "device_class": None,
    },
    "top_performer": {
        "translation_key": "top_performer",
        "icon": "mdi:medal",
        "device_class": None,
    },
    "monthly_goal_on_track": {
        "translation_key": "monthly_goal_on_track",
        "icon": "mdi:chart-line",
        "device_class": None,
    }
}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Wigle binary sensors."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    username = config_entry.data[CONF_USERNAME]
    
    entities = []
    
    # Only create sensors that are enabled in options
    enabled_sensors = config_entry.options.get("enabled_binary_sensors", list(BINARY_SENSOR_TYPES.keys()))
    
    for sensor_key, sensor_config in BINARY_SENSOR_TYPES.items():
        if sensor_key in enabled_sensors:
            entities.append(
                WigleBinarySensor(
                    coordinator=coordinator,
                    sensor_key=sensor_key,
                    sensor_config=sensor_config,
                    username=username,
                    config_entry=config_entry,
                )
            )
    
    async_add_entities(entities)


class WigleBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Wigle binary sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        sensor_key: str,
        sensor_config: dict,
        username: str,
        config_entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._sensor_config = sensor_config
        self._username = username
        self._config_entry = config_entry
        
        self._attr_translation_key = sensor_config["translation_key"]
        self._attr_unique_id = f"wigle_{username}_{sensor_key}"
        self._attr_icon = sensor_config["icon"]
        self._attr_device_class = sensor_config["device_class"]
        self._attr_has_entity_name = True

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
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if not self.coordinator.data:
            return None
            
        statistics = self.coordinator.data.get("statistics", {})
        
        if self._sensor_key == "active_this_month":
            return self._check_activity_this_month(statistics)
        elif self._sensor_key == "active_this_week":
            return self._check_activity_this_week(statistics)
        elif self._sensor_key == "rank_improved":
            return self._check_rank_improved(statistics)
        elif self._sensor_key == "goal_reached":
            return self._check_goal_reached(statistics)
        elif self._sensor_key == "top_performer":
            return self._check_top_performer(statistics)
        elif self._sensor_key == "monthly_goal_on_track":
            return self._check_monthly_goal_on_track(statistics)
            
        return None

    def _check_activity_this_month(self, statistics: dict) -> bool | None:
        """Check if user has been active this month."""
        last_activity = statistics.get("last")
        if not last_activity:
            return None
            
        try:
            # Format: YYYYMMDD-NNNNN
            date_part = last_activity.split("-")[0]
            last_date = datetime.strptime(date_part, "%Y%m%d")
            current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            return last_date >= current_month_start
        except (ValueError, IndexError):
            _LOGGER.warning(f"Unable to parse last activity date: {last_activity}")
            return None

    def _check_activity_this_week(self, statistics: dict) -> bool | None:
        """Check if user has been active this week."""
        last_activity = statistics.get("last")
        if not last_activity:
            return None
            
        try:
            # Format: YYYYMMDD-NNNNN
            date_part = last_activity.split("-")[0]
            last_date = datetime.strptime(date_part, "%Y%m%d")
            # Start of current week (Monday)
            now = datetime.now()
            week_start = now - timedelta(days=now.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            return last_date >= week_start
        except (ValueError, IndexError):
            _LOGGER.warning(f"Unable to parse last activity date: {last_activity}")
            return None

    def _check_rank_improved(self, statistics: dict) -> bool | None:
        """Check if rank has improved."""
        current_rank = statistics.get("rank")
        prev_rank = statistics.get("prevRank")
        
        if not current_rank or not prev_rank:
            return None
            
        # Lower rank number = better position
        improvement = prev_rank - current_rank
        
        # Check if improvement meets the threshold
        threshold = self._config_entry.options.get("notification_rank_threshold", 100)
        return improvement >= threshold

    def _check_goal_reached(self, statistics: dict) -> bool | None:
        """Check if rank goal has been reached."""
        current_rank = statistics.get("rank")
        rank_goal = self._config_entry.options.get("rank_goal", 0)
        
        if not current_rank or rank_goal <= 0:
            return None
            
        return current_rank <= rank_goal

    def _check_top_performer(self, statistics: dict) -> bool | None:
        """Check if user is in top 10% or top 1000."""
        current_rank = statistics.get("rank")
        if not current_rank:
            return None
            
        # Consider top performer if in top 1000 or if monthly rank is very good
        monthly_rank = statistics.get("monthRank", 999999)
        
        return current_rank <= 1000 or monthly_rank <= 100

    def _check_monthly_goal_on_track(self, statistics: dict) -> bool | None:
        """Check if user is on track for monthly goal based on current progress."""
        monthly_rank = statistics.get("monthRank")
        monthly_goal = self._config_entry.options.get("monthly_rank_goal", 0)
        
        if not monthly_rank or monthly_goal <= 0:
            return None
            
        # Get current day of month to calculate if on track
        now = datetime.now()
        days_in_month = (now.replace(month=now.month + 1, day=1) - timedelta(days=1)).day
        progress_ratio = now.day / days_in_month
        
        # If we're ahead of where we need to be rank-wise, we're on track
        expected_rank_by_now = monthly_goal / progress_ratio
        return monthly_rank <= expected_rank_by_now

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {}
            
        statistics = self.coordinator.data.get("statistics", {})
        attributes = {"username": statistics.get("userName", self._username)}
        
        if self._sensor_key == "rank_improved":
            current_rank = statistics.get("rank")
            prev_rank = statistics.get("prevRank")
            if current_rank and prev_rank:
                improvement = prev_rank - current_rank
                attributes.update({
                    "current_rank": current_rank,
                    "previous_rank": prev_rank,
                    "rank_improvement": improvement,
                    "improvement_threshold": self._config_entry.options.get("notification_rank_threshold", 100),
                })
                
        elif self._sensor_key == "goal_reached":
            current_rank = statistics.get("rank")
            rank_goal = self._config_entry.options.get("rank_goal", 0)
            if current_rank:
                attributes.update({
                    "current_rank": current_rank,
                    "goal": rank_goal,
                    "distance_to_goal": max(0, current_rank - rank_goal) if rank_goal > 0 else None,
                })
                
        elif self._sensor_key == "top_performer":
            attributes.update({
                "current_rank": statistics.get("rank"),
                "monthly_rank": statistics.get("monthRank"),
                "top_1000": statistics.get("rank", 999999) <= 1000,
                "top_100_monthly": statistics.get("monthRank", 999999) <= 100,
            })
            
        elif self._sensor_key in ["active_this_month", "active_this_week"]:
            last_activity = statistics.get("last")
            first_activity = statistics.get("first")
            attributes.update({
                "last_activity": last_activity,
                "first_activity": first_activity,
            })
            
            if last_activity:
                try:
                    date_part = last_activity.split("-")[0]
                    last_date = datetime.strptime(date_part, "%Y%m%d")
                    days_since = (datetime.now() - last_date).days
                    attributes["days_since_last_activity"] = days_since
                except (ValueError, IndexError):
                    pass
                    
        elif self._sensor_key == "monthly_goal_on_track":
            monthly_rank = statistics.get("monthRank")
            monthly_goal = self._config_entry.options.get("monthly_rank_goal", 0)
            if monthly_rank:
                now = datetime.now()
                progress_ratio = now.day / 30  # Approximation
                attributes.update({
                    "monthly_rank": monthly_rank,
                    "monthly_goal": monthly_goal,
                    "progress_ratio": round(progress_ratio, 2),
                    "days_remaining": (datetime(now.year, now.month + 1, 1) - now).days if now.month < 12 else (datetime(now.year + 1, 1, 1) - now).days,
                })
                
        return attributes

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success