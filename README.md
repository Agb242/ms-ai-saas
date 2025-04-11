# SMS AI SaaS

Un SaaS open-source multi-tenant permettant de créer des assistants conversationnels accessibles par SMS.

## 🚀 Fonctionnalités

- Gestion multi-tenant avec isolation des données
- Intégration avec Kannel/Gammu pour la gestion des SMS
- Intégration avec OpenRouter AI pour les réponses intelligentes
- Interface d'administration pour la configuration
- Historique des conversations

## 🛠️ Stack Technique

- Backend: FastAPI (Python)
- Base de données: PostgreSQL avec Row-Level Security
- Authentification: JWT + bcrypt
- Passerelle SMS: Kannel/Gammu
- IA: OpenRouter AI
- Frontend: React.js

## 📦 Installation

### Prérequis

- Python 3.8+
- PostgreSQL
- Docker et Docker Compose
- Kannel ou Gammu

### Installation locale

1. Cloner le repository:
```bash
git clone https://github.com/votre-username/sms-ai-saas.git
cd sms-ai-saas
```

2. Installer les dépendances:
```bash
cd backend
pip install -r requirements.txt
```

3. Configurer l'environnement:
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

4. Lancer les services:
```bash
docker-compose up -d
```

## 🔧 Configuration

1. Configurer Kannel/Gammu
2. Configurer les clés API OpenRouter
3. Configurer la base de données PostgreSQL

## 📝 Licence

MIT License 