# 📡 Wigle WiFi Network Statistics Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/elieduclr/Wigle-Stats-HACS.svg)](https://github.com/elieduclr/Wigle-Stats-HACS/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Français](https://img.shields.io/badge/README-Français-blue?style=for-the-badge)](FR-README.md)

A Home Assistant integration to retrieve WiFi, Bluetooth, and cellular discovery statistics from your [Wigle.net](https://wigle.net) account 🌐

## ✨ Features

This integration allows you to track your wardriving performance directly in Home Assistant:

- 🏆 **Rankings**: Global and monthly rank in the Wigle community
- 📶 **WiFi Networks**: Number of discovered networks (with/without GPS coordinates)
- 📱 **Cell Towers**: Antennas discovered during your travels
- 🔵 **Bluetooth Devices**: BLE devices detected with geolocation
- 📍 **Geolocation**: Tracking of mapped WiFi locations
- 📈 **Evolution**: History of ranks and monthly progression
- ⏰ **Activity**: First and last contribution dates

## 🚀 Installation

### Option 1: Installation via HACS (Recommended)

#### 📋 Prerequisites
- ✅ Home Assistant 2023.1.0 or newer
- ✅ [HACS](https://hacs.xyz/) installed and configured
- ✅ [Wigle.net](https://wigle.net) account with API enabled

#### 🔧 HACS Installation Steps

1. **📁 Add custom integration:**
   - [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=elieduclr&repository=Wigle-Stats-HA&category=integration)

2. **💾 Install the integration:**
   - Click `DOWNLOAD`
   - Restart Home Assistant 🔄

3. **⚙️ Configuration:**
   - [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=wigle)
   - Enter your credentials (see API section below)

### Option 2: Manual Installation

#### 📂 File Structure

Download all files and create this structure in your Home Assistant configuration:

```
config/
└── custom_components/
    └── wigle/
        ├── translations/
        |   ├── de.json
        |   ├── es.json
        |   ├── fr.json
        |   └── it.json
        ├── __init__.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── sensor.py
        ├── strings.json
        └── wigle_api.py
```

#### 🔄 After Manual Installation

1. **Restart Home Assistant**
2. **Clear browser cache** (Ctrl+F5)
3. **Add integration** via `Settings` → `Devices & Services` → `Add Integrations`

## 🔑 Getting Your Wigle API Credentials

To use this integration, you need your Wigle API credentials:

1. **🌐 Log in** to [wigle.net](https://wigle.net)
2. **👤 Access your profile** → `Account` → `API`
3. **📝 Note your credentials**:
   - **API Name**: `AID54419563fgdh63hdd7d553139928ae`
   - **API Token**: `8b1614a79cbdh76b5d87cb606e29e677`

> ⚠️ **Important**: Keep these credentials confidential!

## ⚙️ Configuration in Home Assistant

When adding the integration, you will need to enter:

| Field | Value | Example |
|-------|-------|---------|
| **Username** | Your Wigle username | `malic1tus` |
| **API Name** | Your API Name (starts with AID) | `AID54419563fgdh63hdd7d553139928ae` |
| **API Token** | Your API token | `8b1614a79cbdh76b5d87cb606e29e677` |

## 📊 Available Sensors

The integration automatically creates **9 sensors** with all your statistics:

| Sensor | Description | Icon |
|--------|-------------|------|
| `sensor.wigle_rank` | 🏆 Your global rank | `mdi:trophy` |
| `sensor.wigle_monthly_rank` | 📅 Your monthly rank | `mdi:trophy-outline` |
| `sensor.wigle_wifi_networks_with_gps` | 📶 WiFi with GPS coordinates | `mdi:wifi` |
| `sensor.wigle_wifi_networks_discovered` | 📡 Total WiFi networks discovered | `mdi:wifi` |
| `sensor.wigle_cell_towers_with_gps` | 📱 Cell towers with GPS | `mdi:cellphone-nfc` |
| `sensor.wigle_cell_towers_discovered` | 🏗️ Total cell towers discovered | `mdi:cellphone-nfc` |
| `sensor.wigle_bluetooth_devices_with_gps` | 🔵 Bluetooth with GPS | `mdi:bluetooth` |
| `sensor.wigle_bluetooth_devices_discovered` | 📻 Total Bluetooth devices | `mdi:bluetooth` |
| `sensor.wigle_total_wifi_locations` | 📍 Total WiFi locations | `mdi:map-marker-multiple` |

## 📋 Additional Attributes

Each sensor includes **detailed attributes**:

### 🏆 Rank Sensors
- `previous_rank` - Previous rank
- `rank_change` - Rank evolution (+ = progress, - = regression)
- `previous_month_rank` - Previous monthly rank
- `month_rank_change` - Monthly evolution

### 📊 All Sensors
- `username` - Wigle username
- `wifi_gps_percentage` - Percentage of WiFi with GPS
- `first_activity` - First activity date (format: `YYYYMMDD-NNNNN`)
- `last_activity` - Last activity date

## 🎨 Dashboard Example

Here's an example Lovelace card to display your statistics:

```yaml
type: entities
title: 📡 Wigle Statistics
entities:
  - entity: sensor.wigle_rank
    name: 🏆 Global Rank
    secondary_info: attribute
    attribute: rank_change
  - entity: sensor.wigle_monthly_rank
    name: 📅 Monthly Rank
  - entity: sensor.wigle_wifi_networks_discovered
    name: 📶 WiFi Networks
  - entity: sensor.wigle_bluetooth_devices_discovered
    name: 🔵 Bluetooth Devices
  - entity: sensor.wigle_cell_towers_discovered
    name: 📱 Cell Towers
```

## 🔄 Data Updates

- **Frequency**: Every hour (Wigle data changes slowly)
- **API Limits**: Respects Wigle rate limits
- **Auto-reconnection**: In case of temporary errors

## 🛠️ Troubleshooting

### ❌ Authentication Error
- ✅ Check that your **username**, **API Name**, and **API Token** are correct
- ✅ Make sure **API is enabled** on your Wigle account
- ✅ The **API Name** must start with `AID` followed by alphanumeric characters
- ✅ Test with curl:
  ```bash
  curl -u AID...:TOKEN... https://api.wigle.net/api/v2/profile/user
  ```

### 📊 No Data
- ⏰ The integration updates data **every hour**
- 🔍 Check Home Assistant **logs** for errors:
  ```
  Settings → System → Logs
  ```

### 🚫 API Rate Limiting
- ⚠️ Wigle limits API requests per user
- ⏱️ The integration respects a **one-hour interval** between updates
- 🔄 Be patient, data will update automatically

### 🔧 Common Issues

| Problem | Solution |
|---------|----------|
| Integration doesn't show up | Restart HA and clear browser cache |
| "cannot_connect" error | Check Internet connectivity |
| "unknown" error | Check detailed logs |

## 🤝 Contribution and Development

Want to contribute? That's fantastic! 🎉

### 🔧 Development Environment

1. **Fork** the repository
2. **Clone** your fork
3. **Create** a branch for your feature
4. **Test** with Home Assistant
5. **Submit** a pull request

### 🐛 Report a Bug

Use [GitHub Issues](https://github.com/elieduclr/Wigle-Stats-HACS/issues) with:
- ✅ Home Assistant version
- ✅ Integration version
- ✅ Complete error logs
- ✅ Steps to reproduce

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🌟 [Wigle.net](https://wigle.net) for their fantastic API
- 🏠 The [Home Assistant](https://www.home-assistant.io/) community
- 📊 All wardrivers who contribute to mapping networks!

---

**⭐ If you like this integration, feel free to give it a star on GitHub!**
