#!/usr/bin/env python
"""
Script pour corriger les données de test
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Comment, UserProfile, Category

def fix_test_data():
    """Corriger les données de test"""
    print("=== Correction des données de test ===\n")
    
    # Corriger le rôle de testjournalist
    try:
        user = User.objects.get(username='testjournalist')
        profile = user.profile
        profile.role = 'journaliste'
        profile.save()
        print(f"✅ Rôle de {user.username} mis à jour vers 'journaliste'")
    except User.DoesNotExist:
        print("❌ Utilisateur testjournalist non trouvé")
    except UserProfile.DoesNotExist:
        print("❌ Profil de testjournalist non trouvé")
    
    # Créer un utilisateur 'Forbes' pour les articles existants
    forbes_user, created = User.objects.get_or_create(
        username='Forbes',
        defaults={
            'first_name': 'Forbes',
            'last_name': 'Magazine',
            'email': 'forbes@test.com'
        }
    )
    
    if created:
        print(f"✅ Utilisateur Forbes créé: {forbes_user.username}")
        # Créer le profil
        UserProfile.objects.get_or_create(
            user=forbes_user,
            defaults={'role': 'journaliste'}
        )
        print(f"✅ Profil journaliste créé pour {forbes_user.username}")
    else:
        print(f"ℹ️  Utilisateur Forbes existe déjà: {forbes_user.username}")
        # S'assurer qu'il a un profil journaliste
        profile, created = UserProfile.objects.get_or_create(
            user=forbes_user,
            defaults={'role': 'journaliste'}
        )
        if not created and profile.role != 'journaliste':
            profile.role = 'journaliste'
            profile.save()
            print(f"✅ Rôle de Forbes mis à jour vers 'journaliste'")

    print("\n=== Vérification des utilisateurs journalistes ===")
    journalists = User.objects.filter(profile__role='journaliste')
    for user in journalists:
        print(f"👤 {user.username} ({user.first_name} {user.last_name})")
        
        # Compter les articles
        user_articles = Article.objects.filter(auteur__icontains=user.username)
        if not user_articles.exists() and user.first_name:
            user_articles = Article.objects.filter(auteur__icontains=user.first_name)
        if not user_articles.exists() and user.last_name:
            user_articles = Article.objects.filter(auteur__icontains=user.last_name)
        if not user_articles.exists():
            user_articles = Article.objects.filter(auteur=user.username)
            
        print(f"   📰 Articles: {user_articles.count()}")
        for article in user_articles:
            print(f"      - '{article.titre}' (auteur: {article.auteur})")
        
        # Compter les commentaires
        user_comments = Comment.objects.filter(article__in=user_articles)
        print(f"   💬 Commentaires reçus: {user_comments.count()}")
        print()

if __name__ == '__main__':
    fix_test_data()
    print("✅ Correction terminée!")
