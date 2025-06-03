#!/usr/bin/env python
"""
Script de test pour vérifier le fonctionnement du système de rôles.
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile

def test_user_profile_creation():
    """Test de création automatique des profils utilisateur"""
    print("=== Test de création des profils utilisateur ===")
    
    # Créer un utilisateur de test
    test_username = "test_user_roles"
    if User.objects.filter(username=test_username).exists():
        User.objects.filter(username=test_username).delete()
    
    user = User.objects.create_user(
        username=test_username,
        email="test@example.com",
        password="testpass123"
    )
    
    # Vérifier que le profil a été créé automatiquement
    assert hasattr(user, 'profile'), "Le profil utilisateur n'a pas été créé automatiquement"
    assert user.profile.role == 'lecteur', f"Le rôle par défaut devrait être 'lecteur', mais c'est '{user.profile.role}'"
    
    print(f"✅ Utilisateur créé : {user.username}")
    print(f"✅ Profil créé automatiquement avec le rôle : {user.profile.role}")
    
    return user

def test_role_changes():
    """Test des changements de rôles"""
    print("\n=== Test des changements de rôles ===")
    
    user = test_user_profile_creation()
    
    # Test changement vers journaliste
    user.profile.role = 'journaliste'
    user.profile.save()
    user.refresh_from_db()
    assert user.profile.role == 'journaliste', "Le changement vers journaliste a échoué"
    print(f"✅ Changement vers journaliste réussi : {user.profile.role}")
    
    # Test changement vers admin
    user.profile.role = 'admin'
    user.profile.save()
    user.refresh_from_db()
    assert user.profile.role == 'admin', "Le changement vers admin a échoué"
    print(f"✅ Changement vers admin réussi : {user.profile.role}")
    
    # Test retour vers lecteur
    user.profile.role = 'lecteur'
    user.profile.save()
    user.refresh_from_db()
    assert user.profile.role == 'lecteur', "Le retour vers lecteur a échoué"
    print(f"✅ Retour vers lecteur réussi : {user.profile.role}")
    
    return user

def test_role_validation():
    """Test de validation des rôles"""
    print("\n=== Test de validation des rôles ===")
    
    user = User.objects.get(username="test_user_roles")
    
    # Tester les rôles valides
    valid_roles = ['lecteur', 'journaliste', 'admin']
    for role in valid_roles:
        user.profile.role = role
        user.profile.save()
        user.refresh_from_db()
        assert user.profile.role == role, f"Le rôle {role} n'a pas été sauvegardé correctement"
        print(f"✅ Rôle {role} validé")

def test_template_tags():
    """Test des template tags de rôles"""
    print("\n=== Test des template tags ===")
    
    from blog.templatetags.role_tags import user_role, has_role, can_access_admin, is_admin, is_journaliste, is_lecteur
    
    user = User.objects.get(username="test_user_roles")
    
    # Test avec rôle lecteur
    user.profile.role = 'lecteur'
    user.profile.save()
    
    assert user_role(user) == 'lecteur', "user_role ne retourne pas le bon rôle"
    assert has_role(user, 'lecteur'), "has_role ne fonctionne pas pour lecteur"
    assert not can_access_admin(user), "can_access_admin devrait être False pour lecteur"
    assert is_lecteur(user), "is_lecteur devrait être True"
    assert not is_journaliste(user), "is_journaliste devrait être False"
    assert not is_admin(user), "is_admin devrait être False"
    print("✅ Template tags pour lecteur OK")
    
    # Test avec rôle journaliste
    user.profile.role = 'journaliste'
    user.profile.save()
    
    assert user_role(user) == 'journaliste', "user_role ne retourne pas le bon rôle"
    assert has_role(user, 'journaliste'), "has_role ne fonctionne pas pour journaliste"
    assert can_access_admin(user), "can_access_admin devrait être True pour journaliste"
    assert not is_lecteur(user), "is_lecteur devrait être False"
    assert is_journaliste(user), "is_journaliste devrait être True"
    assert not is_admin(user), "is_admin devrait être False"
    print("✅ Template tags pour journaliste OK")
    
    # Test avec rôle admin
    user.profile.role = 'admin'
    user.profile.save()
    
    assert user_role(user) == 'admin', "user_role ne retourne pas le bon rôle"
    assert has_role(user, 'admin'), "has_role ne fonctionne pas pour admin"
    assert can_access_admin(user), "can_access_admin devrait être True pour admin"
    assert not is_lecteur(user), "is_lecteur devrait être False"
    assert not is_journaliste(user), "is_journaliste devrait être False"
    assert is_admin(user), "is_admin devrait être True"
    print("✅ Template tags pour admin OK")

def test_views_access():
    """Test d'accès aux vues selon les rôles"""
    print("\n=== Test d'accès aux vues ===")
    
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    user = User.objects.get(username="test_user_roles")
    
    # Connexion de l'utilisateur
    client.force_login(user)
    
    # Test accès page admin avec rôle lecteur
    user.profile.role = 'lecteur'
    user.profile.save()
    
    response = client.get(reverse('page_admin'))
    assert response.status_code == 403, "Un lecteur ne devrait pas pouvoir accéder à la page admin"
    print("✅ Accès refusé à la page admin pour lecteur")
    
    # Test accès page journaliste avec rôle lecteur
    response = client.get(reverse('page_journaliste'))
    assert response.status_code == 403, "Un lecteur ne devrait pas pouvoir accéder à la page journaliste"
    print("✅ Accès refusé à la page journaliste pour lecteur")
    
    # Test accès page journaliste avec rôle journaliste
    user.profile.role = 'journaliste'
    user.profile.save()
    
    response = client.get(reverse('page_journaliste'))
    assert response.status_code == 200, "Un journaliste devrait pouvoir accéder à la page journaliste"
    print("✅ Accès accordé à la page journaliste pour journaliste")
    
    # Test accès page admin avec rôle journaliste
    response = client.get(reverse('page_admin'))
    assert response.status_code == 403, "Un journaliste ne devrait pas pouvoir accéder à la page admin"
    print("✅ Accès refusé à la page admin pour journaliste")
    
    # Test accès page admin avec rôle admin
    user.profile.role = 'admin'
    user.profile.save()
    
    response = client.get(reverse('page_admin'))
    assert response.status_code == 200, "Un admin devrait pouvoir accéder à la page admin"
    print("✅ Accès accordé à la page admin pour admin")
    
    response = client.get(reverse('page_journaliste'))
    assert response.status_code == 200, "Un admin devrait pouvoir accéder à la page journaliste"
    print("✅ Accès accordé à la page journaliste pour admin")

