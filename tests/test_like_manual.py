"""
Script de test pour créer des données de test et tester la fonctionnalité Like
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Article, Category, Like

def create_test_data():
    """Créer des données de test"""
    
    # Créer un utilisateur de test s'il n'existe pas
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@test.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"Utilisateur créé: {user.username}")
    else:
        print(f"Utilisateur existant: {user.username}")
    
    # Créer une catégorie de test
    category, created = Category.objects.get_or_create(
        nom='Test Category',
        defaults={
            'description': 'Catégorie de test'
        }
    )
    if created:
        print(f"Catégorie créée: {category.nom}")
    else:
        print(f"Catégorie existante: {category.nom}")
    
    # Créer quelques articles de test
    for i in range(1, 4):
        article, created = Article.objects.get_or_create(
            titre=f'Article de test {i}',
            defaults={
                'contenu': f'Contenu de l\'article de test {i}. ' * 10,
                'auteur': 'TestAuthor',
                'category': category
            }
        )
        if created:
            print(f"Article créé: {article.titre}")
        else:
            print(f"Article existant: {article.titre}")
    
    return user

def test_like_functionality():
    """Tester la fonctionnalité Like"""
    user = create_test_data()
    
    # Récupérer le premier article
    article = Article.objects.first()
    
    print(f"\n=== Test de la fonctionnalité Like ===")
    print(f"Article: {article.titre}")
    print(f"Utilisateur: {user.username}")
    
    # État initial
    print(f"\nÉtat initial:")
    print(f"Total likes: {article.get_total_likes()}")
    print(f"Utilisateur a liké: {article.is_liked_by(user)}")
    
    # Créer un like
    like, created = Like.objects.get_or_create(user=user, article=article)
    if created:
        print(f"\nLike créé!")
    else:
        print(f"\nLike existait déjà!")
    
    # État après like
    print(f"Total likes après: {article.get_total_likes()}")
    print(f"Utilisateur a liké après: {article.is_liked_by(user)}")
    
    # Supprimer le like
    if Like.objects.filter(user=user, article=article).exists():
        Like.objects.filter(user=user, article=article).delete()
        print(f"\nLike supprimé!")
        
        # État après suppression
        print(f"Total likes final: {article.get_total_likes()}")
        print(f"Utilisateur a liké final: {article.is_liked_by(user)}")

if __name__ == '__main__':
    test_like_functionality()
