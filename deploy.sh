#!/bin/bash
set -e

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Compiler les messages de traduction
python manage.py compilemessages

# Démarrer Gunicorn
exec gunicorn monprojet.wsgi --config gunicorn_config.py
