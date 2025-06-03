#!/usr/bin/env python
"""
Script pour créer un utilisateur de test pour tester manuellement
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile

def create_test_user():
    print("🔧 Création d'un utilisateur de test")
    print("=" * 40)
    
    username = 'test_manual'
    password = 'test123'
    
    # Supprimer s'il existe déjà
    User.objects.filter(username=username).delete()
    
    # Créer l'utilisateur
    user = User.objects.create_user(
        username=username,
        email='test@manual.com',
        password=password
    )
    
    # Créer le profil
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = 'journaliste'
    profile.save()
    
    print(f"✅ Utilisateur créé: {username}")
    print(f"✅ Mot de passe: {password}")
    print(f"✅ Rôle: {profile.role}")
    print(f"")
    print(f"🌐 Vous pouvez maintenant vous connecter sur:")
    print(f"   http://127.0.0.1:8000/")
    print(f"   Username: {username}")
    print(f"   Password: {password}")
    print(f"")
    print(f"📝 Puis visitez: http://127.0.0.1:8000/ajouter_article/")
    print(f"   pour voir le champ auteur pré-rempli automatiquement!")

if __name__ == "__main__":
    create_test_user()
