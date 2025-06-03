#!/usr/bin/env python
"""
Script de test pour vérifier les statistiques de la page journaliste
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Comment, UserProfile, Category
from django.utils import timezone
from datetime import datetime, timedelta

def test_journalist_stats():
    """Test des statistiques journaliste"""
    print("=== Test des statistiques journaliste ===\n")
    
    # Afficher tous les utilisateurs
    print("📍 Utilisateurs dans la base :")
    users = User.objects.all()
    for user in users:
        try:
            profile = user.profile
            print(f"  - {user.username} ({user.first_name} {user.last_name}) - Rôle: {profile.role}")
        except UserProfile.DoesNotExist:
            print(f"  - {user.username} ({user.first_name} {user.last_name}) - Pas de profil")
    print()
    
    # Afficher tous les articles
    print("📍 Articles dans la base :")
    articles = Article.objects.all()
    for article in articles:
        print(f"  - '{article.titre}' par {article.auteur} (créé le {article.date_creation.strftime('%Y-%m-%d')})")
    print(f"Total: {articles.count()} articles\n")
    
    # Afficher tous les commentaires
    print("📍 Commentaires dans la base :")
    comments = Comment.objects.all()
    for comment in comments:
        print(f"  - '{comment.contenu[:50]}...' par {comment.nom} sur '{comment.article.titre}'")
    print(f"Total: {comments.count()} commentaires\n")
    
    # Test de la logique de filtrage pour chaque journaliste
    print("📍 Test de filtrage des articles par journaliste :")
    journalists = User.objects.filter(profile__role='journaliste')
    
    for user in journalists:
        print(f"\n--- Test pour {user.username} ---")
        
        # Test de la logique de filtrage comme dans la vue
        user_articles = Article.objects.filter(
            auteur__icontains=user.username
        )
        if not user_articles.exists() and user.first_name:
            user_articles = Article.objects.filter(
                auteur__icontains=user.first_name
            )
        if not user_articles.exists() and user.last_name:
            user_articles = Article.objects.filter(
                auteur__icontains=user.last_name
            )
        if not user_articles.exists():
            user_articles = Article.objects.filter(auteur=user.username)
            
        print(f"Articles trouvés: {user_articles.count()}")
        for article in user_articles:
            print(f"  - '{article.titre}' (auteur: {article.auteur})")
        
        # Articles récents (ce mois-ci)
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        recent_articles = user_articles.filter(date_creation__gte=current_month)
        print(f"Articles ce mois-ci: {recent_articles.count()}")
        
        # Commentaires sur les articles de l'utilisateur
        user_comments = Comment.objects.filter(article__in=user_articles)
        print(f"Commentaires reçus: {user_comments.count()}")

def create_test_data():
    """Créer des données de test si nécessaire"""
    print("=== Création de données de test ===\n")
    
    # Créer un utilisateur journaliste si il n'existe pas
    journalist, created = User.objects.get_or_create(
        username='testjournalist',
        defaults={
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.dupont@test.com'
        }
    )
    
    if created:
        print(f"✅ Utilisateur journaliste créé: {journalist.username}")
        # Créer le profil
        UserProfile.objects.get_or_create(
            user=journalist,
            defaults={'role': 'journaliste'}
        )
        print(f"✅ Profil journaliste créé pour {journalist.username}")
    else:
        print(f"ℹ️  Utilisateur journaliste existe déjà: {journalist.username}")
    
    # Créer une catégorie de test
    category, created = Category.objects.get_or_create(
        nom='Test',
        defaults={'description': 'Catégorie de test'}
    )
    
    if created:
        print(f"✅ Catégorie créée: {category.nom}")
    else:
        print(f"ℹ️  Catégorie existe déjà: {category.nom}")
    
    # Créer des articles de test
    articles_to_create = [
        {
            'titre': 'Article Test Journaliste 1',
            'auteur': 'testjournalist',
            'contenu': 'Contenu de test pour le premier article'
        },
        {
            'titre': 'Article Test Journaliste 2', 
            'auteur': 'Jean',
            'contenu': 'Contenu de test pour le second article'
        },
        {
            'titre': 'Article Test Autre Auteur',
            'auteur': 'autreauteur',
            'contenu': 'Contenu d\'un autre auteur'
        }
    ]
    
    for article_data in articles_to_create:
        article, created = Article.objects.get_or_create(
            titre=article_data['titre'],
            defaults={
                'auteur': article_data['auteur'],
                'contenu': article_data['contenu'],
                'category': category
            }
        )
        
        if created:
            print(f"✅ Article créé: '{article.titre}' par {article.auteur}")
            
            # Créer un commentaire pour cet article
            Comment.objects.create(
                article=article,
                nom='Test Commentateur',
                email='test@comment.com',
                contenu='Ceci est un commentaire de test'
            )
            print(f"✅ Commentaire ajouté à l'article '{article.titre}'")
        else:
            print(f"ℹ️  Article existe déjà: '{article.titre}'")

if __name__ == '__main__':
    print("🚀 Démarrage du test des statistiques journaliste\n")
    
    # Créer des données de test si nécessaire
    create_test_data()
    print()
    
    # Tester les statistiques
    test_journalist_stats()
    
    print("\n✅ Test terminé!")