def test_role_change_view():
    """Test de la vue de changement de rôle"""
    print("\n=== Test de la vue de changement de rôle ===")
    
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    user = User.objects.get(username="test_user_roles")
    client.force_login(user)
    
    # Test changement vers journaliste
    response = client.post(reverse('set_role'), {'role': 'journaliste'})
    assert response.status_code == 302, "La vue set_role devrait rediriger"
    
    user.refresh_from_db()
    assert user.profile.role == 'journaliste', "Le rôle n'a pas été changé vers journaliste"
    print("✅ Changement de rôle via vue réussi")
    
    # Test rôle invalide
    old_role = user.profile.role
    response = client.post(reverse('set_role'), {'role': 'invalid_role'})
    user.refresh_from_db()
    assert user.profile.role == old_role, "Le rôle ne devrait pas changer avec une valeur invalide"
    print("✅ Rôle invalide rejeté correctement")

def cleanup():
    """Nettoyage des données de test"""
    print("\n=== Nettoyage ===")
    User.objects.filter(username="test_user_roles").delete()
    print("✅ Données de test supprimées")

def main():
    """Fonction principale de test"""
    print("🚀 Début des tests du système de rôles\n")
    
    try:
        test_user_profile_creation()
        test_role_changes()
        test_role_validation()
        test_template_tags()
        test_views_access()
        test_role_change_view()
        
        print("\n🎉 Tous les tests ont réussi !")
        print("✅ Le système de rôles fonctionne correctement")
        
    except AssertionError as e:
        print(f"\n❌ Test échoué : {e}")
        return False
    except Exception as e:
        print(f"\n💥 Erreur inattendue : {e}")
        return False
    finally:
        cleanup()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)