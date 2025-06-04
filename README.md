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
