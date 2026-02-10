# DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
## APPLICATION GÉOLOCALISATION IP

**Version:** 0.1.0  
**Date de création:** 09 février 2026  
**Auteur:** KAMENI TCHOUATCHEU GAETAN BRUNEL  
**Statut:** En développement  

---

## 1. IDENTIFICATION DU PROJET

### 1.1 Description générale
Application web complète de géolocalisation d'adresses IP utilisant une architecture microservices composée de :
- **Frontend:** Interface utilisateur NiceGUI
- **Backend:** API FastAPI
- **Service externe:** API CIRCL (ip.circl.lu)

### 1.2 Objectifs
- Fournir une interface graphique intuitive pour localiser une adresse IP
- Intégrer l'API CIRCL pour récupérer les données de géolocalisation
- Afficher les résultats sur une carte OpenStreetMap
- Gérer les erreurs de connexion et les timeouts

### 1.3 Portée fonctionnelle
- Recherche géolocalisation par adresse IP
- Affichage des résultats en interface graphique
- Intégration cartographique (OpenStreetMap)
- Gestion de la configuration serveur (hostname, port)
- Support CORS pour requêtes cross-origin

---

## 2. ARCHITECTURE SYSTÈME

### 2.1 Schéma architectural

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE COMPLÈTE                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐         ┌──────────────────┐          │
│  │   NiceGUI UI    │         │   FastAPI Proxy  │          │
│  │   Client.py     │────────▶│   Webserv.py     │          │
│  │  Port: 8080     │         │   Port: 8000     │          │
│  └─────────────────┘         └────────┬─────────┘          │
│                                        │                     │
│                                        │ HTTPS               │
│                                        ▼                     │
│                              ┌──────────────────┐          │
│                              │  CIRCL API       │          │
│                              │ ip.circl.lu      │          │
│                              └──────────────────┘          │
│                                                               │
│  ┌─────────────────┐         ┌──────────────────┐          │
│  │   OpenStreetMap │◀────────│   Webbrowser     │          │
│  │   Intégration   │         │   External Link  │          │
│  └─────────────────┘         └──────────────────┘          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Composants techniques

#### Backend (webserv.py)
- **Framework:** FastAPI ^0.109.0
- **Serveur:** Uvicorn ^0.22.0
- **Configuration:** Pydantic Settings ^2.0.0
- **Middleware:** CORS (Cross-Origin Resource Sharing)
- **Requêtes HTTP:** Requests ^2.31.0

#### Frontend (client.py)
- **Framework:** NiceGUI ^1.4.0
- **Requêtes HTTP:** Requests ^2.31.0
- **Intégration mapping:** Webbrowser (OpenStreetMap)

#### Dépendances globales
- **Python:** ^3.12
- **Gestionnaire de paquets:** Poetry ^1.0

---

## 3. INSTALLATION ET DÉPLOIEMENT

### 3.1 Prérequis système
- **OS:** Windows, macOS, Linux
- **Python:** 3.12 ou supérieur
- **Git:** Pour la gestion de version
- **Connexion Internet:** Accès à ip.circl.lu

### 3.2 Installation des dépendances

#### Étape 1 : Installer Poetry (si non installé)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Étape 2 : Installer les dépendances du projet
```bash
poetry install
```

Cela installera :
- FastAPI 0.109.0+
- NiceGUI 1.4.0+
- Uvicorn 0.22.0+
- Requests 2.31.0+
- Pydantic Settings 2.0.0+

### 3.3 Configuration de l'environnement

#### Créer le fichier `.env` (optionnel)
```bash
cp .env.example .env
```

#### Contenu recommandé de `.env`
```
CIRCL_API_URL=https://ip.circl.lu
DEBUG=False
APP_NAME=IP Geolocation API
```

### 3.4 Vérification de l'installation
```bash
poetry run python test_nicegui.py
```

**Résultat attendu:** Un label "Hello NiceGUI!" apparaît dans le navigateur à `http://127.0.0.1:8000`

---

## 4. PROCÉDURES D'EXPLOITATION

### 4.1 Démarrage de l'application

#### Configuration recommandée : Terminal double (2 instances)

**Terminal 1 - Démarrage du serveur API**
```bash
cd C:\Users\pc\Desktop\python\python
poetry run uvicorn webserv:app --reload
```

**Sortie attendue:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Terminal 2 - Démarrage du client**
```bash
cd C:\Users\pc\Desktop\python\python
poetry run python client.py
```

**Sortie attendue:**
```
INFO:     Uvicorn running on http://127.0.0.1:8080
```

Le navigateur se lance automatiquement à `http://127.0.0.1:8080`

### 4.2 Accès aux services

| Service | URL | Description |
|---------|-----|-------------|
| API Info | `http://127.0.0.1:8000/` | Vérification de l'API |
| Geolocalisation | `http://127.0.0.1:8000/ip/{ip}` | Requête IP (remplacer {ip}) |
| Interface Web | `http://127.0.0.1:8080` | Application client NiceGUI |
| OpenStreetMap | Auto-ouverture | Carte générée automatiquement |

