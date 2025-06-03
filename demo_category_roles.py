#!/usr/bin/env python
"""
Script de démonstration du système de rôles pour les catégories.
Ce script crée des utilisateurs test et démontre les différents niveaux d'accès.
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile, Category
from django.test import Client

def create_demo_users():
    """Crée des utilisateurs de démonstration avec différents rôles"""
    print("🚀 Création des utilisateurs de démonstration...")
    
    # Supprimer les utilisateurs existants s'ils existent
    User.objects.filter(username__in=['demo_admin', 'demo_journalist', 'demo_reader']).delete()
    
    # Créer les utilisateurs
    admin_user = User.objects.create_user(
        username='demo_admin',
        password='admin123',
        email='admin@demo.com',
        first_name='Admin',
        last_name='Démonstration'
    )
    
    journalist_user = User.objects.create_user(
        username='demo_journalist',
        password='journalist123',
        email='journalist@demo.com',
        first_name='Journaliste',
        last_name='Démonstration'
    )
    
    reader_user = User.objects.create_user(
        username='demo_reader',
        password='reader123',
        email='reader@demo.com',
        first_name='Lecteur',
        last_name='Démonstration'
    )
    
    # Configurer les rôles
    admin_profile, _ = UserProfile.objects.get_or_create(user=admin_user)
    admin_profile.role = 'admin'
    admin_profile.save()
    
    journalist_profile, _ = UserProfile.objects.get_or_create(user=journalist_user)
    journalist_profile.role = 'journaliste'
    journalist_profile.save()
    
    reader_profile, _ = UserProfile.objects.get_or_create(user=reader_user)
    reader_profile.role = 'lecteur'
    reader_profile.save()
    
    print("✅ Utilisateurs créés avec succès !")
    print(f"   👑 Admin: {admin_user.username} (rôle: {admin_profile.role})")
    print(f"   ✍️  Journaliste: {journalist_user.username} (rôle: {journalist_profile.role})")
    print(f"   👀 Lecteur: {reader_user.username} (rôle: {reader_profile.role})")
    
    return admin_user, journalist_user, reader_user

def create_demo_categories():
    """Crée des catégories de démonstration"""
    print("\n📁 Création de catégories de démonstration...")
    
    categories = [
        {'nom': 'Technologie', 'description': 'Articles sur les nouvelles technologies'},
        {'nom': 'Sciences', 'description': 'Découvertes scientifiques et recherche'},
        {'nom': 'Culture', 'description': 'Art, littérature et événements culturels'},
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            nom=cat_data['nom'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"   ✅ Catégorie créée: {category.nom}")
        else:
            print(f"   📁 Catégorie existante: {category.nom}")
        created_categories.append(category)
    
    return created_categories

def test_access_permissions():
    """Teste les permissions d'accès pour chaque rôle"""
    print("\n🔐 Test des permissions d'accès...")
    
    client = Client()
    
    # Test pour l'administrateur
    print("\n👑 Test accès ADMINISTRATEUR:")
    client.login(username='demo_admin', password='admin123')
    
    # Test accès à la gestion des catégories
    response = client.get('/gerer-categories/')
    if response.status_code == 200:
        print("   ✅ Peut accéder à la gestion des catégories")
        if 'Ajouter une catégorie' in response.content.decode():
            print("   ✅ Peut voir le bouton 'Ajouter une catégorie'")
        else:
            print("   ❌ Ne peut pas voir le bouton 'Ajouter une catégorie'")
    else:
        print(f"   ❌ Accès refusé à la gestion des catégories (code: {response.status_code})")
    
    client.logout()
    
    # Test pour le journaliste
    print("\n✍️ Test accès JOURNALISTE:")
    client.login(username='demo_journalist', password='journalist123')
    
    response = client.get('/gerer-categories/')
    if response.status_code == 200:
        print("   ✅ Peut accéder à la gestion des catégories (consultation)")
        if 'Mode consultation' in response.content.decode():
            print("   ✅ Voit le badge 'Mode consultation'")
        else:
            print("   ❌ Ne voit pas le badge 'Mode consultation'")
        
        if 'Ajouter une catégorie' not in response.content.decode():
            print("   ✅ Ne peut pas voir le bouton 'Ajouter une catégorie' (correct)")
        else:
            print("   ❌ Peut voir le bouton 'Ajouter une catégorie' (incorrect)")
    else:
        print(f"   ❌ Accès refusé à la gestion des catégories (code: {response.status_code})")
    
    # Test d'accès aux actions interdites
    response = client.get('/ajouter-categorie/')
    if response.status_code == 403:
        print("   ✅ Accès refusé à l'ajout de catégorie (correct)")
    else:
        print(f"   ❌ Peut accéder à l'ajout de catégorie (code: {response.status_code})")
    
    client.logout()
    
    # Test pour le lecteur
    print("\n👀 Test accès LECTEUR:")
    client.login(username='demo_reader', password='reader123')
    
    response = client.get('/gerer-categories/')
    if response.status_code == 403:
        print("   ✅ Accès refusé à la gestion des catégories (correct)")
    else:
        print(f"   ❌ Peut accéder à la gestion des catégories (code: {response.status_code})")
    
    client.logout()

