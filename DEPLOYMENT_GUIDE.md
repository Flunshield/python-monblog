# DEPLOYMENT_GUIDE.md

# 🚀 Guide de Déploiement – MonProjet Django Blog

Bienvenue dans le guide de déploiement professionnel de votre blog Django ! Ce document vous accompagne pas à pas pour mettre en production un projet sécurisé, optimisé et prêt pour la montée en charge.

---

## 📑 Table des matières
- [1️⃣ Introduction](#1️⃣-introduction)
- [2️⃣ Prérequis techniques](#2️⃣-prérequis-techniques)
- [3️⃣ Étapes détaillées pour la mise en production](#3️⃣-étapes-détaillées-pour-la-mise-en-production)
- [4️⃣ Conseils de sécurité](#4️⃣-conseils-de-sécurité)
- [5️⃣ Commandes utiles](#5️⃣-commandes-utiles)
- [6️⃣ Conclusion](#6️⃣-conclusion)

---

## 1️⃣ Introduction

Ce guide a pour objectif de vous permettre de déployer MonProjet Django Blog sur un serveur Linux (Ubuntu recommandé) avec une configuration professionnelle : PostgreSQL, Gunicorn, Nginx, sécurité renforcée et gestion des variables d’environnement.

---

## 2️⃣ Prérequis techniques

- 🐧 **OS** : Ubuntu 22.04 LTS ou équivalent
- 🐍 **Python** : 3.10+
- 🐘 **PostgreSQL** : 13+
- 🌐 **Nginx**
- 🐙 **Git**
- 🔒 **Certbot** (Let’s Encrypt pour SSL)

---

## 3️⃣ Étapes détaillées pour la mise en production

### 3.1 Cloner le projet
```bash
git clone https://github.com/Flunshield/python-monblog.git
cd monprojet
```

### 3.2 Créer l’environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3.4 Configurer les variables d’environnement
- Copier `.env.example` en `.env` et adapter les valeurs (SECRET_KEY, DB_*, etc.)

### 3.5 Configurer la base PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE monprojetdb;
CREATE USER monprojetuser WITH PASSWORD 'motdepassefort';
GRANT ALL PRIVILEGES ON DATABASE monprojetdb TO monprojetuser;
\q
```

### 3.6 Appliquer les migrations
```bash
python manage.py migrate
```

### 3.7 Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### 3.8 Compiler les traductions (optionnel)
```bash
python manage.py compilemessages
```

### 3.9 Lancer le serveur en production avec Gunicorn
```bash
gunicorn monprojet.wsgi --config gunicorn_config.py
```

### 3.10 Configurer Nginx comme reverse proxy
Exemple de configuration :
```nginx
server {
    listen 80;
    server_name monblog.com www.monblog.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        alias /app/staticfiles/;
    }
    location /media/ {
        alias /app/media/;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3.11 Sécuriser avec HTTPS (Let’s Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d monblog.com -d www.monblog.com
```

### 3.12 Démarrer Gunicorn en tant que service (systemd)
Exemple de fichier `/etc/systemd/system/gunicorn.service` :
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/app/monprojet
EnvironmentFile=/app/monprojet/.env
ExecStart=/app/monprojet/venv/bin/gunicorn monprojet.wsgi --config gunicorn_config.py

[Install]
WantedBy=multi-user.target
```

---

## 4️⃣ Conseils de sécurité

- 🔒 **Désactivez DEBUG** en production
- 🔒 **Définissez ALLOWED_HOSTS** correctement
- 🔒 **Activez SECURE_SSL_REDIRECT, HSTS, CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE**
- 🔒 **Utilisez des mots de passe forts** pour la base de données et le superutilisateur
- 🔒 **Mettez à jour régulièrement vos dépendances**
- 💡 **Sauvegardez régulièrement la base de données**

---

## 5️⃣ Commandes utiles

- Redémarrer Gunicorn (systemd) :
```bash
sudo systemctl restart gunicorn
```
- Vérifier les logs :
```bash
tail -f logs/*.log
```
- Mettre à jour le code :
```bash
git pull
```

---

## 🚢 Déploiement avec Docker

### 1. Préparer les variables d'environnement

- Copiez `.env.example` en `.env` et adaptez les valeurs (notamment `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`).
- Pour Docker Compose, laissez `DB_HOST=db` (nom du service PostgreSQL).

### 2. Lancer l'application avec Docker Compose

Dans le dossier du projet, exécutez :

```powershell
# Pour Windows PowerShell
docker-compose up --build
```

- L'application Django sera accessible sur http://localhost:8000
- Les fichiers statiques, médias et logs sont persistés dans les dossiers locaux (`./staticfiles`, `./media`, `./logs`).
- Les données PostgreSQL sont persistées dans le volume `postgres_data`.

### 3. Commandes utiles avec Docker

- **Appliquer les migrations** :
  ```powershell
  docker-compose exec web python manage.py migrate
  ```
- **Créer un superutilisateur** :
  ```powershell
  docker-compose exec web python manage.py createsuperuser
  ```
- **Collecter les fichiers statiques** :
  ```powershell
  docker-compose exec web python manage.py collectstatic --noinput
  ```
- **Accéder au shell Django** :
  ```powershell
  docker-compose exec web python manage.py shell
  ```
- **Redémarrer le service web** :
  ```powershell
  docker-compose restart web
  ```

### 4. Arrêter et supprimer les conteneurs

```powershell
docker-compose down
```

---

## 6️⃣ Conclusion

Votre blog Django est maintenant prêt pour la production ! Pour aller plus loin, consultez la [documentation officielle Django](https://docs.djangoproject.com/fr/5.2/howto/deployment/checklist/).

Merci d’utiliser MonProjet Django Blog !

[Retour au dépôt GitHub](https://github.com/Flunshield/python-monblog)
