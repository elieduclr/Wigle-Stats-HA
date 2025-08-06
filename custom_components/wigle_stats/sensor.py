import logging
import base64
import requests
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN, BASE_URL

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=12)

def get_auth_header(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    username = config.get("username")
    password = config.get("password")

    def fetch_data():
        try:
            headers = get_auth_header(username, password)
            headers["Accept"] = "application/json"
            response = requests.get(BASE_URL, headers=headers, timeout=10)
            return response.json()
        except Exception as e:
            _LOGGER.error("Erreur API Wigle : %s", e)
            return {}

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Wigle Stats",
        update_method=hass.async_add_executor_job(fetch_data),
        update_interval=SCAN_INTERVAL,
    )

    await coordinator.async_config_entry_first_refresh()
    async_add_entities([WigleSensor(coordinator)], True)

class WigleSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Wigle Stats"
        self._attr_unique_id = "wigle_stats"

    @property
    def native_value(self):
        return self.coordinator.data.get("rank")

    @property
    def extra_state_attributes(self):
        return self.coordinator.data.get("statistics", {})
