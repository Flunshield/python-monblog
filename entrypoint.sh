#!/bin/bash
set -e

# Attendre que la base de données soit prête
echo "Attente de la base de données..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Base de données prête !"

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

# Collecter les fichiers statiques
echo "Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# Compiler les messages de traduction
echo "Compilation des traductions..."
python manage.py compilemessages || true

# Démarrer Gunicorn
echo "Démarrage de Gunicorn..."
exec gunicorn monprojet.wsgi --config gunicorn_config.py
