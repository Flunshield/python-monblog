#!/usr/bin/env python
"""
Test complet pour vérifier la nouvelle gestion dynamique des rôles via la base de données.
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile, Role
from blog.templatetags.role_tags import user_role, has_role, is_admin, is_journaliste, is_lecteur


def test_role_model():
    """Test du modèle Role et ses méthodes"""
    print("=== Test du modèle Role ===")
    
    # Vérifier que les rôles par défaut sont créés
    roles = Role.get_default_roles()
    assert 'lecteur' in roles, "Le rôle lecteur n'existe pas"
    assert 'journaliste' in roles, "Le rôle journaliste n'existe pas"
    assert 'admin' in roles, "Le rôle admin n'existe pas"
    
    # Vérifier que les objets sont bien créés en base
    assert Role.objects.filter(name='lecteur').exists(), "Rôle lecteur non trouvé en base"
    assert Role.objects.filter(name='journaliste').exists(), "Rôle journaliste non trouvé en base"
    assert Role.objects.filter(name='admin').exists(), "Rôle admin non trouvé en base"
    
    print("✅ Modèle Role et rôles par défaut OK")
    return roles


def test_user_profile_creation_with_new_model():
    """Test de création automatique des profils utilisateur avec le nouveau modèle"""
    print("\n=== Test de création des profils utilisateur avec nouveau modèle ===")
    
    # Nettoyer d'abord
    test_username = "test_user_new_roles"
    if User.objects.filter(username=test_username).exists():
        User.objects.filter(username=test_username).delete()
    
    # Créer un utilisateur
    user = User.objects.create_user(
        username=test_username,
        email="test@newroles.com",
        password="testpass123"
    )
    
    # Vérifier que le profil a été créé automatiquement
    assert hasattr(user, 'profile'), "Le profil utilisateur n'a pas été créé automatiquement"
    assert user.profile.role.name == 'lecteur', f"Le rôle par défaut devrait être 'lecteur', mais c'est '{user.profile.role.name}'"
    
    print(f"✅ Utilisateur créé : {user.username}")
    print(f"✅ Profil créé automatiquement avec le rôle : {user.profile.role.name}")
    
    return user


def test_role_changes_with_new_model(user):
    """Test des changements de rôles avec le nouveau modèle"""
    print("\n=== Test des changements de rôles avec nouveau modèle ===")
    
    roles = Role.get_default_roles()
    
    # Test changement vers journaliste
    user.profile.role = roles['journaliste']
    user.profile.save()
    user.refresh_from_db()
    assert user.profile.role.name == 'journaliste', "Le changement vers journaliste a échoué"
    print(f"✅ Changement vers journaliste réussi : {user.profile.role.name}")
    
    # Test changement vers admin
    user.profile.role = roles['admin']
    user.profile.save()
    user.refresh_from_db()
    assert user.profile.role.name == 'admin', "Le changement vers admin a échoué"
    print(f"✅ Changement vers admin réussi : {user.profile.role.name}")
    
    # Test retour vers lecteur
    user.profile.role = roles['lecteur']
    user.profile.save()
    user.refresh_from_db()
    assert user.profile.role.name == 'lecteur', "Le retour vers lecteur a échoué"
    print(f"✅ Retour vers lecteur réussi : {user.profile.role.name}")


def test_template_tags_with_new_model(user):
    """Test des template tags avec le nouveau modèle"""
    print("\n=== Test des template tags avec nouveau modèle ===")
    
    roles = Role.get_default_roles()
    
    # Test avec rôle lecteur
    user.profile.role = roles['lecteur']
    user.profile.save()
    
    assert user_role(user) == 'lecteur', "user_role ne retourne pas le bon rôle"
    assert has_role(user, 'lecteur'), "has_role ne fonctionne pas pour lecteur"
    assert not has_role(user, 'admin'), "has_role devrait être False pour admin"
    assert is_lecteur(user), "is_lecteur devrait être True"
    assert not is_journaliste(user), "is_journaliste devrait être False"
    assert not is_admin(user), "is_admin devrait être False"
    print("✅ Template tags pour lecteur OK")
    
    # Test avec rôle journaliste
    user.profile.role = roles['journaliste']
    user.profile.save()
    
    assert user_role(user) == 'journaliste', "user_role ne retourne pas le bon rôle"
    assert has_role(user, 'journaliste'), "has_role ne fonctionne pas pour journaliste"
    assert not is_lecteur(user), "is_lecteur devrait être False"
    assert is_journaliste(user), "is_journaliste devrait être True"
    assert not is_admin(user), "is_admin devrait être False"
    print("✅ Template tags pour journaliste OK")
    
    # Test avec rôle admin
    user.profile.role = roles['admin']
    user.profile.save()
    
    assert user_role(user) == 'admin', "user_role ne retourne pas le bon rôle"
    assert has_role(user, 'admin'), "has_role ne fonctionne pas pour admin"
    assert not is_lecteur(user), "is_lecteur devrait être False"
    assert not is_journaliste(user), "is_journaliste devrait être False"
    assert is_admin(user), "is_admin devrait être True"
    print("✅ Template tags pour admin OK")


def test_view_role_checks():
    """Test des vérifications de rôles dans les vues"""
    print("\n=== Test des vérifications de rôles dans les vues ===")
    
    from django.test import Client
    from django.urls import reverse
    
    client = Client()
    
    # Créer un utilisateur de test
    test_username = "test_view_roles"
    if User.objects.filter(username=test_username).exists():
        User.objects.filter(username=test_username).delete()
    
    user = User.objects.create_user(
        username=test_username,
        email="test@viewroles.com", 
        password="testpass123"
    )
    
    roles = Role.get_default_roles()
    client.force_login(user)
    
    # Test accès page admin avec rôle lecteur
    user.profile.role = roles['lecteur']
    user.profile.save()
    
    response = client.get(reverse('page_admin'))
    assert response.status_code == 403, "Un lecteur ne devrait pas pouvoir accéder à la page admin"
    print("✅ Accès refusé à la page admin pour lecteur")
    
    # Test accès page admin avec rôle admin
    user.profile.role = roles['admin']
    user.profile.save()
    
    response = client.get(reverse('page_admin'))
    assert response.status_code == 200, "Un admin devrait pouvoir accéder à la page admin"
    print("✅ Accès accordé à la page admin pour admin")
    
    # Nettoyer
    user.delete()


def cleanup():
    """Nettoyage des données de test"""
    print("\n=== Nettoyage ===")
    
    # Supprimer les utilisateurs de test
    test_usernames = ["test_user_new_roles", "test_view_roles"]
    for username in test_usernames:
        if User.objects.filter(username=username).exists():
            User.objects.filter(username=username).delete()
            print(f"✅ Utilisateur {username} supprimé")


def main():
    """Fonction principale de test"""
    print("🧪 TEST COMPLET DE LA NOUVELLE GESTION DYNAMIQUE DES RÔLES")
    print("=" * 60)
    
    try:
        # Tests du modèle Role
        roles = test_role_model()
        
        # Tests de création de profil
        user = test_user_profile_creation_with_new_model()
        
        # Tests de changement de rôles
        test_role_changes_with_new_model(user)
        
        # Tests des template tags
        test_template_tags_with_new_model(user)
        
        # Tests des vues
        test_view_role_checks()
        
        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
        print("✅ La gestion dynamique des rôles via la base de données fonctionne parfaitement")
        print("✅ Les modèles Role et UserProfile sont correctement configurés")
        print("✅ Les template tags utilisent la nouvelle structure")
        print("✅ Les vues vérifient correctement les rôles")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR DANS LES TESTS : {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        cleanup()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
