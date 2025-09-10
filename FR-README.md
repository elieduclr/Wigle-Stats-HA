# 📡 Wigle WiFi Network Statistics Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/elieduclr/Wigle-Stats-HACS.svg)](https://github.com/elieduclr/Wigle-Stats-HACS/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Anglais](https://img.shields.io/badge/README-Anglais-blue?style=for-the-badge)](README.md)

Une intégration Home Assistant pour récupérer les statistiques de découverte WiFi, Bluetooth et cellulaire de votre compte [Wigle.net](https://wigle.net) 🌐

## ✨ Fonctionnalités

Cette intégration vous permet de suivre vos performances de wardriving directement dans Home Assistant :

- 🏆 **Classements** : Rang global et mensuel dans la communauté Wigle
- 📶 **Réseaux WiFi** : Nombre de réseaux découverts (avec/sans coordonnées GPS)
- 📱 **Tours cellulaires** : Antennes découvertes lors de vos déplacements
- 🔵 **Appareils Bluetooth** : Devices BLE détectés avec géolocalisation
- 📍 **Géolocalisation** : Suivi des emplacements WiFi mappés
- 📈 **Évolution** : Historique des rangs et progression mensuelle
- ⏰ **Activité** : Dates de première et dernière contribution

## 🚀 Installation

### Option 1 : Installation via HACS (Recommandé)

#### 📋 Prérequis
- ✅ Home Assistant 2023.1.0 ou plus récent
- ✅ [HACS](https://hacs.xyz/) installé et configuré
- ✅ Compte [Wigle.net](https://wigle.net) avec API activée

#### 🔧 Étapes d'installation HACS

1. **📁 Ajouter le repository personnalisé :**
   - [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=elieduclr&repository=Wigle-Stats-HA&category=integration)

2. **💾 Installer l'intégration :**
   - Cliquer sur `TÉLÉCHARGER`
   - Redémarrer Home Assistant 🔄

3. **⚙️ Configuration :**
   - [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=wigle)
   - Entrer vos identifiants (voir section API ci-dessous)

### Option 2 : Installation manuelle

#### 📂 Structure des fichiers

Télécharger tous les fichiers et créer cette structure dans votre configuration Home Assistant :

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

#### 🔄 Après installation manuelle

1. **Redémarrer Home Assistant**
2. **Vider le cache du navigateur** (Ctrl+F5)
3. **Ajouter l'intégration** via `Configuration` → `Intégrations`

## 🔑 Obtenir vos identifiants API Wigle

Pour utiliser cette intégration, vous avez besoin de vos identifiants API Wigle :

1. **🌐 Connectez-vous** sur [wigle.net](https://wigle.net)
2. **👤 Accédez à votre profil** → `Account` → `API`
3. **📝 Notez vos identifiants** :
   - **API Name** : `AID54419563fgdh63hdd7d553139928ae`
   - **API Token** : `8b1614a79cbdh76b5d87cb606e29e677`

> ⚠️ **Important** : Gardez ces identifiants confidentiels !

## ⚙️ Configuration dans Home Assistant

Lors de l'ajout de l'intégration, vous devrez saisir :

| Champ | Valeur | Exemple |
|-------|--------|---------|
| **Username** | Votre nom d'utilisateur Wigle | `malic1tus` |
| **API Name** | Votre API Name (commence par AID) | `AID54419563fgdh63hdd7d553139928ae` |
| **API Token** | Votre token API | `8b1614a79cbdh76b5d87cb606e29e677` |

## 📊 Capteurs disponibles

L'intégration crée automatiquement **9 capteurs** avec toutes vos statistiques :

| Capteur | Description | Icône |
|---------|-------------|-------|
| `sensor.wigle_rank` | 🏆 Votre rang global | `mdi:trophy` |
| `sensor.wigle_monthly_rank` | 📅 Votre rang mensuel | `mdi:trophy-outline` |
| `sensor.wigle_wifi_networks_with_gps` | 📶 WiFi avec coordonnées GPS | `mdi:wifi` |
| `sensor.wigle_wifi_networks_discovered` | 📡 Total réseaux WiFi découverts | `mdi:wifi` |
| `sensor.wigle_cell_towers_with_gps` | 📱 Tours cellulaires avec GPS | `mdi:cellphone-nfc` |
| `sensor.wigle_cell_towers_discovered` | 🏗️ Total tours cellulaires découvertes | `mdi:cellphone-nfc` |
| `sensor.wigle_bluetooth_devices_with_gps` | 🔵 Bluetooth avec GPS | `mdi:bluetooth` |
| `sensor.wigle_bluetooth_devices_discovered` | 📻 Total appareils Bluetooth | `mdi:bluetooth` |
| `sensor.wigle_total_wifi_locations` | 📍 Total emplacements WiFi | `mdi:map-marker-multiple` |

## 📋 Attributs supplémentaires

Chaque capteur inclut des **attributs détaillés** :

### 🏆 Capteurs de rang
- `previous_rank` - Rang précédent
- `rank_change` - Évolution du rang (+ = progression, - = régression)
- `previous_month_rank` - Rang mensuel précédent
- `month_rank_change` - Évolution mensuelle

### 📊 Tous les capteurs
- `username` - Nom d'utilisateur Wigle
- `wifi_gps_percentage` - Pourcentage de WiFi avec GPS
- `first_activity` - Date de première activité (format: `YYYYMMDD-NNNNN`)
- `last_activity` - Date de dernière activité

## 🎨 Exemple de dashboard

Voici un exemple de carte Lovelace pour afficher vos statistiques :

```yaml
type: entities
title: 📡 Statistiques Wigle
entities:
  - entity: sensor.wigle_rank
    name: 🏆 Rang global
    secondary_info: attribute
    attribute: rank_change
  - entity: sensor.wigle_monthly_rank
    name: 📅 Rang mensuel
  - entity: sensor.wigle_wifi_networks_discovered
    name: 📶 Réseaux WiFi
  - entity: sensor.wigle_bluetooth_devices_discovered
    name: 🔵 Appareils Bluetooth
  - entity: sensor.wigle_cell_towers_discovered
    name: 📱 Tours cellulaires
```

## 🔄 Mise à jour des données

- **Fréquence** : Toutes les heures (les données Wigle changent peu)
- **Limite API** : Respecte les limites de taux de Wigle
- **Reconnexion automatique** : En cas d'erreur temporaire

## 🛠️ Dépannage

### ❌ Erreur d'authentification
- ✅ Vérifiez que votre **username**, **API Name** et **API Token** sont corrects
- ✅ Assurez-vous que l'**API est activée** sur votre compte Wigle
- ✅ L'**API Name** doit commencer par `AID` suivi de caractères alphanumériques
- ✅ Testez avec curl : 
  ```bash
  curl -u AID...:TOKEN... https://api.wigle.net/api/v2/profile/user
  ```

### 📊 Pas de données
- ⏰ L'intégration met à jour les données **toutes les heures**
- 🔍 Vérifiez les **logs** de Home Assistant pour les erreurs :
  ```
  Paramètres → Système → Journaux
  ```

### 🚫 Limitation de l'API
- ⚠️ Wigle limite les requêtes API par utilisateur
- ⏱️ L'intégration respecte un **intervalle d'une heure** entre mises à jour
- 🔄 Patience, les données se mettront à jour automatiquement

### 🔧 Problèmes courants

| Problème | Solution |
|----------|----------|
| Intégration ne s'affiche pas | Redémarrer HA et vider le cache navigateur |
| Erreur "cannot_connect" | Vérifier la connectivité Internet |
| Erreur "unknown" | Consulter les logs détaillés |

## 🤝 Contribution et développement

Vous souhaitez contribuer ? C'est fantastique ! 🎉

### 🔧 Environnement de développement

1. **Fork** le repository
2. **Cloner** votre fork
3. **Créer** une branche pour votre fonctionnalité
4. **Tester** avec Home Assistant
5. **Soumettre** une pull request

### 🐛 Signaler un bug

Utilisez les [GitHub Issues](https://github.com/elieduclr/Wigle-Stats-HACS/issues) avec :
- ✅ Version de Home Assistant
- ✅ Version de l'intégration
- ✅ Logs d'erreur complets
- ✅ Étapes pour reproduire

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- 🌟 [Wigle.net](https://wigle.net) pour leur formidable API
- 🏠 La communauté [Home Assistant](https://www.home-assistant.io/) 
- 📊 Tous les wardrivers qui contribuent à cartographier les réseaux !

---

**⭐ Si cette intégration vous plaît, n'hésitez pas à lui donner une étoile sur GitHub !**
