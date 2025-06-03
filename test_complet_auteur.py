#!/usr/bin/env python
"""
Test complet du pré-remplissage automatique du champ auteur
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile, Article, Category
from blog.forms import ArticleForm
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from blog.views import ajouter_article

def test_view_with_authenticated_user():
    """Test de la vue avec un utilisateur authentifié"""
    print("🧪 Test : Vue avec utilisateur authentifié")
    print("=" * 50)
    
    # Créer une factory de requêtes
    factory = RequestFactory()
    
    # Créer un utilisateur de test
    username = 'test_view_user'
    User.objects.filter(username=username).delete()
    
    user = User.objects.create_user(
        username=username,
        email='test@view.com',
        password='testpass123'
    )
    
    # Créer le profil
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.role = 'journaliste'
    profile.save()
    
    # Créer une requête GET simulée
    request = factory.get('/ajouter_article/')
    request.user = user
    
    # Simuler les messages (nécessaire pour la vue)
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.contrib.sessions.backends.db import SessionStore
    
    request.session = SessionStore()
    request._messages = FallbackStorage(request)
    
    # Appeler la vue
    response = ajouter_article(request)
    
    print(f"✅ Utilisateur: {user.username}")
    print(f"✅ Code de réponse: {response.status_code}")
    
    # Vérifier que la réponse contient le bon contenu
    content = response.content.decode('utf-8')
    if user.username in content:
        print(f"✅ Le username '{user.username}' est présent dans le formulaire")
    else:
        print(f"❌ Le username '{user.username}' n'est pas présent dans le formulaire")
        return False
    
    # Nettoyer
    user.delete()
    return True

def test_view_with_anonymous_user():
    """Test de la vue avec un utilisateur anonyme"""
    print("\n🧪 Test : Vue avec utilisateur anonyme")
    print("=" * 50)
    
    # Créer une factory de requêtes
    factory = RequestFactory()
    
    # Créer une requête GET simulée
    request = factory.get('/ajouter_article/')
    request.user = AnonymousUser()
    
    # Simuler les messages et sessions
    from django.contrib.messages.storage.fallback import FallbackStorage
    from django.contrib.sessions.backends.db import SessionStore
    
    request.session = SessionStore()
    request._messages = FallbackStorage(request)
    
    # Appeler la vue
    response = ajouter_article(request)
    
    print(f"✅ Utilisateur: Anonyme")
    print(f"✅ Code de réponse: {response.status_code}")
    
    # Vérifier que le formulaire ne contient pas de valeur pré-remplie
    content = response.content.decode('utf-8')
    if 'readonly' not in content:
        print("✅ Le champ auteur n'est pas en lecture seule pour utilisateur anonyme")
    else:
        print("❌ Le champ auteur est en lecture seule pour utilisateur anonyme")
        return False
    
    return True

def test_form_initialization():
    """Test direct de l'initialisation du formulaire"""
    print("\n🧪 Test : Initialisation directe du formulaire")
    print("=" * 50)
    
    # Test avec données initiales
    test_username = 'form_test_user'
    form_with_initial = ArticleForm(initial={'auteur': test_username})
    
    # Vérifier les propriétés du formulaire
    auteur_field = form_with_initial.fields['auteur']
    is_readonly = auteur_field.widget.attrs.get('readonly', False)
    help_text = auteur_field.help_text
    
    print(f"✅ Valeur initiale: {form_with_initial.initial.get('auteur')}")
    print(f"✅ Champ readonly: {is_readonly}")
    print(f"✅ Message d'aide: {help_text}")
    
    # Test sans données initiales
    form_without_initial = ArticleForm()
    auteur_field_empty = form_without_initial.fields['auteur']
    is_readonly_empty = auteur_field_empty.widget.attrs.get('readonly', False)
    
    print(f"✅ Sans initial - readonly: {is_readonly_empty}")
    
    if is_readonly and not is_readonly_empty:
        print("✅ Le comportement readonly est correct selon l'initialisation")
        return True
    else:
        print("❌ Le comportement readonly n'est pas correct")
        return False

def test_article_creation():
    """Test de création d'article avec auteur pré-rempli"""
    print("\n🧪 Test : Création d'article avec auteur automatique")
    print("=" * 50)
    
    # Créer utilisateur et catégorie
    username = 'creation_test_user'
    User.objects.filter(username=username).delete()
    
    user = User.objects.create_user(
        username=username,
        email='creation@test.com',
        password='testpass123'
    )
    
    category = Category.objects.create(
        nom='Test Category Creation',
        description='Test'
    )
    
    # Données d'article
    article_data = {
        'titre': 'Test Article Auteur Auto',
        'contenu': 'Contenu de test',
        'auteur': user.username,
        'category': category.id,
    }
    
    # Créer le formulaire et sauvegarder
    form = ArticleForm(data=article_data)
    
    if form.is_valid():
        article = form.save()
        print(f"✅ Article créé: {article.titre}")
        print(f"✅ Auteur: {article.auteur}")
        
        if article.auteur == user.username:
            print("✅ L'auteur correspond à l'utilisateur")
            
            # Nettoyer
            article.delete()
            category.delete()
            user.delete()
            return True
        else:
            print(f"❌ L'auteur ne correspond pas (attendu: {user.username}, obtenu: {article.auteur})")
    else:
        print(f"❌ Formulaire invalide: {form.errors}")
    
    # Nettoyer en cas d'erreur
    category.delete()
    user.delete()
    return False

def main():
    print("🚀 TESTS COMPLETS - PRÉ-REMPLISSAGE AUTOMATIQUE DU CHAMP AUTEUR")
    print("=" * 80)
    
    tests_results = []
    
    try:
        # Tests individuels
        tests_results.append(test_form_initialization())
        tests_results.append(test_view_with_authenticated_user())
        tests_results.append(test_view_with_anonymous_user())
        tests_results.append(test_article_creation())
        
        # Résultats
        print("\n" + "=" * 80)
        print("📊 RÉSULTATS DES TESTS")
        print("=" * 80)
        
        passed = sum(tests_results)
        total = len(tests_results)
        
        print(f"✅ Tests réussis: {passed}/{total}")
        
        if all(tests_results):
            print("🎉 TOUS LES TESTS ONT RÉUSSI!")
            print("✅ Le pré-remplissage automatique du champ auteur fonctionne parfaitement")
            return True
        else:
            print("⚠️  Certains tests ont échoué")
            return False
            
    except Exception as e:
        print(f"💥 ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
