#!/usr/bin/env python
"""
Script pour changer le rôle d'un utilisateur de lecteur à journaliste
Usage: python change_user_role.py
"""

import os
import sys
import django

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile, Role

def change_user_role_to_journalist(user_id):
    """Change le rôle d'un utilisateur vers journaliste"""
    try:
        # Récupérer l'utilisateur
        user = User.objects.get(id=user_id)
        print(f"Utilisateur trouvé: {user.username} (ID: {user.id})")
        
        # Récupérer ou créer le profil
        profile, created = UserProfile.objects.get_or_create(user=user)
        if created:
            print("Profil créé pour l'utilisateur")
        
        # Afficher le rôle actuel
        print(f"Rôle actuel: {profile.role.name}")
        
        # Récupérer le rôle journaliste
        default_roles = Role.get_default_roles()
        journalist_role = default_roles['journaliste']
        
        # Changer le rôle
        profile.role = journalist_role
        profile.save()
        
        print(f"✅ Rôle changé avec succès!")
        print(f"Nouveau rôle: {profile.role.name}")
        
        return True
        
    except User.DoesNotExist:
        print(f"❌ Utilisateur avec l'ID {user_id} non trouvé")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du changement de rôle: {e}")
        return False

def show_user_info(user_id):
    """Affiche les informations de l'utilisateur"""
    try:
        user = User.objects.get(id=user_id)
        profile = user.profile
        print(f"\n📋 Informations utilisateur:")
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Rôle: {profile.role.name}")
        print(f"Date création: {user.date_joined}")
        print(f"Dernière connexion: {user.last_login}")
        
    except User.DoesNotExist:
        print(f"❌ Utilisateur avec l'ID {user_id} non trouvé")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    USER_ID = 2
    
    print("🔄 Changement de rôle utilisateur")
    print("=" * 40)
    
    # Afficher les infos avant
    print("AVANT:")
    show_user_info(USER_ID)
    
    # Changer le rôle
    print(f"\n🔄 Changement du rôle pour l'utilisateur ID {USER_ID}...")
    success = change_user_role_to_journalist(USER_ID)
    
    if success:
        # Afficher les infos après
        print("\nAPRÈS:")
        show_user_info(USER_ID)
    
    print("\n" + "=" * 40)
    print("✨ Script terminé")
