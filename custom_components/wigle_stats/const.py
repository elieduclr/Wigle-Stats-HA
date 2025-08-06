"""Constants for the Wigle WiFi Network Statistics integration."""

DOMAIN = "wigle"

# Configuration
CONF_API_NAME = "api_name"
CONF_API_TOKEN = "api_token"

# API Constants
WIGLE_API_BASE = "https://api.wigle.net/api/v2"
WIGLE_USER_STATS_ENDPOINT = "/stats/user"
WIGLE_PROFILE_ENDPOINT = "/profile/user"

# Sensor Types
SENSOR_TYPES = {
    "rank": {
        "name": "Rank",
        "icon": "mdi:trophy",
        "unit": None,
        "device_class": None,
    },
    "month_rank": {
        "name": "Monthly Rank",
        "icon": "mdi:trophy-outline",
        "unit": None,
        "device_class": None,
    },
    "discovered_wifi_gps": {
        "name": "WiFi Networks with GPS",
        "icon": "mdi:wifi",
        "unit": "networks",
        "device_class": None,
    },
    "discovered_wifi": {
        "name": "WiFi Networks Discovered",
        "icon": "mdi:wifi",
        "unit": "networks", 
        "device_class": None,
    },
    "discovered_cell_gps": {
        "name": "Cell Towers with GPS",
        "icon": "mdi:cell-phone-wireless",
        "unit": "towers",
        "device_class": None,
    },
    "discovered_cell": {
        "name": "Cell Towers Discovered",
        "icon": "mdi:cell-phone-wireless", 
        "unit": "towers",
        "device_class": None,
    },
    "discovered_bt_gps": {
        "name": "Bluetooth Devices with GPS",
        "icon": "mdi:bluetooth",
        "unit": "devices",
        "device_class": None,
    },
    "discovered_bt": {
        "name": "Bluetooth Devices Discovered", 
        "icon": "mdi:bluetooth",
        "unit": "devices",
        "device_class": None,
    },
    "total_wifi_locations": {
        "name": "Total WiFi Locations",
        "icon": "mdi:map-marker-multiple",
        "unit": "locations",
        "device_class": None,
    },
}