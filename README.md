# 📡 Wigle WiFi Network Statistics Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/elieduclr/Wigle-Stats-HACS.svg)](https://github.com/elieduclr/Wigle-Stats-HACS/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Français](https://img.shields.io/badge/README-Français-blue?style=for-the-badge)]([FR-README.md](https://github.com/elieduclr/Wigle-Stats-HA/blob/main/FR-README.md))

A comprehensive Home Assistant integration to retrieve WiFi, Bluetooth, and cellular discovery statistics from your [Wigle.net](https://wigle.net) account with advanced features and smart monitoring 🌐

## ✨ Features

This integration allows you to track your wardriving performance directly in Home Assistant with advanced monitoring capabilities:

### 📊 Core Statistics
- 🏆 **Rankings**: Global and monthly rank in the Wigle community
- 📶 **WiFi Networks**: Number of discovered networks (with/without GPS coordinates)
- 📱 **Cell Towers**: Antennas discovered during your travels
- 🔵 **Bluetooth Devices**: BLE devices detected with geolocation
- 📍 **Geolocation**: Tracking of mapped WiFi locations
- 📈 **Evolution**: History of ranks and monthly progression
- ⏰ **Activity**: First and last contribution dates

### 🎯 Smart Monitoring
- 🔔 **Activity Tracking**: Monitor weekly and monthly activity status
- 📈 **Goal Management**: Set and track ranking goals with progress indicators
- 🎖️ **Performance Status**: Automatic detection of top performer status
- 📅 **Trend Analysis**: Track rank improvements and goal progress
- ⚙️ **Flexible Configuration**: Customizable update intervals and sensor selection

### 🛠️ Advanced Features
- 🔄 **Robust Error Handling**: Automatic retry with intelligent backoff
- 📡 **Smart Caching**: Maintains last known data during temporary outages
- ⏱️ **Rate Limiting**: Respects API limits with intelligent request management
- 🎛️ **Custom Services**: Manual updates and goal configuration via services

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
        |   ├── ar.json
        |   ├── da.json
        |   ├── de.json
        |   ├── el.json
        |   ├── es.json
        |   ├── fi.json
        |   ├── fr.json
        |   ├── it.json
        |   ├── ja.json
        |   ├── ko.json
        |   ├── nb.json
        |   ├── nl.json
        |   ├── pl.json
        |   ├── pt.json
        |   ├── ro.json
        |   ├── ru.json
        |   ├── sv.json
        |   ├── tr.json
        |   ├── zh-Hans.json
        |   └── zh-Hant.json
        ├── __init__.py
        ├── binary_sensor.py
        ├── config_flow.py
        ├── const.py
        ├── manifest.json
        ├── sensor.py
        ├── services.yaml
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

### Initial Setup

When adding the integration, you will need to enter:

| Field | Value | Example |
|-------|-------|---------|
| **Username** | Your Wigle username | `malic1tus` |
| **API Name** | Your API Name (starts with AID) | `AID54419563fgdh63hdd7d553139928ae` |
| **API Token** | Your API token | `8b1614a79cbdh76b5d87cb606e29e677` |

### Advanced Options

After initial setup, you can configure advanced options via `Settings` → `Devices & Services` → `Wigle` → `Configure`:

| Option | Description | Default | Range |
|--------|-------------|---------|-------|
| **Update Interval** | How often to fetch new data (minutes) | 60 | 30-1440 |
| **Rank Goal** | Target global rank (0 = disabled) | 0 | 0-999999 |
| **Monthly Rank Goal** | Target monthly rank (0 = disabled) | 0 | 0-99999 |
| **Enabled Sensors** | Select which sensors to create | All | Customizable |
| **Notifications** | Enable rank change notifications | No | Yes/No |
| **Notification Threshold** | Minimum rank change for alerts | 100 | 1+ |

## 📊 Available Entities

### Regular Sensors (9 total)

The integration automatically creates sensors with all your statistics:

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

### Binary Sensors (6 total)

Smart status indicators for activity and goal tracking:

| Binary Sensor | Description | Icon |
|---------------|-------------|------|
| `binary_sensor.wigle_active_this_month` | 📅 Active this month | `mdi:calendar-check` |
| `binary_sensor.wigle_active_this_week` | 🗓️ Active this week | `mdi:calendar-week` |
| `binary_sensor.wigle_rank_improved` | 📈 Rank significantly improved | `mdi:trending-up` |
| `binary_sensor.wigle_goal_reached` | 🎯 Global rank goal reached | `mdi:target` |
| `binary_sensor.wigle_top_performer` | 🏅 Top performer status | `mdi:medal` |
| `binary_sensor.wigle_monthly_goal_on_track` | 📊 Monthly goal on track | `mdi:chart-line` |

## 📋 Entity Attributes

### 🏆 Rank Sensors
- `previous_rank` - Previous rank
- `rank_change` - Rank evolution (+ = progress, - = regression)
- `previous_month_rank` - Previous monthly rank
- `month_rank_change` - Monthly evolution
- `rank_improvement` - Calculated improvement value
- `rank_improvement_percentage` - Improvement as percentage

### 📊 All Sensors
- `username` - Wigle username
- `wifi_gps_percentage` - Percentage of WiFi with GPS
- `first_activity` - First activity date (format: `YYYYMMDD-NNNNN`)
- `last_activity` - Last activity date

### 🔔 Binary Sensor Attributes
- **Activity sensors**: `days_since_last_activity`, activity dates
- **Goal sensors**: `distance_to_goal`, current vs target values
- **Performance sensors**: ranking thresholds and status details

## 🛠️ Services

The integration provides custom services for advanced control:

### `wigle.force_update`
Force an immediate update of data for a specific user.

```yaml
service: wigle.force_update
data:
  username: "your_username"
```

### `wigle.set_rank_goal`
Set ranking goals for a user.

```yaml
service: wigle.set_rank_goal
data:
  username: "your_username"
  goal: 1000              # Global rank goal
  monthly_goal: 50        # Monthly rank goal (optional)
```

### `wigle.reset_statistics`
Reset cached statistics and force fresh data retrieval.

```yaml
service: wigle.reset_statistics
data:
  username: "your_username"
```

## 🎨 Dashboard Examples

### Basic Statistics Card

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

### Activity & Goals Card

```yaml
type: entities
title: 🎯 Activity & Goals
entities:
  - entity: binary_sensor.wigle_active_this_week
    name: 📅 Active This Week
  - entity: binary_sensor.wigle_active_this_month
    name: 🗓️ Active This Month
  - entity: binary_sensor.wigle_rank_improved
    name: 📈 Rank Improved
  - entity: binary_sensor.wigle_goal_reached
    name: 🎯 Goal Reached
  - entity: binary_sensor.wigle_top_performer
    name: 🏅 Top Performer
```

### Advanced Dashboard with Conditional Cards

```yaml
type: conditional
conditions:
  - entity: binary_sensor.wigle_goal_reached
    state: "on"
card:
  type: markdown
  content: |
    ## 🎉 Congratulations!
    You've reached your ranking goal!
```

## 🔄 Data Updates & Performance

- **Default Frequency**: Every hour (configurable from 30 minutes to 24 hours)
- **Smart Retry**: Automatic retry with exponential backoff on failures
- **Rate Limiting**: Intelligent request management respecting API limits
- **Caching**: Maintains last known data during temporary API issues
- **Error Recovery**: Graceful degradation and automatic recovery

## 🛠️ Troubleshooting

### ❌ Authentication Error
- ✅ Check that your **username**, **API Name**, and **API Token** are correct
- ✅ Make sure **API is enabled** on your Wigle account
- ✅ The **API Name** must start with `AID` followed by alphanumeric characters
- ✅ Test with curl:
  ```bash
  curl -u AID...:TOKEN... https://api.wigle.net/api/v2/profile/user
  ```

### 📊 No Data or Stale Data
- ⏰ Check the configured **update interval** in integration options
- 🔄 Use the `wigle.force_update` service to trigger immediate refresh
- 🔍 Check Home Assistant **logs** for errors:
  ```
  Settings → System → Logs → Filter by "wigle"
  ```
- 🗑️ Try the `wigle.reset_statistics` service to clear cache

### 🚫 API Rate Limiting
- ⚠️ Wigle limits API requests per user (100/hour)
- ⏱️ The integration automatically respects rate limits
- 📊 Check entity attributes for `_consecutive_errors` to monitor issues
- 🔄 Increase update interval if you have multiple instances

### 🔧 Common Issues

| Problem | Solution |
|---------|----------|
| Binary sensors not appearing | Check enabled sensors in integration options |
| Goals not working | Verify goal values are set in options (not 0) |
| Services not available | Restart Home Assistant after installation |
| "cannot_connect" error | Check Internet connectivity and API credentials |
| Entities show "unknown" | Check detailed logs for API errors |

### 🐛 Debug Mode

Enable debug logging for detailed troubleshooting:

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.wigle: debug
```

## 🚀 Advanced Usage

### Automations Examples

#### Rank Improvement Notification

```yaml
automation:
  - alias: "Wigle Rank Improved"
    trigger:
      - platform: state
        entity_id: binary_sensor.wigle_rank_improved
        to: "on"
    action:
      - service: notify.mobile_app
        data:
          message: "🎉 Your Wigle rank improved by {{ state_attr('sensor.wigle_rank', 'rank_improvement') }} positions!"
```

#### Weekly Activity Reminder

```yaml
automation:
  - alias: "Weekly Wigle Activity Reminder"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: time
        weekday: ["sun"]
      - condition: state
        entity_id: binary_sensor.wigle_active_this_week
        state: "off"
    action:
      - service: notify.persistent_notification
        data:
          message: "📡 You haven't been wardriving this week. Time to hit the road!"
```

### Template Sensors

Create custom sensors for specific metrics:

```yaml
# configuration.yaml
template:
  - sensor:
      - name: "Wigle Discovery Rate"
        state: >
          {% set wifi = states('sensor.wigle_wifi_networks_discovered') | int %}
          {% set days = (now() - states.sensor.wigle_rank.attributes.first_activity | as_datetime).days %}
          {{ (wifi / days) | round(1) if days > 0 else 0 }}
        unit_of_measurement: "networks/day"
```

## 🌍 Internationalization

The integration supports multiple languages:
- 🇺🇸 English (default)
- 🇫🇷 French
- 🇩🇪 German
- 🇪🇸 Spanish
- 🇮🇹 Italian
- 🇯🇵 Japanese
- 🇰🇷 Korean
- 🇳🇱 Dutch
- 🇵🇱 Polish
- 🇧🇷 Portuguese
- 🇷🇺 Russian
- 🇹🇷 Turkish
- 🇨🇳 Chinese (Simplified)
- 🇹🇼 Chinese (Traditional)
- 🇳🇴 Norwegian
- 🇸🇪 Swedish
- 🇩🇰 Danish
- 🇫🇮 Finnish
- 🇬🇷 Greek
- 🇷🇴 Romanian

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
- ✅ Complete error logs (with debug enabled)
- ✅ Steps to reproduce
- ✅ Configuration details (sanitized)

### 💡 Feature Requests

We welcome feature requests! Please include:
- Clear description of the feature
- Use case and benefits
- Potential implementation ideas

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🌟 [Wigle.net](https://wigle.net) for their fantastic API and wardriving community
- 🏠 The [Home Assistant](https://www.home-assistant.io/) community for inspiration and support
- 📊 All wardrivers who contribute to mapping wireless networks worldwide
- 🛠️ Contributors and testers who help improve this integration

## 📈 Changelog

### Version 2.1.0 (Latest)
- ✨ **New**: Extended language support (7 additional languages)
  - Chinese (Traditional), Norwegian, Swedish, Danish, Finnish, Greek, and Romanian
- 🌍 **Enhanced**: Multi-language support now covers 20 languages

### Version 2.0.0
- ✨ **New**: Binary sensors for activity and goal tracking
- ✨ **New**: Advanced configuration options
- ✨ **New**: Custom services for manual control
- ✨ **New**: Smart caching and error recovery
- ✨ **New**: Multi-language support (13 languages)
- 🔧 **Improved**: Robust API client with retry logic
- 🔧 **Improved**: Better error handling and diagnostics
- 🔧 **Enhanced**: Rich entity attributes and status indicators

### Version 1.x.x
- 📊 Basic sensor support
- 🔐 API authentication
- 📈 Rank and statistics tracking

---

**⭐ If you like this integration, feel free to give it a star on GitHub!**

---

*This integration is not affiliated with or endorsed by Wigle.net. Wigle is a trademark of their respective owners.*