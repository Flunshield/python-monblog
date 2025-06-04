#!/bin/bash
set -e

# Attendre que la base de données soit prête
echo "🔄 Attente de la base de données..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ Base de données prête !"

# Appliquer les migrations
echo "🔄 Application des migrations..."
python manage.py migrate

# Seeding intelligent des données
echo "🔄 Vérification et seeding des données..."

# Vérifier si les données de base existent
ROLES_COUNT=$(python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()
from blog.models import Role
print(Role.objects.count())
" 2>/dev/null || echo "0")

CATEGORIES_COUNT=$(python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()
from blog.models import Category
print(Category.objects.count())
" 2>/dev/null || echo "0")

USERS_COUNT=$(python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()
from django.contrib.auth.models import User
print(User.objects.count())
" 2>/dev/null || echo "0")

echo "📊 État actuel - Rôles: $ROLES_COUNT, Catégories: $CATEGORIES_COUNT, Utilisateurs: $USERS_COUNT"

# Seeding conditionnel
if [ "$ROLES_COUNT" = "0" ] || [ "$CATEGORIES_COUNT" = "0" ]; then
    echo "🌱 Seeding des données de base requis..."
    
    # Créer les rôles et catégories de base
    python manage.py seed_roles || echo "⚠️ Erreur lors du seeding des rôles"
    python manage.py seed_categories || echo "⚠️ Erreur lors du seeding des catégories"
    
    # Créer les utilisateurs de production si aucun n'existe
    if [ "$USERS_COUNT" = "0" ]; then
        echo "👥 Création des comptes de production..."
        ADMIN_PASSWORD="${DJANGO_ADMIN_PASSWORD:-ProdAdmin2024!}"
        python manage.py seed_users --password "$ADMIN_PASSWORD" || echo "⚠️ Erreur lors du seeding des utilisateurs"
        echo "🔑 Mot de passe admin: $ADMIN_PASSWORD"
    fi
    
    # Mode développement : ajouter du contenu d'exemple
    if [ "${DJANGO_DEBUG:-False}" = "True" ]; then
        echo "🚧 Mode développement détecté - ajout de contenu d'exemple..."
        python manage.py seed_articles --count 15 || echo "⚠️ Erreur lors du seeding des articles"
        python manage.py seed_comments --count 30 || echo "⚠️ Erreur lors du seeding des commentaires"
        python manage.py seed_likes --count 50 || echo "⚠️ Erreur lors du seeding des likes"
    fi
    
    echo "✅ Seeding terminé !"
else
    echo "✅ Données de base déjà présentes - seeding ignoré"
fi

# Collecter les fichiers statiques
echo "🔄 Collection des fichiers statiques..."
python manage.py collectstatic --noinput

# Compiler les messages de traduction
echo "🔄 Compilation des traductions..."
python manage.py compilemessages || true

# Démarrer Gunicorn
echo "🚀 Démarrage de Gunicorn..."
exec gunicorn monprojet.wsgi --config gunicorn_config.py
