#!/usr/bin/env python3
"""
Script pour tester les permissions des articles.
Ce script vérifie que seuls les journalistes et admins peuvent 
modifier/supprimer leurs articles respectifs.
"""

import os
import django
import sys

# Configuration Django
sys.path.append('c:\\Users\\jbert\\Documents\\python isitech\\monprojet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Category, UserProfile
from django.test import Client
from django.urls import reverse

def create_test_data():
    """Créer des données de test"""
    print("🔧 Création des données de test...")
    
    # Créer des utilisateurs avec différents rôles
    users_data = [
        {'username': 'lecteur1', 'role': 'lecteur'},
        {'username': 'journaliste1', 'role': 'journaliste'},
        {'username': 'admin1', 'role': 'admin'},
    ]
    
    users = {}
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': f"{user_data['username']}@test.com",
                'first_name': user_data['username'].title(),
                'password': 'testpass123'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
        
        # Créer ou mettre à jour le profil
        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = user_data['role']
        profile.save()
        
        users[user_data['role']] = user
        print(f"   ✅ Utilisateur {user.username} créé avec le rôle {user_data['role']}")
    
    # Créer une catégorie de test
    category, created = Category.objects.get_or_create(
        nom="Test Category",
        defaults={'description': 'Catégorie pour les tests'}
    )
    if created:
        print(f"   ✅ Catégorie '{category.nom}' créée")
    
    # Créer des articles de test
    articles_data = [
        {'titre': 'Article du journaliste', 'auteur': 'journaliste1'},
        {'titre': 'Article de l\'admin', 'auteur': 'admin1'},
        {'titre': 'Ancien article', 'auteur': 'ancien_auteur'},
    ]
    
    articles = {}
    for article_data in articles_data:
        article, created = Article.objects.get_or_create(
            titre=article_data['titre'],
            defaults={
                'contenu': f"Contenu de l'article: {article_data['titre']}",
                'auteur': article_data['auteur'],
                'category': category
            }
        )
        articles[article_data['auteur']] = article
        if created:
            print(f"   ✅ Article '{article.titre}' créé par {article.auteur}")
    
    return users, articles, category

def test_home_page_permissions():
    """Tester les permissions sur la page d'accueil"""
    print("\n🧪 Test des permissions sur la page d'accueil...")
    
    users, articles, category = create_test_data()
    client = Client()
    
    # Test pour chaque type d'utilisateur
    for role, user in users.items():
        print(f"\n   📋 Test pour {role} ({user.username}):")
        
        # Connexion de l'utilisateur
        client.login(username=user.username, password='testpass123')
        
        # Récupérer la page d'accueil
        response = client.get('/')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Compter les boutons de modification/suppression visibles
            modify_buttons = content.count('btn-outline-warning')  # Boutons modifier
            delete_buttons = content.count('btn-outline-danger')   # Boutons supprimer
            
            print(f"      - Boutons 'Modifier' visibles: {modify_buttons}")
            print(f"      - Boutons 'Supprimer' visibles: {delete_buttons}")
            
            # Vérifications selon le rôle
            if role == 'lecteur':
                if modify_buttons == 0 and delete_buttons == 0:
                    print("      ✅ CORRECT: Aucun bouton de gestion visible pour le lecteur")
                else:
                    print("      ❌ ERREUR: Le lecteur ne devrait voir aucun bouton de gestion")
            
            elif role == 'journaliste':
                # Le journaliste ne devrait voir que les boutons pour ses propres articles
                expected_buttons = len([a for a in articles.values() if a.auteur == user.username])
                if modify_buttons == expected_buttons and delete_buttons == expected_buttons:
                    print(f"      ✅ CORRECT: {expected_buttons} bouton(s) visible(s) pour les articles du journaliste")
                else:
                    print(f"      ❌ ERREUR: Attendu {expected_buttons} boutons, trouvé {modify_buttons} modifier et {delete_buttons} supprimer")
            
            elif role == 'admin':
                # L'admin devrait voir tous les boutons
                total_articles = Article.objects.count()
                if modify_buttons == total_articles and delete_buttons == total_articles:
                    print(f"      ✅ CORRECT: {total_articles} bouton(s) visible(s) pour tous les articles (admin)")
                else:
                    print(f"      ❌ ERREUR: Attendu {total_articles} boutons, trouvé {modify_buttons} modifier et {delete_buttons} supprimer")
        else:
            print(f"      ❌ ERREUR: Code de réponse {response.status_code}")
        
        client.logout()

def test_direct_access_permissions():
    """Tester l'accès direct aux URLs de modification/suppression"""
    print("\n🧪 Test de l'accès direct aux URLs...")
    
    users, articles, category = create_test_data()
    client = Client()
    
    # Récupérer un article pour les tests
    test_article = articles['journaliste1']  # Article du journaliste
    
    # Tests pour chaque utilisateur
    for role, user in users.items():
        print(f"\n   📋 Test d'accès direct pour {role} ({user.username}):")
        
        client.login(username=user.username, password='testpass123')
        
        # Test d'accès à la modification d'un article qui n'appartient pas à l'utilisateur
        if role != 'admin' and user.username != test_article.auteur:
            # Accès à la modification (devrait être interdit)
            modify_url = reverse('modifier_article', args=[test_article.id])
            response = client.get(modify_url)
            
            if response.status_code == 403:
                print("      ✅ CORRECT: Accès interdit à la modification")
            else:
                print(f"      ❌ ERREUR: Accès autorisé (code {response.status_code}) alors qu'il devrait être interdit")
            
            # Accès à la suppression (devrait être interdit)
            delete_url = reverse('supprimer_article', args=[test_article.id])
            response = client.get(delete_url)
            
            if response.status_code == 403:
                print("      ✅ CORRECT: Accès interdit à la suppression")
            else:
                print(f"      ❌ ERREUR: Accès autorisé (code {response.status_code}) alors qu'il devrait être interdit")
        
        elif user.username == test_article.auteur or role == 'admin':
            # L'utilisateur devrait avoir accès à ses propres articles ou être admin
            modify_url = reverse('modifier_article', args=[test_article.id])
            response = client.get(modify_url)
            
            if response.status_code == 200:
                print("      ✅ CORRECT: Accès autorisé à la modification")
            else:
                print(f"      ❌ ERREUR: Accès refusé (code {response.status_code}) alors qu'il devrait être autorisé")
        
        client.logout()

def test_anonymous_user():
    """Tester qu'un utilisateur non connecté ne peut rien faire"""
    print("\n🧪 Test pour utilisateur anonyme...")
    
    users, articles, category = create_test_data()
    client = Client()
    
    test_article = articles['journaliste1']
    
    # Test d'accès sans connexion
    modify_url = reverse('modifier_article', args=[test_article.id])
    response = client.get(modify_url)
    
    if response.status_code == 302:  # Redirection vers login
        print("   ✅ CORRECT: Utilisateur anonyme redirigé vers la connexion")
    else:
        print(f"   ❌ ERREUR: Code de réponse {response.status_code} au lieu de redirection")

def main():
    """Fonction principale"""
    print("🚀 Démarrage des tests de permissions des articles")
    print("=" * 60)
    
    try:
        test_home_page_permissions()
        test_direct_access_permissions()
        test_anonymous_user()
        
        print("\n" + "=" * 60)
        print("✅ Tests terminés ! Vérifiez les résultats ci-dessus.")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
