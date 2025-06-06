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

# Seeding des données essentielles pour la production
echo "Seeding des données de production..."
python manage.py seed_production --skip-if-exists --admin-password "${DJANGO_ADMIN_PASSWORD:-ProdAdmin2024!}"

# Collecter les fichiers statiques
echo "Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# Compiler les messages de traduction
echo "Compilation des traductions..."
python manage.py compilemessages || true

# Correction des permissions sur les logs (utile si volume monté)
chown -R django:django /app/logs || true

# Démarrer Gunicorn
echo "Démarrage de Gunicorn..."
exec gunicorn monprojet.wsgi --config gunicorn_config.py