### 4.3 Test manuel de l'API

#### Test de la racine API
```bash
curl http://127.0.0.1:8000/
```

**Réponse:**
```json
{
  "message": "Hello from IP Geolocation API",
  "app_name": "IP Geolocation API"
}
```

#### Test de géolocalisation
```bash
curl http://127.0.0.1:8000/ip/8.8.8.8
```

**Réponse type:**
```json
{
  "ip": "8.8.8.8",
  "location": {...},
  "country": "United States",
  "city": "Mountain View"
}
```

---

## 5. FONCTIONNALITÉS DÉTAILLÉES

### 5.1 Webserv.py (Backend FastAPI)

#### Gestion de la configuration
- **Modèle Pydantic:** `Settings` pour la gestion des variables d'environnement
- **Mise en cache:** `@lru_cache()` pour optimisation des performances
- **Variables:** `app_name`, `circl_api_url`, `debug`

#### Endpoints disponibles

**1. GET /**
```
Description: Vérification de l'API
Réponse: {"message": "Hello from IP Geolocation API", "app_name": "..."}
Code HTTP: 200
```

**2. GET /ip/{ip_address}**
```
Description: Géolocalisation d'une adresse IP
Paramètre: ip_address (string, requis)
Réponse: Données de géolocalisation
Codes HTTP:
  - 200: Succès
  - 400: Requête invalide
  - 503: Service unavailable
```

#### Gestion des erreurs

| Type d'erreur | Gestion |
|---------------|---------|
| Timeout | HTTPException 503 |
| Connexion échouée | HTTPException 503 |
| IP invalide | HTTPException 400 |
| Réponse vide | HTTPException 503 |

#### Support CORS
- Origins: `*` (tous les domaines)
- Credentials: Activé
- Methods: Tous (`GET`, `POST`, etc.)
- Headers: Tous autorisés

### 5.2 Client.py (Frontend NiceGUI)

#### Classe GeolocateClient

**Initialisation:**
```python
client = GeolocateClient(
    server_hostname="127.0.0.1",
    server_port=8000
)
```

**Méthodes principales:**

| Méthode | Paramètres | Retour | Description |
|---------|-----------|--------|-------------|
| `query()` | ip_address (str) | dict \| None | Requête géolocalisation |
| `open_map()` | latitude, longitude, country | None | Ouverture OpenStreetMap |

#### Interface utilisateur NiceGUI

**Éléments:**
- Champ saisie IP (placeholder: "8.8.8.8")
- Hostname configurable (défaut: 127.0.0.1)
- Port configurable (défaut: 8000)
- Zone résultat affichage données
- Bouton ouverture carte
- Messages statut et erreurs

---

## 6. STRUCTURE DES FICHIERS

```
C:\Users\pc\Desktop\python\python\
├── pyproject.toml              # Configuration Poetry
├── poetry.lock                 # Verrouillage versions dépendances
├── .env.example               # Modèle configuration
├── README.md                  # Documentation (ce fichier)
├── RUNNING.md                 # Guide démarrage détaillé
├── webserv.py                 # API FastAPI (125 lignes)
├── client.py                  # Client NiceGUI (172 lignes)
├── test_nicegui.py           # Test de vérification
├── .venv/                     # Environnement virtuel
└── __pycache__/              # Cache Python
```

---

## 7. GESTION DES ERREURS ET DÉPANNAGE

### 7.1 Erreurs courantes

#### Erreur: "Failed to connect to server"
- **Cause:** Serveur API non démarré
- **Solution:** Démarrer le serveur dans Terminal 1
```bash
poetry run uvicorn webserv:app --reload
```

#### Erreur: "Request timed out"
- **Cause:** API CIRCL inaccessible
- **Solution:** 
  - Vérifier connexion Internet
  - Vérifier URL API: https://ip.circl.lu
  - Augmenter timeout (actuellement 10s)

#### Erreur: "Port already in use"
- **Cause:** Port 8000 ou 8080 occupé
- **Solution:**
```bash
# Chercher processus sur port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Tuer le processus (Windows)
taskkill /PID {PID} /F
```

#### Erreur: Module non trouvé
- **Cause:** Dépendances non installées
- **Solution:** `poetry install`

### 7.2 Logs et debugging

#### Activer le mode debug
```bash
# Modifier .env
DEBUG=True

# Ou démarrer avec paramètre
poetry run uvicorn webserv:app --reload --log-level debug
```

#### Localisation des logs
- Terminal API: Sortie Uvicorn standard
- Client: Messages NiceGUI dans terminal
- Navigateur: Console DevTools (F12)

---

## 8. MAINTENANCE ET MONITORING

### 8.1 Mise à jour des dépendances

```bash
# Vérifier les mises à jour disponibles
poetry show --latest

# Mettre à jour une dépendance
poetry update fastapi

# Mettre à jour tous les paquets
poetry update
```

### 8.2 Performance

**Optimisations implémentées:**
- Cache LRU sur `get_settings()`
- Requêtes asynchrones FastAPI
- Timeout client 10 secondes
- Middleware CORS optimisé

**Métriques à surveiller:**
- Temps réponse API (cible: <1s)
- Disponibilité CIRCL API
- Utilisation mémoire (client léger)

### 8.3 Sécurité

**Configurations actuelles:**
- CORS autorisant tous les origins (⚠️ À restreindre en production)
- Validation Pydantic des IP
- Gestion des erreurs sans exposition de stack traces

**Recommandations:**
```python
# En production, restreindre CORS
allow_origins=["https://yourdomain.com"]

# Implémenter authentification
# Ajouter rate limiting
# Valider formats IP (IPv4/IPv6)
```

---

## 9. CONTACT ET SUPPORT

**Auteur:** KAMENI TCHOUATCHEU GAETAN BRUNEL  
**Email:** gaetanbrunel.kamenitchouatcheu@et.esiea.fr  
**Institution:** ESIEA  

---

## 10. HISTORIQUE DES VERSIONS

| Version | Date | Description | Auteur |
|---------|------|-------------|--------|
| 0.1.0 | 09/02/2026 | Création initiale | KAMENI |
| 0.1.1 | 10/02/2026 | DCE complet | KAMENI |

---

**Document validé:** 10 février 2026  
**Dernière mise à jour:** 10 février 2026

### client.py (NiceGUI Frontend)
- **GeolocateClient Class:** Encapsulates API communication logic
- **Interactive UI:** Input fields for IP address and server configuration
- **Real-time Results:** Displays geolocation data including:
  - City and Country
  - Latitude and Longitude
  - ASN and Timezone
- **OpenStreetMap Integration:** Automatically opens OSM map centered on the coordinates
- **Error Handling:** User-friendly error messages via notifications

## API Responses

### Successful Response (200)
```json
{
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "latitude": 37.386,
  "longitude": -122.084,
  "city": "Mountain View",
  "asn": "AS15169",
  "timezone": "America/Los_Angeles"
}
```

### Error Response (404)
```json
{
  "detail": "IP not found in CIRCL database: 127.0.0.1"
}
```

## Configuration

Create a `.env` file to customize settings (optional):
```
APP_NAME=My IP Geolocation Service
CIRCL_API_URL=https://ip.circl.lu
DEBUG=true
```

## Troubleshooting

1. **"Failed to connect to server"** - Make sure `webserv.py` is running in another terminal
2. **"IP not found"** - Not all IPs have geolocation data. Try 8.8.8.8 (Google DNS)
3. **Port already in use** - Change port numbers in the client input fields or stop the conflicting process

## Exercise Answers

### What is a Web Service?
A web service is a software system that allows communication between computers over a network using standard web protocols (HTTP/HTTPS).

### What is a REST API?
REST (Representational State Transfer) is an architectural style for APIs that uses HTTP methods (GET, POST, PUT, DELETE) to perform operations on resources identified by URLs.

### What is FastAPI?
FastAPI is a modern Python web framework for building APIs quickly with automatic validation, documentation, and async support.

### Pydantic Settings Questions
- **Class to inherit:** `BaseSettings` from `pydantic_settings`
- **Default field:** `circl_api_url: str = "https://ip.circl.lu"`
- **String field:** `app_name: str = "API Name"`
- **Environment variables:** Yes, automatically mapped if field names match env var names (case-insensitive with BaseSettings)
- **Loading .env:** Configured in Config class with `env_file = ".env"`
- **Caching:** Use `@lru_cache()` decorator to load once and reuse

### Client Implementation Questions
- **Class structure:** `GeolocateClient` encapsulates the logic
- **Request method:** `query(ip_address)` takes IP and server hostname
- **URL construction:** `f"http://{hostname}:{port}/ip/{ip_address}"`
- **HTTP GET:** Use `requests.get(url, timeout=10)`
- **Success check:** `response.status_code == 200`
- **Return format:** `response.json()` for JSON parsing
- **Instantiation:** `client = GeolocateClient("127.0.0.1", 8000)`
- **Localhost call:** `http://127.0.0.1:8000/ip/{ip}`

### NiceGUI UI Components
- **Title:** `ui.label("Title")`
- **IP Input:** `ui.input(label="IP", placeholder="...")`
- **Button:** `ui.button("Geolocate", on_click=handler)`
- **Results:** `ui.label()` or `ui.markdown()` for formatted output
- **Errors:** `ui.notify(message, type="negative")`
- **Launch:** `ui.run(host="0.0.0.0", port=8080)`

### CIRCL API Integration
- **Test URL:** `https://ip.circl.lu/geolookup/8.8.8.8`
- **Response Format:** JSON
- **Key fields:** `latitude`, `longitude`, `country`, `city`, `asn`, `timezone`
