#!/usr/bin/env python3
"""
Test avec les utilisateurs existants dans la base de données.
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
from blog.models import Article, UserProfile
from django.urls import reverse

def test_existing_users():
    """Tester avec les utilisateurs existants"""
    print("🧪 Test avec les utilisateurs existants")
    print("=" * 50)
    
    # Lister les journalistes et leurs articles
    journalistes = User.objects.filter(profile__role='journaliste')
    articles = Article.objects.all()
    
    print(f"📋 Journalistes trouvés: {journalistes.count()}")
    for journalist in journalistes:
        print(f"   - {journalist.username}")
        
        # Chercher les articles de ce journaliste
        user_articles = articles.filter(auteur__icontains=journalist.username)
        if user_articles.exists():
            print(f"     Articles trouvés:")
            for article in user_articles:
                print(f"       - '{article.titre}' par '{article.auteur}'")
        else:
            print(f"     Aucun article trouvé pour {journalist.username}")
    
    print(f"\n📰 Tous les articles:")
    for article in articles:
        print(f"   - '{article.titre}' par '{article.auteur}' (ID: {article.id})")
    
    # Créer un article pour un journaliste existant
    if journalistes.exists():
        test_journalist = journalistes.first()
        print(f"\n🔧 Création d'un article pour {test_journalist.username}...")
        
        test_article, created = Article.objects.get_or_create(
            titre=f"Nouvel article de {test_journalist.username}",
            defaults={
                'contenu': f"Ceci est un nouvel article écrit par {test_journalist.username}.",
                'auteur': test_journalist.username
            }
        )
        
        if created:
            print(f"   ✅ Article créé: '{test_article.titre}'")
        else:
            print(f"   📄 Article existant: '{test_article.titre}'")
        
        # Tester les permissions
        print(f"\n🧪 Test des permissions pour {test_journalist.username}:")
        client = Client()
        
        # Connexion
        client.login(username=test_journalist.username, password='testpass123')
        
        # Test page de détail
        url = reverse('article_detail', args=[test_article.id])
        response = client.get(url)
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            has_edit = 'Modifier cet article' in content
            has_delete = 'Supprimer' in content and 'btn btn-danger' in content
            
            print(f"   Page de détail - Bouton modifier: {has_edit}")
            print(f"   Page de détail - Bouton supprimer: {has_delete}")
        else:
            print(f"   ❌ Erreur page de détail: code {response.status_code}")
        
        # Test page d'accueil avec redirection
        response = client.get('/', follow=True)
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            edit_count = content.count('btn-outline-warning')
            delete_count = content.count('btn-outline-danger')
            
            print(f"   Page d'accueil - Boutons modifier: {edit_count}")
            print(f"   Page d'accueil - Boutons supprimer: {delete_count}")
            
            # Vérifier que l'article apparaît
            if test_article.titre in content:
                print(f"   ✅ Article trouvé sur la page d'accueil")
            else:
                print(f"   ❌ Article non trouvé sur la page d'accueil")
        else:
            print(f"   ❌ Erreur page d'accueil: code {response.status_code}")
        
        client.logout()

def create_and_test_simple_case():
    """Créer un cas de test simple et le tester"""
    print("\n🔧 Création d'un cas de test simple...")
    
    # Nettoyer les anciens tests
    User.objects.filter(username='simple_journalist').delete()
    
    # Créer un journaliste simple
    user = User.objects.create_user(
        username='simple_journalist',
        email='simple@test.com',
        password='testpass123'
    )
    
    # Créer le profil journaliste
    profile = UserProfile.objects.create(user=user, role='journaliste')
    
    # Créer un article
    article = Article.objects.create(
        titre='Article simple test',
        contenu='Contenu simple pour test.',
        auteur=user.username
    )
    
    print(f"   ✅ Journaliste créé: {user.username} (rôle: {profile.role})")
    print(f"   ✅ Article créé: '{article.titre}' par '{article.auteur}'")
    
    # Test avec le client de test
    client = Client()
    client.login(username=user.username, password='testpass123')
    
    # Test direct des template tags
    from blog.templatetags.role_tags import can_edit_article, can_delete_article
    
    # Recharger l'utilisateur avec les relations
    user_with_profile = User.objects.select_related('profile').get(id=user.id)
    
    can_edit = can_edit_article(user_with_profile, article)
    can_delete = can_delete_article(user_with_profile, article)
    
    print(f"   Template tag can_edit_article: {can_edit}")
    print(f"   Template tag can_delete_article: {can_delete}")
    
    # Test de la page de détail
    url = reverse('article_detail', args=[article.id])
    response = client.get(url)
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        has_edit = 'Modifier cet article' in content
        has_delete = 'Supprimer' in content and 'btn btn-danger' in content
        
        print(f"   Page de détail - Bouton modifier: {has_edit}")
        print(f"   Page de détail - Bouton supprimer: {has_delete}")
        
        if has_edit and has_delete:
            print("   ✅ SUCCÈS: Tous les boutons sont visibles!")
        else:
            print("   ❌ PROBLÈME: Certains boutons manquent")
    else:
        print(f"   ❌ Erreur: code {response.status_code}")

def main():
    """Fonction principale"""
    try:
        test_existing_users()
        create_and_test_simple_case()
        
        print("\n" + "=" * 50)
        print("✅ Tests terminés!")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
