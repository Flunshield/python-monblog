#!/usr/bin/env python
"""
Script de test pour vérifier que le champ auteur est automatiquement pré-rempli
avec l'username de l'utilisateur connecté lors de la création d'un article.
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Article, Category, UserProfile

def test_auteur_automatique():
    """Test que le champ auteur est pré-rempli automatiquement"""
    print("🧪 Test : Pré-remplissage automatique du champ auteur")
    print("=" * 60)
    
    # Créer un client de test    client = Client()
    
    # Nettoyer et créer un utilisateur journaliste
    test_username = 'journaliste_test_auto'
    User.objects.filter(username=test_username).delete()
    
    user = User.objects.create_user(
        username=test_username,
        email='journaliste_auto@test.com',
        password='testpass123'
    )
    
    # Vérifier si le profil existe déjà ou le créer
    try:
        profile = user.profile
        profile.role = 'journaliste'
        profile.save()
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, role='journaliste')
    
    # Se connecter
    login_success = client.login(username=test_username, password='testpass123')
    if not login_success:
        print("❌ Échec de la connexion")
        return False
    
    print(f"✅ Utilisateur '{user.username}' connecté avec succès")
    
    # Accéder à la page d'ajout d'article
    response = client.get(reverse('ajouter_article'))
    
    if response.status_code != 200:
        print(f"❌ Échec d'accès à la page d'ajout d'article (code: {response.status_code})")
        return False
    
    print("✅ Page d'ajout d'article accessible")
    
    # Vérifier que le formulaire contient la valeur pré-remplie
    form = response.context['form']
    auteur_initial = form.initial.get('auteur')
    
    if auteur_initial != user.username:
        print(f"❌ Le champ auteur n'est pas pré-rempli correctement")
        print(f"   Attendu: {user.username}")
        print(f"   Obtenu: {auteur_initial}")
        return False
    
    print(f"✅ Champ auteur pré-rempli correctement avec: '{auteur_initial}'")
    
    # Vérifier que le champ est en lecture seule
    auteur_field = form.fields['auteur']
    is_readonly = auteur_field.widget.attrs.get('readonly', False)
    
    if not is_readonly:
        print("❌ Le champ auteur n'est pas en lecture seule")
        return False
    
    print("✅ Champ auteur configuré en lecture seule")
    
    # Vérifier le message d'aide
    help_text = auteur_field.help_text
    if "automatiquement rempli" not in help_text:
        print("❌ Message d'aide manquant ou incorrect")
        print(f"   Message d'aide: {help_text}")
        return False
    
    print("✅ Message d'aide présent et correct")
    
    # Test de création d'article avec le champ pré-rempli
    category = Category.objects.create(nom='Test Category', description='Test')
    
    article_data = {
        'titre': 'Article de test avec auteur automatique',
        'contenu': 'Contenu de test pour vérifier le pré-remplissage de l\'auteur.',
        'auteur': user.username,  # Sera pré-rempli automatiquement
        'category': category.id,
    }
    
    response = client.post(reverse('ajouter_article'), article_data)
    
    if response.status_code == 302:  # Redirection après succès
        print("✅ Article créé avec succès")
        
        # Vérifier que l'article a été créé avec le bon auteur
        article = Article.objects.filter(titre='Article de test avec auteur automatique').first()
        if article and article.auteur == user.username:
            print(f"✅ Article créé avec l'auteur correct: '{article.auteur}'")
            return True
        else:
            print("❌ Article créé mais avec un auteur incorrect")
            return False
    else:
        print(f"❌ Échec de création de l'article (code: {response.status_code})")
        if hasattr(response, 'context') and response.context.get('form'):
            print(f"   Erreurs du formulaire: {response.context['form'].errors}")
        return False

def test_utilisateur_non_connecte():
    """Test que le champ n'est pas pré-rempli pour un utilisateur non connecté"""
    print("\n🧪 Test : Utilisateur non connecté")
    print("=" * 60)
    
    client = Client()
    
    # Accéder à la page sans être connecté
    response = client.get(reverse('ajouter_article'))
    
    if response.status_code != 200:
        print(f"❌ Page non accessible pour utilisateur non connecté (code: {response.status_code})")
        return False
    
    # Vérifier que le champ auteur n'est pas pré-rempli
    form = response.context['form']
    auteur_initial = form.initial.get('auteur')
    
    if auteur_initial:
        print(f"❌ Le champ auteur ne devrait pas être pré-rempli pour un utilisateur non connecté")
        print(f"   Valeur trouvée: {auteur_initial}")
        return False
    
    print("✅ Champ auteur non pré-rempli pour utilisateur non connecté")
    
    # Vérifier que le champ n'est pas en lecture seule
    auteur_field = form.fields['auteur']
    is_readonly = auteur_field.widget.attrs.get('readonly', False)
    
    if is_readonly:
        print("❌ Le champ auteur ne devrait pas être en lecture seule pour un utilisateur non connecté")
        return False
    
    print("✅ Champ auteur modifiable pour utilisateur non connecté")
    return True

def cleanup():
    """Nettoyer les données de test"""
    print("\n🧹 Nettoyage des données de test...")
    
    # Supprimer les articles de test
    Article.objects.filter(titre__contains='test').delete()
    
    # Supprimer les catégories de test
    Category.objects.filter(nom__contains='Test').delete()
    
    # Supprimer les utilisateurs de test
    User.objects.filter(username__contains='test').delete()
    
    print("✅ Nettoyage terminé")

def main():
    print("🚀 TESTS - PRÉ-REMPLISSAGE AUTOMATIQUE DU CHAMP AUTEUR")
    print("=" * 80)
    
    try:
        # Test principal
        test1_success = test_auteur_automatique()
        
        # Test utilisateur non connecté
        test2_success = test_utilisateur_non_connecte()
        
        # Nettoyage
        cleanup()
        
        # Résultat final
        print("\n" + "=" * 80)
        print("📊 RÉSULTATS DES TESTS")
        print("=" * 80)
        
        if test1_success and test2_success:
            print("✅ TOUS LES TESTS RÉUSSIS")
            print("✅ Le pré-remplissage automatique du champ auteur fonctionne correctement")
            return True
        else:
            print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print("❌ Le pré-remplissage automatique nécessite des corrections")
            return False
            
    except Exception as e:
        print(f"💥 ERREUR LORS DES TESTS: {e}")
        cleanup()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
