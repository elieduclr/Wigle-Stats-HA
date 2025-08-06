
# 📡 Wigle Stats for Home Assistant

A custom Home Assistant integration to fetch and display your **Wigle.net user statistics**, including WiFi, Bluetooth, and cellular discoveries, as well as global and monthly rank.

> 🔐 Requires your Wigle.net API credentials (API name and API token).

---

## ✨ Features

- ✅ Displays total discovered WiFi, Bluetooth, and cell networks
- 📊 Tracks global and monthly rank
- 🕓 Automatic refresh (every 12 hours by default)
- 🌍 Available as a HACS custom integration
- 🛠️ Easy to use, minimal setup required

---

## 🚀 Installation (via HACS)

1. Open Home Assistant
2. Go to **HACS → Integrations → 3-dot menu → Custom repositories**
3. Add this repo:  ```https://github.com/elieduclr/Wigle-Stats-HACS``` as an **Integration**
4. Install "Wigle Stats"
5. Restart Home Assistant

---

## 🛠️ Manual Setup (YAML)

```yaml
# configuration.yaml
sensor:
  - platform: wigle_stats
    username: YOUR_WIGLE_API_NAME
    password: YOUR_WIGLE_API_TOKEN
```

🔍 Example Dashboard
You can create a Lovelace card like this:
```yaml
type: entities
title: Wigle Stats
entities:
  - entity: sensor.wigle_stats
    name: Global Rank
  - type: attribute
    entity: sensor.wigle_stats
    attribute: discoveredWiFi
    name: Discovered WiFi
  - type: attribute
    entity: sensor.wigle_stats
    attribute: discoveredBt
    name: Discovered Bluetooth Devices
  - type: attribute
    entity: sensor.wigle_stats
    attribute: monthRank
    name: Monthly Rank
```

🔒 Security Note
This integration uses Basic Authentication with your Wigle API credentials. They are transmitted over HTTPS but not encrypted in config.yaml, so be cautious when sharing files or screenshots.

📜 License
MIT License.
This project is not affiliated with Wigle.net.

🤝 Contributing
Feel free to fork, improve, and submit PRs!
If you find bugs or want to suggest features, open an issue.

📧 Author
Made with 🖤 by elieduclr
Follow my cyberpunk / ethical hacking journey.