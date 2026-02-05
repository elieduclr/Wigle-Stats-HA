# 📡 Intégration Wigle WiFi Network Statistics pour Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/malicaeus/Wigle-Stats-HA.svg)](https://github.com/malicaeus/Wigle-Stats-HA/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![English](https://img.shields.io/badge/README-English-blue?style=for-the-badge)](https://github.com/malicaeus/Wigle-Stats-HA/blob/main/README.md)

Une intégration complète pour Home Assistant permettant de récupérer les statistiques de découverte WiFi, Bluetooth et cellulaire de votre compte [Wigle.net](https://wigle.net) avec des fonctionnalités avancées et une surveillance intelligente 🌐

## ✨ Fonctionnalités

Cette intégration vous permet de suivre vos performances de wardriving directement dans Home Assistant avec des capacités de surveillance avancées :

### 📊 Statistiques de base
- 🏆 **Classements** : Rang global et mensuel dans la communauté Wigle
- 📶 **Réseaux WiFi** : Nombre de réseaux découverts (avec/sans coordonnées GPS)
- 📱 **Tours cellulaires** : Antennes découvertes lors de vos déplacements
- 🔵 **Appareils Bluetooth** : Devices BLE détectés avec géolocalisation
- 📍 **Géolocalisation** : Suivi des emplacements WiFi mappés
- 📈 **Évolution** : Historique des rangs et progression mensuelle
- ⏰ **Activité** : Dates de première et dernière contribution

### 🎯 Surveillance intelligente
- 🔔 **Suivi d'activité** : Surveillance du statut d'activité hebdomadaire et mensuelle
- 📈 **Gestion des objectifs** : Définition et suivi des objectifs de classement avec indicateurs de progression
- 🎖️ **Statut de performance** : Détection automatique du statut de top performer
- 📅 **Analyse de tendance** : Suivi des améliorations de rang et de progression des objectifs
- ⚙️ **Configuration flexible** : Intervalles de mise à jour et sélection de capteurs personnalisables

### 🛠️ Fonctionnalités avancées
- 🔄 **Gestion d'erreur robuste** : Retry automatique avec backoff intelligent
- 📡 **Cache intelligent** : Maintient les dernières données connues pendant les pannes temporaires
- ⏱️ **Limitation de taux** : Respecte les limites API avec gestion intelligente des requêtes
- 🎛️ **Services personnalisés** : Mises à jour manuelles et configuration d'objectifs via services

## 🚀 Installation

### Option 1 : Installation via HACS (Recommandée)

#### 📋 Prérequis
- ✅ Home Assistant 2023.1.0 ou plus récent
- ✅ [HACS](https://hacs.xyz/) installé et configuré
- ✅ Compte [Wigle.net](https://wigle.net) avec API activée

#### 🔧 Étapes d'installation HACS

1. **📁 Ajouter l'intégration personnalisée :**
   - [![Ouvrir votre instance Home Assistant et ouvrir un dépôt dans le Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=malicaeus&repository=Wigle-Stats-HA&category=integration)

2. **💾 Installer l'intégration :**
   - Cliquer sur `TÉLÉCHARGER`
   - Redémarrer Home Assistant 🔄

3. **⚙️ Configuration :**
   - [![Ouvrir votre instance Home Assistant et commencer la configuration d'une nouvelle intégration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=wigle)
   - Entrer vos identifiants (voir section API ci-dessous)

### Option 2 : Installation manuelle

#### 📂 Structure des fichiers

Téléchargez tous les fichiers et créez cette structure dans votre configuration Home Assistant :

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

#### 🔄 Après installation manuelle

1. **Redémarrer Home Assistant**
2. **Vider le cache du navigateur** (Ctrl+F5)
3. **Ajouter l'intégration** via `Paramètres` → `Appareils et Services` → `Ajouter une intégration`

## 🔑 Obtenir vos identifiants API Wigle

Pour utiliser cette intégration, vous avez besoin de vos identifiants API Wigle :

1. **🌐 Connectez-vous** sur [wigle.net](https://wigle.net)
2. **👤 Accédez à votre profil** → `Account` → `API`
3. **📝 Notez vos identifiants** :
   - **API Name** : `AID54419563fgdh63hdd7d553139928ae`
   - **API Token** : `8b1614a79cbdh76b5d87cb606e29e677`

> ⚠️ **Important** : Gardez ces identifiants confidentiels !

## ⚙️ Configuration dans Home Assistant

### Configuration initiale

Lors de l'ajout de l'intégration, vous devrez saisir :

| Champ | Valeur | Exemple |
|-------|--------|---------|
| **Nom d'utilisateur** | Votre nom d'utilisateur Wigle | `malic1tus` |
| **API Name** | Votre API Name (commence par AID) | `AID54419563fgdh63hdd7d553139928ae` |
| **API Token** | Votre token API | `8b1614a79cbdh76b5d87cb606e29e677` |

### Options avancées

Après la configuration initiale, vous pouvez configurer les options avancées via `Paramètres` → `Appareils et Services` → `Wigle` → `Configurer` :

| Option | Description | Défaut | Plage |
|--------|-------------|--------|-------|
| **Intervalle de mise à jour** | Fréquence de récupération des données (minutes) | 60 | 30-1440 |
| **Objectif de rang** | Rang global cible (0 = désactivé) | 0 | 0-999999 |
| **Objectif de rang mensuel** | Rang mensuel cible (0 = désactivé) | 0 | 0-99999 |
| **Capteurs activés** | Sélectionner les capteurs à créer | Tous | Personnalisable |
| **Notifications** | Activer les notifications de changement de rang | Non | Oui/Non |
| **Seuil de notification** | Changement de rang minimum pour alertes | 100 | 1+ |

## 📊 Entités disponibles

### Capteurs réguliers (9 au total)

L'intégration crée automatiquement des capteurs avec toutes vos statistiques :

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

### Capteurs binaires (6 au total)

Indicateurs de statut intelligents pour l'activité et le suivi des objectifs :

| Capteur binaire | Description | Icône |
|-----------------|-------------|-------|
| `binary_sensor.wigle_active_this_month` | 📅 Actif ce mois-ci | `mdi:calendar-check` |
| `binary_sensor.wigle_active_this_week` | 🗓️ Actif cette semaine | `mdi:calendar-week` |
| `binary_sensor.wigle_rank_improved` | 📈 Rang significativement amélioré | `mdi:trending-up` |
| `binary_sensor.wigle_goal_reached` | 🎯 Objectif de rang global atteint | `mdi:target` |
| `binary_sensor.wigle_top_performer` | 🏅 Statut de top performer | `mdi:medal` |
| `binary_sensor.wigle_monthly_goal_on_track` | 📊 Objectif mensuel en bonne voie | `mdi:chart-line` |

## 📋 Attributs des entités

### 🏆 Capteurs de rang
- `previous_rank` - Rang précédent
- `rank_change` - Évolution du rang (+ = progression, - = régression)
- `previous_month_rank` - Rang mensuel précédent
- `month_rank_change` - Évolution mensuelle
- `rank_improvement` - Valeur d'amélioration calculée
- `rank_improvement_percentage` - Amélioration en pourcentage

### 📊 Tous les capteurs
- `username` - Nom d'utilisateur Wigle
- `wifi_gps_percentage` - Pourcentage de WiFi avec GPS
- `first_activity` - Date de première activité (format: `YYYYMMDD-NNNNN`)
- `last_activity` - Date de dernière activité

### 🔔 Attributs des capteurs binaires
- **Capteurs d'activité** : `days_since_last_activity`, dates d'activité
- **Capteurs d'objectifs** : `distance_to_goal`, valeurs actuelles vs cibles
- **Capteurs de performance** : seuils de classement et détails de statut

## 🛠️ Services

L'intégration fournit des services personnalisés pour un contrôle avancé :

### `wigle.force_update`
Forcer une mise à jour immédiate des données pour un utilisateur spécifique.

```yaml
service: wigle.force_update
data:
  username: "votre_nom_utilisateur"
```

### `wigle.set_rank_goal`
Définir des objectifs de classement pour un utilisateur.

```yaml
service: wigle.set_rank_goal
data:
  username: "votre_nom_utilisateur"
  goal: 1000              # Objectif de rang global
  monthly_goal: 50        # Objectif de rang mensuel (optionnel)
```

### `wigle.reset_statistics`
Réinitialiser les statistiques en cache et forcer la récupération de données fraîches.

```yaml
service: wigle.reset_statistics
data:
  username: "votre_nom_utilisateur"
```

## 🎨 Exemples de tableau de bord

### Carte de statistiques de base

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

### Carte Activité et Objectifs

```yaml
type: entities
title: 🎯 Activité et Objectifs
entities:
  - entity: binary_sensor.wigle_active_this_week
    name: 📅 Actif cette semaine
  - entity: binary_sensor.wigle_active_this_month
    name: 🗓️ Actif ce mois-ci
  - entity: binary_sensor.wigle_rank_improved
    name: 📈 Rang amélioré
  - entity: binary_sensor.wigle_goal_reached
    name: 🎯 Objectif atteint
  - entity: binary_sensor.wigle_top_performer
    name: 🏅 Top performer
```

### Tableau de bord avancé avec cartes conditionnelles

```yaml
type: conditional
conditions:
  - entity: binary_sensor.wigle_goal_reached
    state: "on"
card:
  type: markdown
  content: |
    ## 🎉 Félicitations !
    Vous avez atteint votre objectif de classement !
```

## 🔄 Mises à jour des données et performances

- **Fréquence par défaut** : Toutes les heures (configurable de 30 minutes à 24 heures)
- **Retry intelligent** : Retry automatique avec backoff exponentiel en cas d'échec
- **Limitation de taux** : Gestion intelligente des requêtes respectant les limites API
- **Cache** : Maintient les dernières données connues pendant les problèmes API temporaires
- **Récupération d'erreur** : Dégradation gracieuse et récupération automatique

## 🛠️ Dépannage

### ❌ Erreur d'authentification
- ✅ Vérifiez que votre **nom d'utilisateur**, **API Name** et **API Token** sont corrects
- ✅ Assurez-vous que l'**API est activée** sur votre compte Wigle
- ✅ L'**API Name** doit commencer par `AID` suivi de caractères alphanumériques
- ✅ Testez avec curl :
  ```bash
  curl -u AID...:TOKEN... https://api.wigle.net/api/v2/profile/user
  ```

### 📊 Pas de données ou données obsolètes
- ⏰ Vérifiez l'**intervalle de mise à jour** configuré dans les options d'intégration
- 🔄 Utilisez le service `wigle.force_update` pour déclencher une actualisation immédiate
- 🔍 Vérifiez les **logs** de Home Assistant pour les erreurs :
  ```
  Paramètres → Système → Journaux → Filtrer par "wigle"
  ```
- 🗑️ Essayez le service `wigle.reset_statistics` pour vider le cache

### 🚫 Limitation de l'API
- ⚠️ Wigle limite les requêtes API par utilisateur (100/heure)
- ⏱️ L'intégration respecte automatiquement les limites de taux
- 📊 Vérifiez les attributs d'entité pour `_consecutive_errors` pour surveiller les problèmes
- 🔄 Augmentez l'intervalle de mise à jour si vous avez plusieurs instances

### 🔧 Problèmes courants

| Problème | Solution |
|----------|----------|
| Les capteurs binaires n'apparaissent pas | Vérifiez les capteurs activés dans les options d'intégration |
| Les objectifs ne fonctionnent pas | Vérifiez que les valeurs d'objectif sont définies dans les options (pas 0) |
| Services non disponibles | Redémarrez Home Assistant après l'installation |
| Erreur "cannot_connect" | Vérifiez la connectivité Internet et les identifiants API |
| Les entités affichent "unknown" | Vérifiez les logs détaillés pour les erreurs API |

### 🐛 Mode debug

Activez la journalisation de debug pour un dépannage détaillé :

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.wigle: debug
```

## 🚀 Usage avancé

### Exemples d'automatisations

#### Notification d'amélioration de rang

```yaml
automation:
  - alias: "Amélioration rang Wigle"
    trigger:
      - platform: state
        entity_id: binary_sensor.wigle_rank_improved
        to: "on"
    action:
      - service: notify.mobile_app
        data:
          message: "🎉 Votre rang Wigle s'est amélioré de {{ state_attr('sensor.wigle_rank', 'rank_improvement') }} positions !"
```

#### Rappel d'activité hebdomadaire

```yaml
automation:
  - alias: "Rappel activité Wigle hebdomadaire"
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
          message: "📡 Vous n'avez pas fait de wardriving cette semaine. Il est temps de prendre la route !"
```

### Capteurs template

Créez des capteurs personnalisés pour des métriques spécifiques :

```yaml
# configuration.yaml
template:
  - sensor:
      - name: "Taux de découverte Wigle"
        state: >
          {% set wifi = states('sensor.wigle_wifi_networks_discovered') | int %}
          {% set days = (now() - states.sensor.wigle_rank.attributes.first_activity | as_datetime).days %}
          {{ (wifi / days) | round(1) if days > 0 else 0 }}
        unit_of_measurement: "réseaux/jour"
```

## 🌍 Internationalisation

L'intégration supporte plusieurs langues :
- 🇺🇸 Anglais (par défaut)
- 🇫🇷 Français
- 🇩🇪 Allemand
- 🇪🇸 Espagnol
- 🇮🇹 Italien
- 🇯🇵 Japonais
- 🇰🇷 Coréen
- 🇳🇱 Néerlandais
- 🇵🇱 Polonais
- 🇧🇷 Portugais
- 🇷🇺 Russe
- 🇹🇷 Turc
- 🇨🇳 Chinois (Simplifié)
- 🇹🇼 Chinois (Traditionnel)
- 🇳🇴 Norvégien
- 🇸🇪 Suédois
- 🇩🇰 Danois
- 🇫🇮 Finnois
- 🇬🇷 Grec
- 🇷🇴 Roumain

## 🤝 Contribution et développement

Vous souhaitez contribuer ? C'est fantastique ! 🎉

### 🔧 Environnement de développement

1. **Fork** le repository
2. **Cloner** votre fork
3. **Créer** une branche pour votre fonctionnalité
4. **Tester** avec Home Assistant
5. **Soumettre** une pull request

### 🐛 Signaler un bug

Utilisez les [GitHub Issues](https://github.com/malicaeus/Wigle-Stats-HA/issues) avec :
- ✅ Version de Home Assistant
- ✅ Version de l'intégration
- ✅ Logs d'erreur complets (avec debug activé)
- ✅ Étapes pour reproduire
- ✅ Détails de configuration (nettoyés)

### 💡 Demandes de fonctionnalités

Nous accueillons les demandes de fonctionnalités ! Veuillez inclure :
- Description claire de la fonctionnalité
- Cas d'usage et avantages
- Idées d'implémentation potentielles

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- 🌟 [Wigle.net](https://wigle.net) pour leur formidable API et communauté de wardriving
- 🏠 La communauté [Home Assistant](https://www.home-assistant.io/) pour l'inspiration et le soutien
- 📊 Tous les wardrivers qui contribuent à cartographier les réseaux sans fil dans le monde entier
- 🛠️ Les contributeurs et testeurs qui aident à améliorer cette intégration

## 📈 Journal des modifications

### Version 2.2.0 (Développement)
- ✨ **Nouveau** : Type hints complets pour tous les modules Python
- ✨ **Nouveau** : Docstrings complètes pour toutes les classes et méthodes
- 🔧 **Amélioré** : Maintenabilité du code et support des IDE

### Version 2.1.1 (Stable actuelle)
- 🔧 **Fixe** : [Issue 4](https://github.com/malicaeus/Wigle-Stats-HA/issues/4) - Correction de la gestion des erreurs dans certains cas limites
- 🔧 **Amélioré** : Améliorations de stabilité dans la mise en cache des données
- 🔧 **Amélioré** : Journalisation des erreurs renforcée pour le dépannage

### Version 2.1.0
- ✨ **Nouveau** : Support linguistique étendu (7 langues supplémentaires)
  - 🇨🇳 Chinois (Traditionnel), 🇳🇴 Norvégien, 🇸🇪 Suédois
  - 🇩🇰 Danois, 🇫🇮 Finnois, 🇬🇷 Grec, 🇷🇴 Roumain
- 🌍 **Enrichi** : Support multi-langues couvrant désormais 20 langues
- 🔧 **Amélioré** : Gestion des clés de traduction

### Version 2.0.0
- ✨ **Nouveau** : Capteurs binaires pour le suivi d'activité et d'objectifs
  - Indicateurs d'activité mensuelle/hebdomadaire
  - Détection d'amélioration de rang
  - Suivi de réalisation d'objectifs
  - Statut de top performer
  - Progression des objectifs mensuels
- ✨ **Nouveau** : Options de configuration avancées
  - Intervalles de mise à jour personnalisables
  - Définition et suivi des objectifs de rang
  - Sélection et filtrage des capteurs
  - Configuration du seuil de notification
- ✨ **Nouveau** : Services personnalisés pour le contrôle manuel
  - `wigle.force_update` - Actualisation immédiate des données
  - `wigle.set_rank_goal` - Mise à jour des objectifs de classement
  - `wigle.reset_statistics` - Effacement du cache et rechargement
- ✨ **Nouveau** : Cache intelligent et récupération d'erreur
  - Retry automatique avec backoff exponentiel
  - Persistance des dernières données connues
  - Dégradation gracieuse en cas d'erreur API
- ✨ **Nouveau** : Support multi-langues (13 langues)
  - Anglais, Français, Allemand, Espagnol, Italien, Japonais, Coréen
  - Néerlandais, Polonais, Portugais, Russe, Turc, Chinois (Simplifié)
- 🔧 **Amélioré** : Client API robuste avec logique de retry
  - Gestion des limites de taux
  - Détection des erreurs d'authentification
  - Gestion des timeouts de connexion
  - Backoff exponentiel en cas d'échec
- 🔧 **Amélioré** : Meilleure gestion d'erreur et diagnostics
  - Journalisation détaillée des erreurs
  - Support du mode débogage
  - Suivi des erreurs consécutives
- 🔧 **Enrichi** : Attributs d'entité riches et indicateurs de statut
  - Suivi des rangs précédents
  - Calculs de changement de rang
  - Suivi des dates d'activité
  - Distance à l'objectif
  - Métriques de performance

### Version 1.x.x
- 📊 Support des capteurs de base pour les statistiques WiFi, cellulaires et Bluetooth
- 🔐 Authentification API avec gestion des credentials
- 📈 Suivi des rangs et statistiques
- 🌐 Intégration initiale à Home Assistant

---

**⭐ Si cette intégration vous plaît, n'hésitez pas à lui donner une étoile sur GitHub !**

---

*Cette intégration n'est pas affiliée à ou approuvée par Wigle.net. Wigle est une marque de leurs propriétaires respectifs.*