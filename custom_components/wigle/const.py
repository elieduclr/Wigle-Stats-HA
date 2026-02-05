"""Constants for the Wigle WiFi Network Statistics integration.

This module contains all constant values used throughout the Wigle integration,
including configuration keys, API endpoints, and sensor type definitions.
"""

# Integration domain identifier
DOMAIN: str = "wigle"

# Configuration schema keys
CONF_API_NAME: str = "api_name"
CONF_API_TOKEN: str = "api_token"

# API Configuration and Endpoints
WIGLE_API_BASE: str = "https://api.wigle.net/api/v2"
WIGLE_USER_STATS_ENDPOINT: str = "/stats/user"
WIGLE_PROFILE_ENDPOINT: str = "/profile/user"

# API Rate limiting
MAX_REQUESTS_PER_HOUR: int = 100
REQUEST_TIMEOUT_SECONDS: int = 30

# Sensor Types - Keys will be translated via strings.json
SENSOR_TYPES: dict[str, dict[str, str | None]] = {
    "rank": {
        "translation_key": "rank",
        "icon": "mdi:trophy",
        "unit": None,
        "device_class": None,
    },
    "month_rank": {
        "translation_key": "month_rank",
        "icon": "mdi:trophy-outline",
        "unit": None,
        "device_class": None,
    },
    "discovered_wifi_gps": {
        "translation_key": "discovered_wifi_gps",
        "icon": "mdi:wifi",
        "unit": "networks",
        "device_class": None,
    },
    "discovered_wifi": {
        "translation_key": "discovered_wifi",
        "icon": "mdi:wifi",
        "unit": "networks", 
        "device_class": None,
    },
    "discovered_cell_gps": {
        "translation_key": "discovered_cell_gps",
        "icon": "mdi:cell-phone-wireless",
        "unit": "towers",
        "device_class": None,
    },
    "discovered_cell": {
        "translation_key": "discovered_cell",
        "icon": "mdi:cell-phone-wireless", 
        "unit": "towers",
        "device_class": None,
    },
    "discovered_bt_gps": {
        "translation_key": "discovered_bt_gps",
        "icon": "mdi:bluetooth",
        "unit": "devices",
        "device_class": None,
    },
    "discovered_bt": {
        "translation_key": "discovered_bt",
        "icon": "mdi:bluetooth",
        "unit": "devices",
        "device_class": None,
    },
    "total_wifi_locations": {
        "translation_key": "total_wifi_locations",
        "icon": "mdi:map-marker-multiple",
        "unit": "locations",
        "device_class": None,
    },
}