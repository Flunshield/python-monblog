#!/usr/bin/env python3
"""
Script pour tester les permissions sur la page de détail d'article.
Ce script vérifie que seuls les journalistes et admins autorisés voient
les boutons de modification/suppression sur la page article_detail.
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
        {'username': 'lecteur_test', 'role': 'lecteur'},
        {'username': 'journaliste_test', 'role': 'journaliste'},
        {'username': 'admin_test', 'role': 'admin'},
        {'username': 'autre_journaliste', 'role': 'journaliste'},
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
        
        users[user_data['username']] = user
        print(f"   ✅ Utilisateur {user.username} créé avec le rôle {user_data['role']}")
    
    # Créer une catégorie de test
    category, created = Category.objects.get_or_create(
        nom="Test Category Detail",
        defaults={'description': 'Catégorie pour tester les détails'}
    )
    if created:
        print(f"   ✅ Catégorie '{category.nom}' créée")
    
    # Créer des articles de test avec différents auteurs
    articles_data = [
        {'titre': 'Article du journaliste_test', 'auteur': 'journaliste_test'},
        {'titre': 'Article de l\'admin_test', 'auteur': 'admin_test'},
        {'titre': 'Article de autre_journaliste', 'auteur': 'autre_journaliste'},
    ]
    
    articles = {}
    for article_data in articles_data:
        article, created = Article.objects.get_or_create(
            titre=article_data['titre'],
            defaults={
                'contenu': f"Contenu détaillé de l'article: {article_data['titre']}. Ce contenu est assez long pour bien tester l'affichage de la page de détail.",
                'auteur': article_data['auteur'],
                'category': category
            }
        )
        articles[article_data['auteur']] = article
        if created:
            print(f"   ✅ Article '{article.titre}' créé par {article.auteur}")
    
    return users, articles, category

def test_article_detail_permissions():
    """Tester les permissions sur les pages de détail d'article"""
    print("\n🧪 Test des permissions sur les pages de détail d'article...")
    
    users, articles, category = create_test_data()
    client = Client()
    
    # Tester chaque article avec chaque type d'utilisateur
    for article_owner, article in articles.items():
        print(f"\n   📄 Test de l'article de '{article_owner}': {article.titre}")
        
        for username, user in users.items():
            print(f"\n      👤 Test avec {user.profile.role} ({username}):")
            
            # Connexion de l'utilisateur
            client.login(username=username, password='testpass123')
            
            # Récupérer la page de détail de l'article
            response = client.get(reverse('article_detail', args=[article.id]))
            
            if response.status_code == 200:
                content = response.content.decode('utf-8')
                
                # Vérifier la présence des boutons
                has_modify_button = 'Modifier cet article' in content
                has_delete_button = 'Supprimer' in content and 'btn btn-danger' in content
                
                print(f"         - Bouton 'Modifier' visible: {'✅' if has_modify_button else '❌'}")
                print(f"         - Bouton 'Supprimer' visible: {'✅' if has_delete_button else '❌'}")
                
                # Vérifications selon le rôle et la propriété de l'article
                user_role = user.profile.role
                
                if user_role == 'lecteur':
                    # Un lecteur ne devrait voir aucun bouton
                    if not has_modify_button and not has_delete_button:
                        print("         ✅ CORRECT: Aucun bouton visible pour le lecteur")
                    else:
                        print("         ❌ ERREUR: Le lecteur ne devrait voir aucun bouton de gestion")
                
                elif user_role == 'journaliste':
                    # Un journaliste ne devrait voir les boutons que pour ses propres articles
                    should_see_buttons = (article.auteur == username)
                    
                    if should_see_buttons:
                        if has_modify_button and has_delete_button:
                            print("         ✅ CORRECT: Boutons visibles pour l'auteur de l'article")
                        else:
                            print("         ❌ ERREUR: Le journaliste devrait voir les boutons pour son article")
                    else:
                        if not has_modify_button and not has_delete_button:
                            print("         ✅ CORRECT: Aucun bouton visible pour l'article d'un autre")
                        else:
                            print("         ❌ ERREUR: Le journaliste ne devrait pas voir les boutons pour l'article d'un autre")
                
                elif user_role == 'admin':
                    # Un admin devrait voir tous les boutons pour tous les articles
                    if has_modify_button and has_delete_button:
                        print("         ✅ CORRECT: Tous les boutons visibles pour l'admin")
                    else:
                        print("         ❌ ERREUR: L'admin devrait voir tous les boutons")
                
            else:
                print(f"         ❌ ERREUR: Code de réponse {response.status_code}")
            
            client.logout()

def test_anonymous_access():
    """Tester l'accès anonyme aux pages de détail"""
    print("\n🧪 Test d'accès anonyme aux pages de détail...")
    
    users, articles, category = create_test_data()
    client = Client()
    
    # Tester avec un article
    test_article = list(articles.values())[0]
    
    response = client.get(reverse('article_detail', args=[test_article.id]))
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        has_modify_button = 'Modifier cet article' in content
        has_delete_button = 'Supprimer' in content and 'btn btn-danger' in content
        
        if not has_modify_button and not has_delete_button:
            print("   ✅ CORRECT: Aucun bouton de gestion visible pour un utilisateur anonyme")
        else:
            print("   ❌ ERREUR: Un utilisateur anonyme ne devrait voir aucun bouton de gestion")
    else:
        print(f"   ❌ ERREUR: Code de réponse {response.status_code} pour un accès anonyme")

def test_url_consistency():
    """Vérifier que les URLs des boutons sont correctes"""
    print("\n🧪 Test de cohérence des URLs...")
    
    users, articles, category = create_test_data()
    client = Client()
    
    # Tester avec un admin qui peut tout voir
    admin_user = users['admin_test']
    client.login(username=admin_user.username, password='testpass123')
    
    test_article = list(articles.values())[0]
    response = client.get(reverse('article_detail', args=[test_article.id]))
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Vérifier que les URLs sont présentes et correctes
        modify_url = reverse('modifier_article', args=[test_article.id])
        delete_url = reverse('supprimer_article', args=[test_article.id])
        
        if modify_url in content:
            print("   ✅ URL de modification correcte")
        else:
            print("   ❌ URL de modification manquante ou incorrecte")
        
        if delete_url in content:
            print("   ✅ URL de suppression correcte")
        else:
            print("   ❌ URL de suppression manquante ou incorrecte")
    
    client.logout()

def main():
    """Fonction principale"""
    print("🚀 Test des permissions sur les pages de détail d'article")
    print("=" * 70)
    
    try:
        test_article_detail_permissions()
        test_anonymous_access()
        test_url_consistency()
        
        print("\n" + "=" * 70)
        print("✅ Tests terminés ! Vérifiez les résultats ci-dessus.")
        print("💡 Les boutons de modification/suppression ne devraient être visibles que pour:")
        print("   - Les journalistes sur leurs propres articles")
        print("   - Les admins sur tous les articles")
        print("   - Jamais pour les lecteurs ou utilisateurs anonymes")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
