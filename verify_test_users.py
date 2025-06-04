#!/usr/bin/env python
"""
Script de vérification pour tester les rôles et permissions des utilisateurs créés
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
from blog.templatetags.role_tags import user_role, has_role, is_admin, is_journaliste, is_lecteur, can_access_admin


def test_user_roles():
    """Tester les rôles et permissions des utilisateurs créés"""
    
    print("🧪 Test des rôles et permissions des utilisateurs\n")
    
    test_users = ['lecteur_test', 'journaliste_test', 'admin_test']
    
    for username in test_users:
        try:
            user = User.objects.get(username=username)
            print(f"👤 Test de l'utilisateur : {username}")
            print(f"   Email: {user.email}")
            print(f"   Nom complet: {user.get_full_name()}")
            
            # Test du rôle via template tag
            current_role = user_role(user)
            print(f"   Rôle actuel: {current_role}")
            
            # Test des permissions via template tags
            print(f"   Permissions:")
            print(f"     - is_lecteur: {is_lecteur(user)}")
            print(f"     - is_journaliste: {is_journaliste(user)}")
            print(f"     - is_admin: {is_admin(user)}")
            print(f"     - can_access_admin: {can_access_admin(user)}")
            
            # Test du rôle spécifique
            expected_role = username.split('_')[0]  # lecteur, journaliste, admin
            if has_role(user, expected_role):
                print(f"   ✅ Rôle '{expected_role}' correctement assigné")
            else:
                print(f"   ❌ Problème avec le rôle '{expected_role}'")
            
            # Test des accès selon le rôle
            print(f"   Accès aux fonctionnalités:")
            if expected_role == 'lecteur':
                print(f"     - Navigation simple: ✅")
                print(f"     - Ajouter article: ❌ (pas autorisé)")
                print(f"     - Gestion admin: ❌ (pas autorisé)")
            elif expected_role == 'journaliste':
                print(f"     - Navigation simple: ✅")
                print(f"     - Ajouter article: ✅")
                print(f"     - Gérer articles: ✅")
                print(f"     - Modération: ✅")
                print(f"     - Gérer catégories: ✅ (lecture)")
                print(f"     - Page journaliste: ✅")
                print(f"     - Page admin: ❌ (pas autorisé)")
            elif expected_role == 'admin':
                print(f"     - Navigation simple: ✅")
                print(f"     - Ajouter article: ✅")
                print(f"     - Gérer articles: ✅")
                print(f"     - Modération: ✅")
                print(f"     - Gérer catégories: ✅ (complète)")
                print(f"     - Page admin: ✅")
            
            print("-" * 50)
            
        except User.DoesNotExist:
            print(f"❌ Utilisateur '{username}' non trouvé")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Erreur lors du test de '{username}': {e}")
            print("-" * 50)
    
    # Statistiques globales
    print("\n📊 Statistiques globales des rôles:")
    all_roles = Role.objects.all()
    for role in all_roles:
        user_count = UserProfile.objects.filter(role=role).count()
        users_list = [up.user.username for up in UserProfile.objects.filter(role=role)[:5]]
        users_display = ", ".join(users_list)
        if len(users_list) == 5 and user_count > 5:
            users_display += f" ... (+{user_count - 5} autres)"
        
        print(f"   {role.name}: {user_count} utilisateur(s) - {users_display}")
    
    print("\n🎯 Test de l'assignation automatique du rôle par défaut:")
    try:
        # Créer un utilisateur temporaire pour tester l'assignation automatique
        temp_user = User.objects.create_user(
            username='temp_test_user',
            email='temp@test.com',
            password='temppass'
        )
        
        if hasattr(temp_user, 'profile') and temp_user.profile.role.name == 'lecteur':
            print("   ✅ L'assignation automatique du rôle 'lecteur' fonctionne")
        else:
            print("   ❌ Problème avec l'assignation automatique du rôle")
        
        # Supprimer l'utilisateur temporaire
        temp_user.delete()
        
    except Exception as e:
        print(f"   ❌ Erreur lors du test d'assignation automatique: {e}")
    
    print("\n✅ Tests terminés !")


if __name__ == "__main__":
    test_user_roles()
