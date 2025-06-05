#!/usr/bin/env python
"""
Script pour créer 3 utilisateurs de test avec des rôles différents :
- lecteur_test (rôle: lecteur)
- journaliste_test (rôle: journaliste)  
- admin_test (rôle: admin)
"""

import os
import sys
import django

# Configuration de l'environnement Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile, Role


def create_test_users():
    """Créer 3 utilisateurs de test avec des rôles différents"""
    
    print("🚀 Création des utilisateurs de test...")
    
    # S'assurer que les rôles par défaut existent
    default_roles = Role.get_default_roles()
    print(f"✅ Rôles disponibles : {list(default_roles.keys())}")
    
    # Définition des utilisateurs à créer
    users_to_create = [
        {
            'username': 'lecteur_test',
            'email': 'lecteur@test.com',
            'password': 'testpass123',
            'first_name': 'Jean',
            'last_name': 'Lecteur',
            'role': 'lecteur'
        },
        {
            'username': 'journaliste_test', 
            'email': 'journaliste@test.com',
            'password': 'testpass123',
            'first_name': 'Marie',
            'last_name': 'Journaliste',
            'role': 'journaliste'
        },
        {
            'username': 'admin_test',
            'email': 'admin@test.com', 
            'password': 'testpass123',
            'first_name': 'Pierre',
            'last_name': 'Admin',
            'role': 'admin'
        }
    ]
    
    created_users = []
    
    for user_data in users_to_create:
        try:
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=user_data['username']).exists():
                print(f"⚠️  L'utilisateur '{user_data['username']}' existe déjà")
                # Récupérer l'utilisateur existant
                user = User.objects.get(username=user_data['username'])
                
                # Mettre à jour son rôle si nécessaire
                if hasattr(user, 'profile'):
                    current_role = user.profile.role.name
                    if current_role != user_data['role']:
                        user.profile.role = default_roles[user_data['role']]
                        user.profile.save()
                        print(f"  ✅ Rôle mis à jour de '{current_role}' vers '{user_data['role']}'")
                    else:
                        print(f"  ✅ Rôle '{current_role}' déjà correct")
                else:
                    # Créer le profil manquant
                    UserProfile.objects.create(user=user, role=default_roles[user_data['role']])
                    print(f"  ✅ Profil créé avec le rôle '{user_data['role']}'")
                
                created_users.append(user)
                continue
            
            # Créer le nouvel utilisateur
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            
            # Le signal post_save devrait créer automatiquement un profil avec le rôle 'lecteur'
            # Mais nous devons modifier le rôle si ce n'est pas 'lecteur'
            if user_data['role'] != 'lecteur':
                user.profile.role = default_roles[user_data['role']]
                user.profile.save()
            
            created_users.append(user)
            print(f"✅ Utilisateur '{user_data['username']}' créé avec le rôle '{user_data['role']}'")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'utilisateur '{user_data['username']}': {e}")
            continue
    
    print(f"\n📊 Résumé : {len(created_users)} utilisateurs traités")
    
    # Afficher un récapitulatif
    print("\n📋 Récapitulatif des utilisateurs :")
    print("-" * 60)
    print(f"{'Username':<20} {'Email':<25} {'Rôle':<15}")
    print("-" * 60)
    
    for user in created_users:
        if hasattr(user, 'profile'):
            role_name = user.profile.role.name
        else:
            role_name = "Pas de profil"
        
        print(f"{user.username:<20} {user.email:<25} {role_name:<15}")
    
    print("-" * 60)
    
    # Vérifier les rôles en base
    print("\n🔍 Vérification des rôles en base :")
    for role_name, role_obj in default_roles.items():
        user_count = UserProfile.objects.filter(role=role_obj).count()
        print(f"  - {role_name}: {user_count} utilisateur(s)")
    
    print("\n✅ Script terminé avec succès !")
    print("\n💡 Informations de connexion :")
    print("   - Tous les mots de passe : testpass123")
    print("   - URLs utiles :")
    print("     - Connexion : /login/")
    print("     - Admin Django : /admin/")
    print("     - Profil : /profile/")


if __name__ == "__main__":
    create_test_users()
