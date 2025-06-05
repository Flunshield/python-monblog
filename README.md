# MonProjet Django Blog 🚀

> **Plateforme de blog moderne avec intelligence artificielle intégrée**

Une application web complète développée avec Django, proposant une gestion avancée d'articles, système de rôles sophistiqué, modération intelligente des commentaires, génération de contenu par IA Gemini et support multilingue.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Django](https://img.shields.io/badge/Django-5.2-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-100%25-success)
![AI](https://img.shields.io/badge/AI-Gemini-purple)

<!-- ============================= -->
## 🌐 **DÉMO EN LIGNE** : [monblog.jbertrand.fr](https://monblog.jbertrand.fr/fr/)
<!-- ============================= -->


## 📋 Table des matières

- [✨ Présentation](#-présentation)
- [🚀 Aperçu des fonctionnalités](#-aperçu-des-fonctionnalités)
- [⚡ Démarrage rapide](#-démarrage-rapide)
- [📦 Prérequis](#-prérequis)
- [🔧 Installation détaillée](#-installation-détaillée)
- [🏗️ Architecture du projet](#️-architecture-du-projet)
- [🔧 Fonctionnalités principales](#-fonctionnalités-principales)
- [🤖 Intelligence artificielle](#-intelligence-artificielle)
- [👥 Système de rôles](#-système-de-rôles)
- [🌐 Internationalisation](#-internationalisation)
- [🔒 Sécurité](#-sécurité)
- [🧪 Tests](#-tests)
- [🐳 Déploiement](#-déploiement)
- [🛠️ API & Endpoints](#️-api--endpoints)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)
- [📞 Contact](#-contact)

---

## ✨ Présentation

**MonProjet Django Blog** est une plateforme de publication moderne qui révolutionne la création de contenu grâce à l'intelligence artificielle. Construite avec Django 5.2 et intégrée avec l'API Gemini de Google, cette application offre une expérience utilisateur exceptionnelle pour les créateurs de contenu.

### 🎯 Objectifs du projet
- **Démocratiser** la création de contenu de qualité
- **Automatiser** les tâches répétitives de rédaction
- **Faciliter** la collaboration entre journalistes et administrateurs
- **Offrir** une expérience multilingue complète

### 💡 Points forts
- ✅ **Interface moderne** et responsive (Bootstrap 5)
- ✅ **IA Gemini intégrée** pour la génération automatique d'articles
- ✅ **Système de rôles dynamique** (Admin, Journaliste, Lecteur)
- ✅ **Modération intelligente** des commentaires
- ✅ **Support multilingue** (Français, Anglais, Espagnol)
- ✅ **Déploiement Docker** prêt pour la production
- ✅ **Tests automatisés** avec couverture complète

---

## 🚀 Aperçu des fonctionnalités

### 🤖 Intelligence Artificielle
| Fonctionnalité | Description | Statut |
|----------------|-------------|---------|
| **Génération d'articles** | Création automatique de contenu avec Gemini 2.0 | ✅ Actif |
| **Support multilingue IA** | Génération en français, anglais, espagnol | ✅ Actif |
| **Interface intuitive** | Page dédiée avec prévisualisation en temps réel | ✅ Actif |

### 👥 Gestion des utilisateurs
| Rôle | Permissions | Capacités |
|------|-------------|-----------|
| **🔥 Admin** | Accès total | Gestion utilisateurs, catégories, articles, commentaires, IA |
| **✍️ Journaliste** | Création & modération | Articles, commentaires sur ses articles, génération IA |
| **👤 Lecteur** | Consultation | Lecture, commentaires, likes |

### 📝 Gestion de contenu
- **Articles** : CRUD complet avec images, catégories, auteur automatique
- **Catégories** : Organisation hierarchisée du contenu
- **Commentaires** : Système de modération avancé avec réponses
- **Likes** : Interaction AJAX sans rechargement
- **Recherche** : Filtrage par catégorie et contenu

### 🌐 Expérience utilisateur
- **Responsive Design** : Interface optimisée mobile/desktop
- **Thème sombre/clair** : Basculement dynamique
- **Traductions** : 3 langues supportées
- **Notifications** : Feedback temps réel (toasts)
- **Navigation** : Menu contextuel selon les rôles

---

## Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/Flunshield/python-monblog.git
cd monprojet
```

### 2. Configurer les variables d'environnement
- Copier le fichier `.env.example` en `.env` :
  ```bash
  cp .env.example .env
  ```
- Ouvrir `.env` et renseigner les valeurs adaptées à votre environnement :
  - `SECRET_KEY` : une clé secrète Django (générer avec `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
  - `DEBUG` : `True` ou `False` selon l'environnement
  - `DATABASE_URL` : URL de connexion à la base de données (exemple pour SQLite : `sqlite:///db.sqlite3`)
  - Adapter les autres variables si besoin (voir commentaires dans `.env.example`)

### 3. Lancer le projet avec Docker Compose (recommandé pour la prod ou tests rapides)
```bash
docker compose up --build
```
- Le projet sera accessible sur http://localhost:8000
- Pour arrêter : `docker compose down`

### 4. (Alternative) Installation manuelle (en local, sans Docker)

#### a. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

#### b. Installer les dépendances
```bash
pip install -r requirements.txt
```

#### c. Appliquer les migrations
```bash
python manage.py migrate
```

#### d. Créer un superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

#### e. Lancer le serveur de développement
```bash
python manage.py runserver
```

---

## Commandes utiles

- Lancer les tests :
  ```bash
  python manage.py test
  ```
- Générer les fichiers de traduction :
  ```bash
  python manage.py makemessages -l fr
  python manage.py makemessages -l en
  python manage.py makemessages -l es
  ```
- Compiler les traductions :
  ```bash
  python manage.py compilemessages
  ```
- Collecter les fichiers statiques :
  ```bash
  python manage.py collectstatic
  ```

---

## Structure du projet

```text
monprojet/
├── blog/                # Application principale (modèles, vues, templates)
│   ├── models.py        # Modèles Article, Catégorie, Commentaire, etc.
│   ├── views.py         # Vues principales
│   ├── forms.py         # Formulaires Django
│   ├── templates/       # Templates HTML (blog/)
│   ├── static/          # Fichiers statiques (CSS, JS, images)
│   └── ...
├── core/                # Configuration du projet (ASGI, WSGI)
├── locale/              # Fichiers de traduction (.po/.mo)
├── media/               # Fichiers uploadés (images d'articles)
├── static/              # Fichiers statiques collectés
├── manage.py            # Commande d'administration Django
├── requirements.txt     # Dépendances Python
└── ...
```

**Principaux dossiers/fichiers :**
- `blog/` : logique métier, modèles, vues, templates
- `static/` : ressources statiques globales
- `media/` : fichiers uploadés par les utilisateurs
- `locale/` : traductions multilingues
- `settings.py` : configuration Django

---

## Fonctionnalités principales

- 🔐 **Authentification & gestion des utilisateurs** (admin, journaliste, lecteur)
- 📝 **CRUD complet des articles** (création, modification, suppression, consultation)
- 🗂️ **Gestion des catégories** (ajout, édition, suppression, filtrage)
- 💬 **Commentaires** (ajout, modération, validation par admin/journaliste)
- 👍 **Likes sur les articles** (AJAX, sans rechargement)
- 🌐 **Traduction multilingue** (français, anglais, espagnol)
- 📊 **Statistiques** (nombre d'articles, commentaires, stats par journaliste)
- 🔎 **Filtrage et recherche** (par catégorie)
- 🖼️ **Upload et gestion d'images**
- 🛡️ **Gestion des rôles et permissions avancées**
- 🌙 **Thème sombre/clair avec bouton de bascule**
- 📝 **Logging avancé** (logs séparés par niveau dans /logs)
- 🐳 **Déploiement Dockerisé & Procfile Heroku/Render**
- 🧪 **Tests unitaires et d'intégration étendus**
- 💄 **UI/UX moderne et responsive** (navbar, footer, etc.)

### Exemples d'utilisation
- Un journaliste peut créer et gérer ses propres articles, mais ne peut pas gérer les utilisateurs.
- Un admin a accès à toutes les fonctionnalités (gestion des utilisateurs, catégories, etc.).
- Les visiteurs peuvent lire, commenter et liker les articles.

---

## API / Endpoints

Le projet propose une API REST/AJAX complète avec authentification et gestion des permissions selon les rôles utilisateurs.

### 🌐 Endpoints Publics

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET` | `/` | Page d'accueil avec articles récents et populaires | Public |
| `GET` | `/articles/` | Liste complète des articles avec pagination | Public |
| `GET` | `/articles/<int:article_id>/` | Détail d'un article avec commentaires | Public |
| `GET` | `/recherche/` | Recherche d'articles avec filtres | Public |

### 🔐 Authentification

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET/POST` | `/register/` | Inscription utilisateur | Public |
| `GET/POST` | `/login/` | Connexion utilisateur | Public |
| `POST` | `/logout/` | Déconnexion utilisateur | Authentifié |
| `GET/POST` | `/password-reset/` | Demande de réinitialisation mot de passe | Public |
| `GET/POST` | `/password-reset-confirm/<uidb64>/<token>/` | Confirmation réinitialisation | Public |

### 📝 Gestion des Articles

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET/POST` | `/ajouter/` | Créer un article | Journaliste, Admin |
| `GET/POST` | `/modifier-article/<int:article_id>/` | Modifier un article | Auteur, Admin |
| `GET/POST` | `/supprimer-article/<int:article_id>/` | Supprimer un article | Auteur, Admin |
| `GET` | `/gerer-articles/` | Liste des articles à gérer | Journaliste, Admin |

### 🗂️ Gestion des Catégories

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET/POST` | `/ajouter-categorie/` | Créer une catégorie | Admin |
| `GET` | `/gerer-categories/` | Liste des catégories | Journaliste, Admin |
| `GET/POST` | `/modifier-categorie/<int:category_id>/` | Modifier une catégorie | Admin |
| `GET/POST` | `/supprimer-categorie/<int:category_id>/` | Supprimer une catégorie | Admin |

### 🤖 Intelligence Artificielle

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET` | `/gemini-generator/` | Interface de génération IA | Journaliste, Admin |
| `POST` | `/generate-article-ai/` | API AJAX de génération d'articles | Journaliste, Admin |

**Exemple de requête AJAX pour génération IA :**
```json
POST /generate-article-ai/
Content-Type: application/json
X-CSRFToken: <token>

{
  "resume": "Article sur l'intelligence artificielle",
  "langue": "fr"
}
```
**Réponse :**
```json
{
  "success": true,
  "titre": "L'Intelligence Artificielle : Révolution Technologique",
  "contenu": "L'intelligence artificielle transforme notre monde..."
}
```

### 💬 Interactions & Modération

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `POST` | `/like/<int:article_id>/` | Like/Unlike un article (AJAX) | Authentifié |
| `GET` | `/moderation-commentaires/` | Interface de modération | Journaliste, Admin |
| `POST` | `/moderation-commentaires/` | Actions de modération | Journaliste, Admin |

**Exemple de requête AJAX pour liker un article :**
```json
POST /like/42/
X-CSRFToken: <token>
```
**Réponse (redirection avec message) :**
```http
HTTP 302 Found
Location: /articles/42/
Messages: "Article liké" ou "Like retiré"
```

### 👥 Espaces Utilisateurs

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET` | `/profile/` | Profil utilisateur avec statistiques | Authentifié |
| `GET` | `/admin-page/` | Tableau de bord administrateur | Admin |
| `GET` | `/journaliste-page/` | Tableau de bord journaliste | Journaliste, Admin |

### 🛠️ Utilitaires & Debug

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET` | `/diagnostic-images/` | Diagnostic des images uploadées | Admin |
| `GET` | `/debug-like/` | Page de test pour les likes | Authentifié |

### 🌐 Internationalisation

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `POST` | `/i18n/set_language/` | Changement de langue | Public |

### 🔧 Administration Django

| Méthode | Endpoint | Description | Permissions |
|---------|----------|-------------|------------|
| `GET/POST` | `/admin/` | Interface d'administration Django | Staff |

### 📋 Codes de Réponse

| Code | Description |
|------|-------------|
| `200` | Succès |
| `302` | Redirection (après POST réussi) |
| `403` | Accès interdit (permissions insuffisantes) |
| `404` | Ressource non trouvée |
| `500` | Erreur serveur |

### 🔒 Sécurité des APIs

- **Protection CSRF** : Tous les endpoints POST nécessitent un token CSRF valide
- **Authentification** : Sessions Django pour les endpoints protégés
- **Permissions** : Vérification des rôles utilisateur (lecteur, journaliste, admin)
- **Validation** : Validation stricte des données d'entrée
- **Rate Limiting** : Protection contre les abus (recommandé en production)

---

## Sécurité

- Authentification Django (sessions, hash des mots de passe)
- Permissions par rôle (admin, journaliste, lecteur)
- Protection CSRF sur tous les formulaires
- Validation des entrées utilisateurs
- Gestion des fichiers uploadés (vérification type/taille)

---

## Traductions et internationalisation 🌍

- Utilisation de `gettext` et des fichiers `.po/.mo` dans `locale/`
- Commandes associées :
  ```bash
  python manage.py makemessages -l fr
  python manage.py makemessages -l en
  python manage.py compilemessages
  ```
- Les templates utilisent le tag `{% trans %}` pour les textes traduisibles

---

## Tests

- Lancer tous les tests :
  ```bash
  python manage.py test
  ```
- Tests unitaires et d'intégration couvrant :
  - Modèles (Article, Catégorie, Commentaire)
  - Vues (CRUD, permissions)
  - Authentification et rôles
  - Traductions

---

## Contribution

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/ma-feature`)
3. Commitez vos modifications (`git commit -am 'Ajout d'une feature'`)
4. Poussez la branche (`git push origin feature/ma-feature`)
5. Ouvrez une Pull Request

**Conventions de code :**
- Respecter la PEP8 pour Python
- Utiliser des noms explicites
- Documenter les fonctions importantes

---

## Licence

Ce projet est sous licence MIT. ![Licence](https://img.shields.io/badge/license-MIT-green)

---

## Historique des évolutions

- Ajout du système de rôles avancé (admin, journaliste, lecteur)
- Modération et validation des commentaires
- Système de likes AJAX
- Statistiques détaillées pour les journalistes
- Gestion multilingue complète (français, anglais)
- Thème sombre/clair avec bouton de bascule
- Logging avancé (fichiers logs par niveau)
- Sécurité renforcée (permissions, CSRF, validation)
- Déploiement Dockerisé et Procfile pour Heroku/Render
- Tests unitaires et d’intégration étendus
- Améliorations UI/UX (navbar, footer, responsive, etc.)

---

## Contact

- [GitHub](https://github.com/Flunshield)
- Email : j.bertrand.sin@gmail.com

---

## Screenshots & Démos

> Ajoutez ici des captures d'écran ou GIFs pour illustrer le fonctionnement du blog !

---

## 🚀 Déploiement en Production avec Docker

Le projet est prêt pour un déploiement sécurisé et automatisé en production grâce à Docker.

### Démarrage rapide (production)

```bash
# Build et lancement (créera automatiquement les comptes essentiels)
docker compose up --build
```

- **Comptes créés automatiquement lors du premier démarrage :**
  | Username      | Email                    | Rôle         | Mot de passe par défaut         |
  |--------------|--------------------------|--------------|---------------------------------|
  | `admin`      | admin@monprojet.com      | admin        | `${DJANGO_ADMIN_PASSWORD}`      |
  | `journaliste`| journaliste@monprojet.com| journaliste  | `${DJANGO_ADMIN_PASSWORD}`      |
  | `lecteur`    | lecteur@monprojet.com    | lecteur      | `${DJANGO_ADMIN_PASSWORD}`      |

- Le mot de passe par défaut est `ProdAdmin2024!` (modifiable via la variable d'environnement `DJANGO_ADMIN_PASSWORD`).
- Le seeding ne recrée pas les comptes s'ils existent déjà.
- L'application s'exécute en mode sécurisé (utilisateur non-root, debug désactivé, permissions renforcées).

Pour plus de détails, voir aussi le fichier `PRODUCTION_DEPLOY.md`.

---

🔥 Merci d'utiliser MonProjet Django Blog !
