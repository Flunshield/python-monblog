#!/usr/bin/env python3
"""
Test d'intégration pour vérifier les permissions des journalistes sur leurs articles.
"""

import os
import django
import sys

# Configuration Django
sys.path.append('c:\\Users\\jbert\\Documents\\python isitech\\monprojet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from blog.models import Article, UserProfile, Category
from django.urls import reverse

def setup_test_data():
    """Configurer les données de test"""
    print("🔧 Configuration des données de test...")
    
    # Créer une catégorie
    category, _ = Category.objects.get_or_create(
        nom="Test Category",
        defaults={'description': 'Catégorie de test'}
    )
    
    # Créer un journaliste
    user, created = User.objects.get_or_create(
        username='real_journalist',
        defaults={
            'email': 'real_journalist@test.com',
            'password': 'testpass123'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # S'assurer que le profil est bien journaliste
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'journaliste'
    profile.save()
    
    # Créer un article pour ce journaliste
    article, created = Article.objects.get_or_create(
        titre="Article du vrai journaliste",
        defaults={
            'contenu': "Contenu de l'article du journaliste.",
            'auteur': user.username,
            'category': category
        }
    )
    
    print(f"   ✅ Journaliste: {user.username} (rôle: {profile.role})")
    print(f"   ✅ Article: '{article.titre}' par '{article.auteur}'")
    
    return user, article

def test_home_page_buttons():
    """Tester l'affichage des boutons sur la page d'accueil"""
    print("\n🧪 Test des boutons sur la page d'accueil...")
    
    user, article = setup_test_data()
    client = Client()
    
    # Test sans connexion
    print("   📄 Test utilisateur anonyme:")
    response = client.get('/')
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        has_edit = 'btn-outline-warning' in content
        has_delete = 'btn-outline-danger' in content
        print(f"      Boutons modifier: {has_edit}, supprimer: {has_delete}")
        if not has_edit and not has_delete:
            print("      ✅ CORRECT: Aucun bouton pour utilisateur anonyme")
        else:
            print("      ❌ ERREUR: Des boutons sont visibles pour utilisateur anonyme")
    
    # Test avec le journaliste connecté
    print("   📄 Test journaliste connecté:")
    login_success = client.login(username=user.username, password='testpass123')
    print(f"      Connexion réussie: {login_success}")
    
    if login_success:
        response = client.get('/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Compter les boutons modifier/supprimer
            edit_count = content.count('btn-outline-warning')
            delete_count = content.count('btn-outline-danger')
            
            print(f"      Boutons modifier trouvés: {edit_count}")
            print(f"      Boutons supprimer trouvés: {delete_count}")
            
            # Vérifier qu'il y a au moins un bouton (pour l'article du journaliste)
            if edit_count > 0 and delete_count > 0:
                print("      ✅ CORRECT: Boutons visibles pour le journaliste")
            else:
                print("      ❌ ERREUR: Aucun bouton visible pour le journaliste")
                print("      🔍 Debug - contenu autour des articles:")
                # Chercher les cartes d'articles
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'card-title' in line and article.titre in line:
                        print(f"         Ligne {i}: {line.strip()}")
                        # Afficher les 10 lignes suivantes
                        for j in range(1, 11):
                            if i + j < len(lines):
                                print(f"         Ligne {i+j}: {lines[i+j].strip()}")
                        break
        else:
            print(f"      ❌ ERREUR: Code de réponse {response.status_code}")
    
    client.logout()

def test_article_detail_buttons():
    """Tester l'affichage des boutons sur la page de détail d'article"""
    print("\n🧪 Test des boutons sur la page de détail d'article...")
    
    user, article = setup_test_data()
    client = Client()
    
    # Test avec le journaliste connecté
    login_success = client.login(username=user.username, password='testpass123')
    print(f"   Connexion réussie: {login_success}")
    
    if login_success:
        url = reverse('article_detail', args=[article.id])
        print(f"   URL testée: {url}")
        
        response = client.get(url)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            has_edit = 'Modifier cet article' in content
            has_delete = 'Supprimer' in content and 'btn btn-danger' in content
            
            print(f"   Bouton 'Modifier cet article': {has_edit}")
            print(f"   Bouton 'Supprimer': {has_delete}")
            
            if has_edit and has_delete:
                print("   ✅ CORRECT: Boutons visibles sur la page de détail")
            else:
                print("   ❌ ERREUR: Boutons manquants sur la page de détail")
                
                # Debug du contenu
                print("   🔍 Debug - recherche des boutons dans le contenu:")
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'btn' in line and ('warning' in line or 'danger' in line):
                        print(f"      Ligne {i}: {line.strip()}")
        else:
            print(f"   ❌ ERREUR: Code de réponse {response.status_code}")
    
    client.logout()

def test_template_tag_directly():
    """Tester directement les template tags"""
    print("\n🧪 Test direct des template tags...")
    
    user, article = setup_test_data()
    
    # Recharger l'utilisateur pour s'assurer qu'il a ses relations
    user = User.objects.select_related('profile').get(id=user.id)
    
    print(f"   Utilisateur: {user.username}")
    print(f"   Profil existe: {hasattr(user, 'profile')}")
    if hasattr(user, 'profile'):
        print(f"   Rôle: {user.profile.role}")
    print(f"   Article auteur: {article.auteur}")
    
    # Test manuel de la logique
    if hasattr(user, 'profile'):
        is_journalist = user.profile.role == 'journaliste'
        is_author = article.auteur.lower() == user.username.lower()
        can_edit = is_journalist and is_author
        
        print(f"   Est journaliste: {is_journalist}")
        print(f"   Est auteur: {is_author}")
        print(f"   Peut modifier: {can_edit}")
        
        if can_edit:
            print("   ✅ CORRECT: Le journaliste peut modifier son article")
        else:
            print("   ❌ ERREUR: Le journaliste ne peut pas modifier son article")

def main():
    """Fonction principale"""
    print("🚀 Test d'intégration des permissions journaliste")
    print("=" * 60)
    
    try:
        test_home_page_buttons()
        test_article_detail_buttons()
        test_template_tag_directly()
        
        print("\n" + "=" * 60)
        print("✅ Tests terminés!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
