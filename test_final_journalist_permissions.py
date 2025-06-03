#!/usr/bin/env python3
"""
Test final et complet des permissions des journalistes.
Ce script vérifie que :
1. Les journalistes peuvent modifier/supprimer leurs propres articles
2. Les journalistes ne peuvent pas modifier/supprimer les articles d'autres auteurs
3. Les lecteurs ne peuvent rien modifier/supprimer
4. Les admins peuvent tout modifier/supprimer
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

def create_comprehensive_test_data():
    """Créer un jeu complet de données de test"""
    print("🔧 Création des données de test complètes...")
    
    # Créer une catégorie
    category, _ = Category.objects.get_or_create(
        nom="Test Category",
        defaults={'description': 'Catégorie de test'}
    )
    
    # Créer différents types d'utilisateurs
    users = {}
    
    # Journaliste 1
    user1, created = User.objects.get_or_create(
        username='journalist1',
        defaults={'email': 'journalist1@test.com'}
    )
    if created:
        user1.set_password('testpass123')
        user1.save()
    profile1, _ = UserProfile.objects.get_or_create(user=user1)
    profile1.role = 'journaliste'
    profile1.save()
    users['journalist1'] = user1
    
    # Journaliste 2
    user2, created = User.objects.get_or_create(
        username='journalist2',
        defaults={'email': 'journalist2@test.com'}
    )
    if created:
        user2.set_password('testpass123')
        user2.save()
    profile2, _ = UserProfile.objects.get_or_create(user=user2)
    profile2.role = 'journaliste'
    profile2.save()
    users['journalist2'] = user2
    
    # Lecteur
    reader, created = User.objects.get_or_create(
        username='reader',
        defaults={'email': 'reader@test.com'}
    )
    if created:
        reader.set_password('testpass123')
        reader.save()
    profile_reader, _ = UserProfile.objects.get_or_create(user=reader)
    profile_reader.role = 'lecteur'
    profile_reader.save()
    users['reader'] = reader
    
    # Admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@test.com'}
    )
    if created:
        admin.set_password('testpass123')
        admin.save()
    profile_admin, _ = UserProfile.objects.get_or_create(user=admin)
    profile_admin.role = 'admin'
    profile_admin.save()
    users['admin'] = admin
    
    # Créer des articles pour chaque journaliste
    articles = {}
    
    # Article du journaliste 1
    article1, _ = Article.objects.get_or_create(
        titre="Article du Journaliste 1",
        defaults={
            'contenu': "Contenu de l'article par le journaliste 1.",
            'auteur': 'journalist1',  # Exactement le nom d'utilisateur
            'category': category
        }
    )
    articles['journalist1'] = article1
    
    # Article du journaliste 2
    article2, _ = Article.objects.get_or_create(
        titre="Article du Journaliste 2",
        defaults={
            'contenu': "Contenu de l'article par le journaliste 2.",
            'auteur': 'journalist2',  # Exactement le nom d'utilisateur
            'category': category
        }
    )
    articles['journalist2'] = article2
    
    print(f"   ✅ Utilisateurs créés: {list(users.keys())}")
    print(f"   ✅ Articles créés: {len(articles)}")
    
    return users, articles

def test_journalist_permissions():
    """Test complet des permissions des journalistes"""
    print("\n🧪 Test des permissions des journalistes")
    print("=" * 50)
    
    users, articles = create_comprehensive_test_data()
    client = Client()
    
    # Test 1: Journaliste peut modifier son propre article
    print("\n1️⃣ Test: Journaliste modifie son propre article")
    client.login(username='journalist1', password='testpass123')
    
    article = articles['journalist1']
    response = client.get(reverse('modifier_article', args=[article.id]))
    
    if response.status_code == 200:
        print("   ✅ SUCCÈS: Journaliste 1 peut accéder à la modification de son article")
    else:
        print(f"   ❌ ÉCHEC: Code de réponse {response.status_code}")
    
    client.logout()
    
    # Test 2: Journaliste ne peut pas modifier l'article d'un autre
    print("\n2️⃣ Test: Journaliste ne peut pas modifier l'article d'un autre")
    client.login(username='journalist1', password='testpass123')
    
    other_article = articles['journalist2']
    response = client.get(reverse('modifier_article', args=[other_article.id]))
    
    if response.status_code == 403:
        print("   ✅ SUCCÈS: Accès interdit pour modifier l'article d'un autre")
    else:
        print(f"   ❌ ÉCHEC: Code de réponse {response.status_code} (attendu: 403)")
    
    client.logout()
    
    # Test 3: Lecteur ne peut rien modifier
    print("\n3️⃣ Test: Lecteur ne peut rien modifier")
    client.login(username='reader', password='testpass123')
    
    response = client.get(reverse('modifier_article', args=[article.id]))
    
    if response.status_code == 403:
        print("   ✅ SUCCÈS: Accès interdit pour le lecteur")
    else:
        print(f"   ❌ ÉCHEC: Code de réponse {response.status_code} (attendu: 403)")
    
    client.logout()
    
    # Test 4: Admin peut tout modifier
    print("\n4️⃣ Test: Admin peut tout modifier")
    client.login(username='admin', password='testpass123')
    
    response = client.get(reverse('modifier_article', args=[article.id]))
    
    if response.status_code == 200:
        print("   ✅ SUCCÈS: Admin peut modifier n'importe quel article")
    else:
        print(f"   ❌ ÉCHEC: Code de réponse {response.status_code}")
    
    client.logout()

def test_template_permissions():
    """Test des permissions au niveau des templates"""
    print("\n🎨 Test des permissions dans les templates")
    print("=" * 50)
    
    users, articles = create_comprehensive_test_data()
    client = Client()
    
    # Test de la page d'accueil pour chaque utilisateur
    for username, user in users.items():
        print(f"\n👤 Test pour {user.profile.role}: {username}")
        
        client.login(username=username, password='testpass123')
        response = client.get('/')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Compter les boutons modifier/supprimer
            edit_buttons = content.count('btn-outline-warning')
            delete_buttons = content.count('btn-outline-danger')
            
            print(f"   Boutons modifier visibles: {edit_buttons}")
            print(f"   Boutons supprimer visibles: {delete_buttons}")
            
            # Vérifications selon le rôle
            if user.profile.role == 'lecteur':
                if edit_buttons == 0 and delete_buttons == 0:
                    print("   ✅ CORRECT: Aucun bouton pour le lecteur")
                else:
                    print("   ❌ ERREUR: Le lecteur ne devrait voir aucun bouton")
            
            elif user.profile.role == 'journaliste':
                # Le journaliste devrait voir exactement 1 bouton (pour son article)
                if edit_buttons == 1 and delete_buttons == 1:
                    print("   ✅ CORRECT: 1 bouton visible pour l'article du journaliste")
                else:
                    print(f"   ❌ ERREUR: Attendu 1 bouton, trouvé {edit_buttons} modifier et {delete_buttons} supprimer")
            
            elif user.profile.role == 'admin':
                # L'admin devrait voir tous les boutons
                total_articles = len(articles)
                if edit_buttons == total_articles and delete_buttons == total_articles:
                    print(f"   ✅ CORRECT: {total_articles} boutons visibles pour tous les articles (admin)")
                else:
                    print(f"   ❌ ERREUR: Attendu {total_articles} boutons, trouvé {edit_buttons} modifier et {delete_buttons} supprimer")
        
        client.logout()

def test_direct_template_tags():
    """Test direct des template tags"""
    print("\n🏷️ Test direct des template tags")
    print("=" * 50)
    
    from blog.templatetags.role_tags import can_edit_article, can_delete_article
    
    users, articles = create_comprehensive_test_data()
    
    journalist1 = users['journalist1']
    journalist2 = users['journalist2']
    reader = users['reader']
    admin = users['admin']
    
    article1 = articles['journalist1']
    article2 = articles['journalist2']
    
    print(f"\n📄 Test avec l'article de journalist1: '{article1.titre}' (auteur: {article1.auteur})")
    
    # Test pour journalist1 (propriétaire)
    can_edit = can_edit_article(journalist1, article1)
    can_delete = can_delete_article(journalist1, article1)
    print(f"   journalist1 peut modifier: {can_edit} ({'✅' if can_edit else '❌'})")
    print(f"   journalist1 peut supprimer: {can_delete} ({'✅' if can_delete else '❌'})")
    
    # Test pour journalist2 (non-propriétaire)
    can_edit = can_edit_article(journalist2, article1)
    can_delete = can_delete_article(journalist2, article1)
    print(f"   journalist2 peut modifier: {can_edit} ({'✅' if not can_edit else '❌'})")
    print(f"   journalist2 peut supprimer: {can_delete} ({'✅' if not can_delete else '❌'})")
    
    # Test pour reader
    can_edit = can_edit_article(reader, article1)
    can_delete = can_delete_article(reader, article1)
    print(f"   reader peut modifier: {can_edit} ({'✅' if not can_edit else '❌'})")
    print(f"   reader peut supprimer: {can_delete} ({'✅' if not can_delete else '❌'})")
    
    # Test pour admin
    can_edit = can_edit_article(admin, article1)
    can_delete = can_delete_article(admin, article1)
    print(f"   admin peut modifier: {can_edit} ({'✅' if can_edit else '❌'})")
    print(f"   admin peut supprimer: {can_delete} ({'✅' if can_delete else '❌'})")

def main():
    """Fonction principale"""
    print("🚀 TEST FINAL DES PERMISSIONS DES JOURNALISTES")
    print("=" * 60)
    
    try:
        test_journalist_permissions()
        test_template_permissions()
        test_direct_template_tags()
        
        print("\n" + "=" * 60)
        print("✅ TESTS TERMINÉS!")
        print("\n📋 RÉSUMÉ DES ATTENTES:")
        print("   • Journalistes: peuvent modifier/supprimer LEURS articles uniquement")
        print("   • Lecteurs: ne peuvent rien modifier/supprimer")
        print("   • Admins: peuvent tout modifier/supprimer")
        print("   • Templates: boutons visibles selon les permissions")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
