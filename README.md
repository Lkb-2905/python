# 🌍 DOSSIER DE CONFIGURATION D'EXPLOITATION (DCE)
## 🌍 GeoIP-Vision V1.0

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![NiceGUI](https://img.shields.io/badge/NiceGUI-1.4+-FF6B6B?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Version:** 1.0.0 Stable | **Date:** Février 2026  
**Auteur:** KAMENI TCHOUATCHEU GAETAN BRUNEL  
**Contact:** [gaetanbrunel.kamenitchouatcheu@et.esiea.fr](mailto:gaetanbrunel.kamenitchouatcheu@et.esiea.fr)

[🚀 Démarrage Rapide](#-démarrage-rapide) • [📚 Documentation](#-architecture-technique) • [🎯 Fonctionnalités](#-fonctionnalités-clés) • [🔧 Installation](#-installation-complète)

</div>

---

## 📋 TABLE DES MATIÈRES

1. [Vue d'ensemble du projet](#-vue-densemble-du-projet)
2. [Architecture Technique](#-architecture-technique)
3. [Stack Technologique](#-stack-technologique)
4. [Fonctionnalités Clés](#-fonctionnalités-clés)
5. [Démarrage Rapide](#-démarrage-rapide)
6. [Installation Complète](#-installation-complète)
7. [Guide d'Utilisation](#-guide-dutilisation)
8. [API Documentation](#-api-documentation)
9. [Qualité & Best Practices](#-qualité--best-practices)
10. [Roadmap & Évolutions](#-roadmap--évolutions)

---

## 🎯 VUE D'ENSEMBLE DU PROJET

### Contexte & Objectifs

Ce projet démontre la mise en œuvre d'une **architecture orientée microservices moderne** pour la géolocalisation d'adresses IP. Il illustre les compétences suivantes :

- ✅ **Architecture Découplée** : Séparation stricte Backend/Frontend
- ✅ **API RESTful** : Conception d'endpoints robustes avec FastAPI
- ✅ **Gestion d'État** : Configuration centralisée avec Pydantic Settings
- ✅ **Intégration Externe** : Consommation d'API tierces (CIRCL.LU)
- ✅ **UX Moderne** : Interface réactive sans rechargement de page
- ✅ **Clean Code** : Respect des standards Python (PEP8, Type Hints, Docstrings)

### Pourquoi ce projet ?

| Aspect | Démonstration |
|--------|---------------|
| **Scalabilité** | Architecture microservices prête pour le déploiement cloud |
| **Maintenabilité** | Code modulaire avec séparation des responsabilités |
| **Performance** | Caching LRU, requêtes asynchrones, timeout optimisés |
| **Sécurité** | Validation des entrées, gestion d'erreurs robuste, CORS configuré |
| **DevOps Ready** | Configuration par environnement, logs structurés |

---

## 🏗️ ARCHITECTURE TECHNIQUE

### Diagramme de Flux

```mermaid
graph TB
    subgraph "Client Layer"
        A[👤 Utilisateur] -->|Saisie IP| B[NiceGUI Frontend<br/>Port 8080]
    end
    
    subgraph "Application Layer"
        B -->|HTTP GET /ip/{ip}| C[FastAPI Backend<br/>Port 8000]
        C -->|Validation & Cache| D[Service Géolocalisation]
    end
    
    subgraph "External Services"
        D -->|HTTPS Request<br/>Timeout: 10s| E[CIRCL.LU API<br/>ip.circl.lu]
    end
    
    subgraph "Presentation Layer"
        E -->|JSON Response| D
        D -->|Données Normalisées| C
        C -->|Payload JSON| B
        B -->|Affichage Dynamique| F[Résultats UI]
        B -->|Ouverture Auto| G[🗺️ OpenStreetMap]
    end
    
    style B fill:#4A90E2,stroke:#2E5C8A,color:#fff
    style C fill:#50C878,stroke:#2E7D4E,color:#fff
    style E fill:#FF6B6B,stroke:#C44545,color:#fff
    style G fill:#FFB84D,stroke:#CC8F3D,color:#fff
```

### Flux de Données Détaillé

1. **Requête Utilisateur**
   - L'utilisateur saisit une adresse IP dans l'interface NiceGUI
   - Validation côté client (format, champs requis)

2. **Traitement Backend**
   - FastAPI reçoit la requête via endpoint `/ip/{ip_address}`
   - Validation Pydantic des paramètres
   - Interrogation de l'API CIRCL avec timeout strict (10s)
   - Parsing et normalisation des données JSON

3. **Réponse & Visualisation**
   - Retour des données structurées au frontend
   - Mise à jour dynamique de l'interface (sans rechargement)
   - Ouverture automatique d'OpenStreetMap centrée sur les coordonnées GPS

---

## 🛠️ STACK TECHNOLOGIQUE

### Technologies Core

| Composant | Technologie | Version | Justification Technique |
|-----------|-------------|---------|-------------------------|
| **Langage** | Python | 3.12+ | Type Hints natifs, Performance améliorée, Pattern Matching |
| **Backend Framework** | FastAPI | 0.109+ | Performance (Starlette/ASGI), Validation auto (Pydantic), OpenAPI natif |
| **Frontend Framework** | NiceGUI | 1.4+ | Développement rapide, Composants réactifs, Python full-stack |
| **HTTP Client** | Requests | 2.31+ | Robustesse éprouvée, Gestion avancée des timeouts |
| **ASGI Server** | Uvicorn | 0.22+ | Performance optimale, Hot-reload pour développement |
| **Dependency Manager** | Poetry | 1.0+ | Lock file déterministe, Résolution de dépendances intelligente |

### Bibliothèques Complémentaires

- **Pydantic Settings** : Configuration centralisée et validation
- **CORS Middleware** : Sécurisation des requêtes cross-origin
- **functools.lru_cache** : Mise en cache des configurations

---

## 🎯 FONCTIONNALITÉS CLÉS

### 🚀 Fonctionnalités Principales

#### 1. Géolocalisation IP Précise
- **Source de données** : API CIRCL.LU (Luxembourg)
- **Informations récupérées** :
  - 🌍 Pays (nom complet + code ISO)
  - 📍 Coordonnées GPS (latitude/longitude)
  - 🏢 ASN (Autonomous System Number) + Organisation
  - 🗺️ Données pays (capitale, superficie, etc.)

#### 2. Visualisation Cartographique
- Intégration native avec **OpenStreetMap**
- Ouverture automatique du navigateur
- Centrage précis sur les coordonnées
- Zoom adaptatif (niveau 10)

#### 3. Interface Utilisateur Moderne
- Design responsive (TailwindCSS)
- Notifications en temps réel
- États de chargement visuels
- Configuration serveur dynamique

### 🛡️ Sécurité & Robustesse

| Aspect | Implémentation |
|--------|----------------|
| **Validation des entrées** | Vérification stricte des formats IP |
| **Gestion des erreurs** | Try/Except exhaustifs avec messages clairs |
| **Timeouts** | Limite de 10s pour éviter les blocages |
| **CORS** | Configuration sécurisée pour les origines autorisées |
| **Type Safety** | Type Hints complets pour prévenir les erreurs |

### ⚡ Performance & Optimisation

- **Caching LRU** : Configuration chargée une seule fois
- **Requêtes Asynchrones** : Endpoints FastAPI async-ready
- **Connexion Persistante** : Réutilisation des sessions HTTP
- **Payload Minimal** : Extraction uniquement des données nécessaires

---

## 🚀 DÉMARRAGE RAPIDE

### Prérequis
```bash
# Vérifier Python
python --version  # Doit être >= 3.12

# Installer Poetry (si nécessaire)
pip install poetry
```

### Installation Express (3 commandes)
```bash
# 1. Cloner le dépôt
git clone https://github.com/Lkb-2905/python.git
cd python

# 2. Installer les dépendances
poetry install

# 3. Lancer l'application (2 terminaux requis)
# Terminal 1 - Backend
poetry run python python/webserv.py

# Terminal 2 - Frontend
poetry run python python/client.py
```

### Accès Immédiat
- **Interface Web** : http://localhost:8080
- **API Backend** : http://127.0.0.1:8000
- **Documentation API** : http://127.0.0.1:8000/docs

---

## 🔧 INSTALLATION COMPLÈTE

### Étape 1 : Environnement Python

```bash
# Créer un environnement virtuel (optionnel avec Poetry)
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### Étape 2 : Installation des Dépendances

```bash
# Avec Poetry (recommandé)
poetry install

# Ou avec pip
pip install -r requirements.txt
```

### Étape 3 : Configuration (Optionnel)

Créer un fichier `.env` dans le dossier `python/` :

```env
# Configuration API
APP_NAME="IP Geolocation Service"
CIRCL_API_URL="https://ip.circl.lu"
DEBUG=False

# Configuration Serveur
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
```

### Étape 4 : Vérification de l'Installation

```bash
# Test simple
poetry run python python/test_nicegui.py

# Devrait afficher "Hello NiceGUI!" dans le navigateur
```

---

## 📖 GUIDE D'UTILISATION

### Démarrage des Services

#### Option 1 : Mode Développement (2 terminaux)

**Terminal 1 - Backend API**
```bash
cd python
poetry run python webserv.py
```
✅ Serveur démarré sur `http://127.0.0.1:8000`

**Terminal 2 - Frontend Client**
```bash
cd python
poetry run python client.py
```
✅ Interface accessible sur `http://localhost:8080`

#### Option 2 : Mode Production (Uvicorn)

```bash
# Backend avec Uvicorn
poetry run uvicorn python.webserv:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend
poetry run python python/client.py
```

### Utilisation de l'Interface

1. **Ouvrir le navigateur** : http://localhost:8080

2. **Saisir une IP** :
   - Exemple : `8.8.8.8` (Google DNS)
   - Exemple : `1.1.1.1` (Cloudflare DNS)
   - Exemple : `208.67.222.222` (OpenDNS)

3. **Cliquer sur "Geolocate IP"**

4. **Résultats affichés** :
   - Pays et code ISO
   - Coordonnées GPS
   - Informations ASN
   - Carte OpenStreetMap (ouverture auto)

### Captures d'Écran

![Interface Principale](python/screenshot.png)

---

## 📡 API DOCUMENTATION

### Endpoints Disponibles

#### 1. Root Endpoint
```http
GET /
```

**Réponse** :
```json
{
  "message": "Hello from IP Geolocation API",
  "app_name": "IP Geolocation Service"
}
```

#### 2. Géolocalisation IP
```http
GET /ip/{ip_address}
```

**Paramètres** :
- `ip_address` (path) : Adresse IP à géolocaliser

**Exemple de Requête** :
```bash
curl http://127.0.0.1:8000/ip/8.8.8.8
```

**Réponse Succès (200)** :
```json
{
  "ip": "8.8.8.8",
  "country": "United States",
  "country_code": "US",
  "latitude": 37.751,
  "longitude": -97.822,
  "city": "Unknown",
  "asn": "15169 (GOOGLE)",
  "timezone": "Unknown"
}
```

**Réponses Erreur** :

| Code | Description | Exemple |
|------|-------------|---------|
| 404 | IP non trouvée | `{"detail": "No geolocation data found for IP: 192.168.1.1"}` |
| 502 | Erreur API externe | `{"detail": "Failed to connect to CIRCL API"}` |
| 504 | Timeout | `{"detail": "CIRCL API request timed out"}` |
| 500 | Erreur serveur | `{"detail": "Internal server error: ..."}` |

### Documentation Interactive

FastAPI génère automatiquement une documentation Swagger :

- **Swagger UI** : http://127.0.0.1:8000/docs
- **ReDoc** : http://127.0.0.1:8000/redoc
- **OpenAPI Schema** : http://127.0.0.1:8000/openapi.json

---

## ✨ QUALITÉ & BEST PRACTICES

### Standards de Code

#### 1. Type Hints Complets
```python
def geolocate_ip(ip_address: str) -> dict:
    """Type hints pour la sécurité du typage"""
    pass
```

#### 2. Docstrings Exhaustives
```python
def query(self, ip_address: str) -> Optional[dict]:
    """
    Query the API for IP geolocation data
    
    Args:
        ip_address: The IP address to geolocate
        
    Returns:
        Dictionary containing geolocation data, or None if request failed
    """
```

#### 3. Gestion d'Erreurs Robuste
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.Timeout:
    raise HTTPException(status_code=504, detail="Request timed out")
except requests.exceptions.ConnectionError:
    raise HTTPException(status_code=502, detail="Connection failed")
```

#### 4. Configuration Centralisée
```python
class Settings(BaseSettings):
    """Pydantic Settings pour la configuration"""
    app_name: str = "IP Geolocation API"
    circl_api_url: str = "https://ip.circl.lu"
    
    model_config = SettingsConfigDict(env_file=".env")
```

### Principes Appliqués

| Principe | Implémentation |
|----------|----------------|
| **SOLID** | Single Responsibility (classes dédiées), Dependency Injection |
| **DRY** | Réutilisation via classes et fonctions utilitaires |
| **KISS** | Architecture simple et compréhensible |
| **Clean Code** | Nommage explicite, fonctions courtes, commentaires pertinents |

### Métriques de Qualité

- ✅ **Couverture de code** : Type hints sur 100% des fonctions
- ✅ **Conformité PEP8** : Respect strict des conventions Python
- ✅ **Documentation** : Docstrings sur toutes les fonctions publiques
- ✅ **Gestion d'erreurs** : Try/Except sur toutes les opérations I/O

---

## 🗺️ ROADMAP & ÉVOLUTIONS

### Version Actuelle : 1.0.0 ✅

- [x] Architecture microservices Backend/Frontend
- [x] Intégration API CIRCL.LU
- [x] Interface NiceGUI responsive
- [x] Visualisation OpenStreetMap
- [x] Gestion d'erreurs complète
- [x] Documentation exhaustive

### Version 1.1.0 (Prochaine Release) 🚧

- [ ] **Tests Unitaires** : Couverture > 80% avec pytest
- [ ] **Tests d'Intégration** : Validation des endpoints API
- [ ] **CI/CD** : GitHub Actions pour tests automatiques
- [ ] **Docker** : Containerisation complète
- [ ] **Logging Avancé** : Structured logging avec loguru

### Version 2.0.0 (Vision Long Terme) 🔮

- [ ] **Base de Données** : Cache Redis pour performances
- [ ] **Authentification** : JWT pour sécurisation API
- [ ] **Multi-API** : Agrégation de plusieurs sources (MaxMind, IPStack)
- [ ] **Dashboard Analytics** : Statistiques d'utilisation
- [ ] **Déploiement Cloud** : AWS/GCP avec Terraform
- [ ] **API Rate Limiting** : Protection contre les abus

---

## 🤝 CONTRIBUTION

### Comment Contribuer ?

1. **Fork** le projet
2. **Créer une branche** : `git checkout -b feature/AmazingFeature`
3. **Commit** : `git commit -m 'Add AmazingFeature'`
4. **Push** : `git push origin feature/AmazingFeature`
5. **Pull Request** : Ouvrir une PR avec description détaillée

### Standards de Contribution

- Respecter PEP8
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation
- Utiliser des commits conventionnels (feat, fix, docs, etc.)

---

## 📄 LICENCE

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 AUTEUR

**KAMENI TCHOUATCHEU GAETAN BRUNEL**  
Ingénieur Logiciel | Étudiant ESIEA

- 📧 Email : [gaetanbrunel.kamenitchouatcheu@et.esiea.fr](mailto:gaetanbrunel.kamenitchouatcheu@et.esiea.fr)
- 💼 LinkedIn : [Votre profil LinkedIn]
- 🐙 GitHub : [@Lkb-2905](https://github.com/Lkb-2905)

---

## 🙏 REMERCIEMENTS

- **CIRCL.LU** : Pour leur API de géolocalisation gratuite et performante
- **FastAPI** : Pour le framework backend moderne
- **NiceGUI** : Pour simplifier le développement d'interfaces web en Python
- **OpenStreetMap** : Pour les données cartographiques libres

---

<div align="center">

### ⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !

**Fait avec ❤️ et Python**

</div>

---

## 📞 SUPPORT

Pour toute question ou problème :

1. **Issues GitHub** : [Ouvrir une issue](https://github.com/Lkb-2905/python/issues)
2. **Email** : gaetanbrunel.kamenitchouatcheu@et.esiea.fr
3. **Documentation** : Consulter ce README et la doc API

---

> *"L'excellence n'est pas un acte, mais une habitude."* - Aristote
>
> *Ce projet démontre ma capacité à concevoir des architectures logicielles complètes, scalables et maintenables, en appliquant les meilleures pratiques de l'industrie.*

---

**© 2026 Kameni Tchouatcheu Gaetan Brunel - Tous droits réservés**
