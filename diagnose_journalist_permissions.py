#!/usr/bin/env python3
"""
Script pour diagnostiquer le problème des permissions d'articles pour les journalistes.
"""

import os
import django
import sys

# Configuration Django
sys.path.append('c:\\Users\\jbert\\Documents\\python isitech\\monprojet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, UserProfile

def diagnose_article_permissions():
    """Diagnostiquer les permissions d'articles"""
    print("🔍 Diagnostic des permissions d'articles pour les journalistes")
    print("=" * 60)
    
    # Lister tous les utilisateurs avec profils
    print("\n📋 Utilisateurs existants:")
    users = User.objects.all()
    for user in users:
        try:
            profile = user.profile
            print(f"   - {user.username} (rôle: {profile.role})")
        except UserProfile.DoesNotExist:
            print(f"   - {user.username} (pas de profil)")
    
    # Lister tous les articles
    print("\n📰 Articles existants:")
    articles = Article.objects.all()
    for article in articles:
        print(f"   - '{article.titre}' par '{article.auteur}' (ID: {article.id})")
    
    # Tester les correspondances auteur/utilisateur
    print("\n🔗 Test des correspondances auteur/utilisateur:")
    for user in users:
        try:
            profile = user.profile
            if profile.role == 'journaliste':
                print(f"\n   👤 Journaliste: {user.username}")
                matching_articles = []
                for article in articles:
                    if article.auteur.lower() == user.username.lower():
                        matching_articles.append(article)
                        print(f"      ✅ Correspond à l'article: '{article.titre}'")
                
                if not matching_articles:
                    print("      ❌ Aucun article correspondant trouvé")
                    print(f"         Nom d'utilisateur: '{user.username}'")
                    print("         Auteurs d'articles disponibles:")
                    for article in articles:
                        print(f"           - '{article.auteur}'")
        except UserProfile.DoesNotExist:
            pass
    
    # Créer un test pratique
    print("\n🧪 Test pratique:")
    test_journaliste = None
    for user in users:
        try:
            if user.profile.role == 'journaliste':
                test_journaliste = user
                break
        except UserProfile.DoesNotExist:
            pass
    
    if test_journaliste:
        print(f"   Utilisation du journaliste: {test_journaliste.username}")
        
        # Créer un article test avec ce journaliste comme auteur
        test_article, created = Article.objects.get_or_create(
            titre="Article test pour permissions",
            defaults={
                'contenu': "Ceci est un article de test pour vérifier les permissions.",
                'auteur': test_journaliste.username
            }
        )
        
        if created:
            print(f"   ✅ Article test créé: '{test_article.titre}' par '{test_article.auteur}'")
        else:
            print(f"   📄 Article test existant: '{test_article.titre}' par '{test_article.auteur}'")
        
        # Tester la correspondance
        match = test_article.auteur.lower() == test_journaliste.username.lower()
        print(f"   Test de correspondance: '{test_article.auteur}' == '{test_journaliste.username}' -> {match}")
        
        return test_journaliste, test_article
    else:
        print("   ❌ Aucun journaliste trouvé pour le test")
        return None, None

def create_test_journalist():
    """Créer un journaliste de test"""
    print("\n🔧 Création d'un journaliste de test...")
    
    # Créer un utilisateur journaliste
    user, created = User.objects.get_or_create(
        username='test_journalist',
        defaults={
            'email': 'test_journalist@example.com',
            'first_name': 'Test',
            'last_name': 'Journalist',
            'password': 'testpass123'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"   ✅ Utilisateur créé: {user.username}")
    else:
        print(f"   📄 Utilisateur existant: {user.username}")
    
    # Créer ou mettre à jour le profil
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = 'journaliste'
    profile.save()
    
    if created:
        print(f"   ✅ Profil journaliste créé pour {user.username}")
    else:
        print(f"   📄 Profil journaliste mis à jour pour {user.username}")
    
    # Créer un article pour ce journaliste
    article, created = Article.objects.get_or_create(
        titre="Mon premier article",
        defaults={
            'contenu': "Ceci est mon premier article en tant que journaliste.",
            'auteur': user.username  # Important: utiliser exactement le username
        }
    )
    
    if created:
        print(f"   ✅ Article créé: '{article.titre}' par '{article.auteur}'")
    else:
        print(f"   📄 Article existant: '{article.titre}' par '{article.auteur}'")
    
    return user, article

def test_template_logic():
    """Tester la logique des template tags"""
    print("\n🧪 Test de la logique des template tags...")
    
    # Importer les fonctions des template tags
    from blog.templatetags.role_tags import can_edit_article, can_delete_article
    
    user, article = create_test_journalist()
    
    # Tester can_edit_article
    can_edit = can_edit_article(user, article)
    print(f"   can_edit_article({user.username}, '{article.titre}'): {can_edit}")
    
    # Tester can_delete_article
    can_delete = can_delete_article(user, article)
    print(f"   can_delete_article({user.username}, '{article.titre}'): {can_delete}")
    
    # Debug des valeurs
    print(f"   Debug:")
    print(f"     - user.is_authenticated: {user.is_authenticated}")
    print(f"     - hasattr(user, 'profile'): {hasattr(user, 'profile')}")
    if hasattr(user, 'profile'):
        print(f"     - user.profile.role: {user.profile.role}")
    print(f"     - article.auteur: '{article.auteur}'")
    print(f"     - user.username: '{user.username}'")
    print(f"     - Comparison: '{article.auteur.lower()}' == '{user.username.lower()}' -> {article.auteur.lower() == user.username.lower()}")

def main():
    """Fonction principale"""
    try:
        # Diagnostic général
        diagnose_article_permissions()
        
        # Test spécifique
        test_template_logic()
        
        print("\n" + "=" * 60)
        print("✅ Diagnostic terminé!")
        print("\n💡 Solutions possibles:")
        print("   1. Vérifier que l'auteur de l'article correspond exactement au username")
        print("   2. Améliorer la logique de correspondance auteur/utilisateur")
        print("   3. Ajouter des logs pour débugger les template tags")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du diagnostic: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
