"""Constants for the Wigle WiFi Network Statistics integration."""

DOMAIN = "wigle"

# Configuration
CONF_API_NAME = "api_name"
CONF_API_TOKEN = "api_token"

# API Constants
WIGLE_API_BASE = "https://api.wigle.net/api/v2"
WIGLE_USER_STATS_ENDPOINT = "/stats/user"
WIGLE_PROFILE_ENDPOINT = "/profile/user"

# Sensor Types - Keys will be translated via strings.json
SENSOR_TYPES = {
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