def show_navigation_differences():
    """Montre les différences dans la navigation selon les rôles"""
    print("\n🧭 Test de la navigation selon les rôles...")
    
    client = Client()
    
    roles = [
        ('demo_admin', 'admin123', '👑 ADMIN'),
        ('demo_journalist', 'journalist123', '✍️ JOURNALISTE'),
        ('demo_reader', 'reader123', '👀 LECTEUR')
    ]
    
    for username, password, role_name in roles:
        print(f"\n{role_name}:")
        client.login(username=username, password=password)
        response = client.get('/')
        
        content = response.content.decode()
        
        # Vérifier la présence des liens dans la navigation
        nav_items = [
            ('Nouvel Article', '/ajouter/'),
            ('Gérer Articles', '/gerer-articles/'),
            ('Catégories', '/gerer-categories/'),
            ('Admin', '/admin-page/'),
            ('Journaliste', '/journaliste-page/')
        ]
        
        for item_name, item_url in nav_items:
            if item_url in content:
                print(f"   ✅ Voit: {item_name}")
            else:
                print(f"   ❌ Ne voit pas: {item_name}")
        
        client.logout()

def main():
    """Fonction principale de démonstration"""
    print("=" * 60)
    print("🎭 DÉMONSTRATION DU SYSTÈME DE RÔLES - CATÉGORIES")
    print("=" * 60)
    
    try:
        # Créer les données de test
        admin_user, journalist_user, reader_user = create_demo_users()
        categories = create_demo_categories()
        
        # Tester les permissions
        test_access_permissions()
        
        # Montrer les différences de navigation
        show_navigation_differences()
        
        print("\n" + "=" * 60)
        print("✅ DÉMONSTRATION TERMINÉE AVEC SUCCÈS !")
        print("=" * 60)
        print("\n📋 RÉSUMÉ DES FONCTIONNALITÉS:")
        print("   👑 ADMIN: Accès complet (voir, ajouter, modifier, supprimer)")
        print("   ✍️  JOURNALISTE: Accès lecture seule (voir les catégories)")
        print("   👀 LECTEUR: Aucun accès aux catégories")
        print("\n🔗 Pour tester manuellement:")
        print("   1. Démarrez le serveur: python manage.py runserver")
        print("   2. Connectez-vous avec l'un des comptes:")
        print("      - demo_admin / admin123")
        print("      - demo_journalist / journalist123")
        print("      - demo_reader / reader123")
        print("   3. Naviguez vers /gerer-categories/ pour voir les différences")
        
    except Exception as e:
        print(f"\n❌ ERREUR pendant la démonstration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
