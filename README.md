# Wigle WiFi Network Statistics Integration for Home Assistant

Cette intégration permet de récupérer les statistiques de votre compte Wigle.net directement dans Home Assistant.

## Fonctionnalités

- **Rang global** et **rang mensuel**
- **Réseaux WiFi découverts** (avec et sans GPS)
- **Tours de téléphonie** découvertes (avec et sans GPS)  
- **Appareils Bluetooth** découverts (avec et sans GPS)
- **Total des emplacements WiFi**
- Attributs supplémentaires incluant l'évolution des rangs et les dates d'activité

## Installation via HACS

### Prérequis
- Home Assistant 2023.1.0 ou plus récent
- HACS installé
- Compte Wigle.net avec API activée

### Étapes d'installation

1. **Ajouter le repository personnalisé dans HACS :**
   - Aller dans HACS → Intégrations
   - Cliquer sur les trois points en haut à droite → "Custom repositories"
   - Ajouter l'URL de votre repository GitHub
   - Choisir la catégorie "Integration"

2. **Installer l'intégration :**
   - Rechercher "Wigle WiFi Network Statistics"
   - Cliquer sur "Download"
   - Redémarrer Home Assistant

3. **Configuration :**
   - Aller dans Configuration → Intégrations
   - Cliquer sur "Ajouter une intégration"
   - Rechercher "Wigle WiFi Network Statistics"
   - Entrer vos identifiants :
     - **Username** : Votre nom d'utilisateur Wigle
     - **API Key** : Votre clé API Wigle (format : AID...)

## Obtenir votre clé API Wigle

1. Connectez-vous sur [wigle.net](https://wigle.net)
2. Allez dans votre profil → "Account" → "API"
3. Copiez votre "Encoded for use" qui ressemble à : `AID5441982d0acf37424dd7d553139928ae`

## Structure des fichiers

Créer le dossier `custom_components/wigle/` dans votre configuration Home Assistant et y placer tous les fichiers Python.

```
custom_components/
└── wigle/
    ├── __init__.py
    ├── manifest.json
    ├── const.py
    ├── wigle_api.py
    ├── config_flow.py
    ├── sensor.py
    └── strings.json
```

## Capteurs disponibles

L'intégration crée automatiquement les capteurs suivants :

- `sensor.wigle_rank` - Votre rang global
- `sensor.wigle_monthly_rank` - Votre rang mensuel  
- `sensor.wigle_wifi_networks_with_gps` - Réseaux WiFi avec coordonnées GPS
- `sensor.wigle_wifi_networks_discovered` - Total réseaux WiFi découverts
- `sensor.wigle_cell_towers_with_gps` - Tours cellulaires avec GPS
- `sensor.wigle_cell_towers_discovered` - Total tours cellulaires découvertes
- `sensor.wigle_bluetooth_devices_with_gps` - Appareils Bluetooth avec GPS  
- `sensor.wigle_bluetooth_devices_discovered` - Total appareils Bluetooth découverts
- `sensor.wigle_total_wifi_locations` - Total des emplacements WiFi

## Attributs disponibles

Chaque capteur inclut des attributs supplémentaires :
- `username` - Nom d'utilisateur Wigle
- `wifi_gps_percentage` - Pourcentage de réseaux WiFi avec GPS
- `previous_rank` - Rang précédent (pour le capteur rank)
- `rank_change` - Évolution du rang 
- `first_activity` - Date de première activité
- `last_activity` - Date de dernière activité

## Dépannage

### Erreur d'authentification
- Vérifiez que votre nom d'utilisateur et clé API sont corrects
- Assurez-vous que l'API est activée sur votre compte Wigle

### Pas de données
- L'intégration met à jour les données toutes les heures
- Vérifiez les logs de Home Assistant pour les erreurs

### Limitation de l'API
- Wigle limite les requêtes API
- L'intégration respecte un intervalle d'une heure entre les mises à jour

## Développement

Pour contribuer au développement :

1. Fork le repository
2. Créer une branche pour votre fonctionnalité
3. Faire vos modifications
4. Tester avec Home Assistant
5. Soumettre une pull request

## Licence

Ce projet est sous licence MIT.