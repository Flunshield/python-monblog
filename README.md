# MonProjet Django Blog 🚀

Un blog moderne développé avec Django permettant la gestion d'articles, de catégories, de commentaires, de rôles utilisateurs et la traduction multilingue.

![Version](https://img.shields.io/badge/version-1.0-blue)
![Licence](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-passing-success)

<!-- ============================= -->
# 🚀 EN PRODUCTION : https://monblog.jbertrand.fr/fr/
<!-- ============================= -->


## Table des matières
- [Présentation](#présentation)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [API / Endpoints](#api--endpoints)
- [Sécurité](#sécurité)
- [Traductions et internationalisation](#traductions-et-internationalisation)
- [Tests](#tests)
- [Contribution](#contribution)
- [Licence](#licence)
- [Historique des évolutions](#historique-des-évolutions)
- [Contact](#contact)
- [Screenshots & Démos](#screenshots--démos)

---

## Présentation

Ce projet est une plateforme de blog moderne construite avec Django. Il propose une gestion complète des articles, des catégories, des commentaires, des rôles utilisateurs (admin, journaliste, lecteur) et prend en charge l'internationalisation (français/anglais).

---

## Prérequis

- **Python** >= 3.10
- **Django** >= 4.2
- **pip** (gestionnaire de paquets Python)
- **virtualenv** (recommandé)
- **Git**
- **Docker** (optionnel, pour le déploiement)

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

#### Mode Production :
```bash
# Démarrage avec seeding minimal (rôles, catégories, compte admin)
docker compose up --build

# Avec mot de passe admin personnalisé
DJANGO_ADMIN_PASSWORD="MonMotDePasseSecurise123!" docker compose up --build
```

#### Mode Développement :
```bash
# Démarrage avec données de test complètes (utilisateurs, articles, commentaires, likes)
docker compose -f docker-compose.dev.yml up --build

# Avec mot de passe personnalisé pour les comptes de test
DJANGO_ADMIN_PASSWORD="DevPassword123!" docker compose -f docker-compose.dev.yml up --build
```

- Le projet sera accessible sur http://localhost:8000
- Pour arrêter : `docker compose down`
- **Seeding automatique** : Les données sont créées automatiquement au premier démarrage

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

### 🌱 Commandes de Seeding (Données de test)

Le projet inclut un système complet de seeders pour initialiser la base de données avec des données de test :

#### Seeding global :
```bash
# Seeding complet pour développement (tout en une fois)
python manage.py seed_all

# Seeding minimal pour production
python manage.py seed_production --admin-password "MotDePasseSecurise123!"
```

#### Seeding par composant :
```bash
# Créer les rôles de base (lecteur, journaliste, admin)
python manage.py seed_roles

# Créer des catégories d'articles
python manage.py seed_categories

# Créer des utilisateurs de test avec différents rôles
python manage.py seed_users --password "testpass123"

# Créer des articles d'exemple
python manage.py seed_articles --count 15

# Créer des commentaires sur les articles
python manage.py seed_comments --count 30

# Créer des likes sur les articles
python manage.py seed_likes --count 50

# Nettoyer toutes les données de test
python manage.py clear_seed_data --confirm
```

#### 🐳 Seeding automatique avec Docker :
- **Production** (`docker-compose.yml`) : Seeding minimal automatique au premier démarrage
- **Développement** (`docker-compose.dev.yml`) : Seeding complet avec données de test

Voir le [Guide des Seeders](SEEDING_GUIDE.md) pour plus de détails.

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
- 🌱 **Système de seeding complet** (données de test automatisées)
- 💄 **UI/UX moderne et responsive** (navbar, footer, etc.)

### 🔑 Comptes de test (mode développement)

Lors du lancement en mode développement (`docker-compose.dev.yml`), les comptes suivants sont automatiquement créés :

| Username | Email | Rôle | Mot de passe | Fonctionnalités |
|----------|-------|------|--------------|-----------------|
| `admin_test` | admin@test.com | Admin | `DevAdmin123!`* | Accès complet à l'administration |
| `journaliste_test` | journaliste@test.com | Journaliste | `DevAdmin123!`* | Création/modification d'articles |
| `lecteur_test` | lecteur@test.com | Lecteur | `DevAdmin123!`* | Lecture, commentaires, likes |

_*Le mot de passe peut être personnalisé via `DJANGO_ADMIN_PASSWORD`_

### Exemples d'utilisation
- Un journaliste peut créer et gérer ses propres articles, mais ne peut pas gérer les utilisateurs.
- Un admin a accès à toutes les fonctionnalités (gestion des utilisateurs, catégories, etc.).
- Les visiteurs peuvent lire, commenter et liker les articles.

---

## API / Endpoints

> **Remarque :** Le projet est principalement orienté web (HTML), mais certaines routes peuvent accepter des requêtes AJAX/JSON.

- `/` : Accueil, liste des articles
- `/article/<id>/` : Détail d'un article
- `/categorie/<id>/` : Articles d'une catégorie
- `/login/`, `/logout/`, `/register/` : Authentification
- `/admin/` : Interface d'administration Django
- `/like/` : Like/Unlike d'un article (POST, AJAX)

**Exemple de requête AJAX pour liker un article :**
```json
POST /like/
{
  "article_id": 42
}
```
**Réponse :**
```json
{
  "status": "success",
  "likes": 12
}
```

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

🔥 Merci d'utiliser MonProjet Django Blog !
