"""
Tests unitaires pour la fonctionnalité Like/Bookmark des articles.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.utils import IntegrityError
import json

from blog.models import Article, Category, Like


class LikeModelTestCase(TestCase):
    """Tests pour le modèle Like."""
    
    def setUp(self):
        """Configuration des données de test."""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com',
            password='testpass123'
        )
        
        self.category = Category.objects.create(
            nom='Test Category',
            description='Une catégorie de test'
        )
        
        self.article = Article.objects.create(
            titre='Article de Test',
            contenu='Contenu de test pour l\'article.',
            auteur='Test Author',
            category=self.category
        )
    
    def test_like_creation(self):
        """Test de création d'un like."""
        like = Like.objects.create(
            user=self.user1,
            article=self.article
        )
        
        self.assertEqual(like.user, self.user1)
        self.assertEqual(like.article, self.article)
        self.assertIsNotNone(like.created_at)
        self.assertIsNotNone(like.updated_at)
    
    def test_like_str_method(self):
        """Test de la méthode __str__ du modèle Like."""
        like = Like.objects.create(
            user=self.user1,
            article=self.article
        )
        
        expected_str = f'{self.user1.username} likes {self.article.titre}'
        self.assertEqual(str(like), expected_str)
    
    def test_unique_like_constraint(self):
        """Test de la contrainte d'unicité (un utilisateur ne peut liker qu'une fois)."""
        # Créer le premier like
        Like.objects.create(
            user=self.user1,
            article=self.article
        )
        
        # Tenter de créer un second like pour le même couple user/article
        with self.assertRaises(IntegrityError):
            Like.objects.create(
                user=self.user1,
                article=self.article
            )
    
    def test_multiple_users_can_like_same_article(self):
        """Test que plusieurs utilisateurs peuvent liker le même article."""
        like1 = Like.objects.create(
            user=self.user1,
            article=self.article
        )
        like2 = Like.objects.create(
            user=self.user2,
            article=self.article
        )
        
        self.assertEqual(Like.objects.filter(article=self.article).count(), 2)
        self.assertNotEqual(like1.user, like2.user)
    
    def test_user_can_like_multiple_articles(self):
        """Test qu'un utilisateur peut liker plusieurs articles."""
        article2 = Article.objects.create(
            titre='Second Article',
            contenu='Contenu du second article.',
            auteur='Test Author',
            category=self.category
        )
        
        like1 = Like.objects.create(
            user=self.user1,
            article=self.article
        )
        like2 = Like.objects.create(
            user=self.user1,
            article=article2
        )
        
        self.assertEqual(Like.objects.filter(user=self.user1).count(), 2)
        self.assertNotEqual(like1.article, like2.article)


class ArticleLikeMethodsTestCase(TestCase):
    """Tests pour les méthodes de like ajoutées au modèle Article."""
    
    def setUp(self):
        """Configuration des données de test."""
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        self.category = Category.objects.create(nom='Test Category')
        self.article = Article.objects.create(
            titre='Article de Test',
            contenu='Contenu de test.',
            auteur='Test Author',
            category=self.category
        )
    
    def test_get_total_likes_empty(self):
        """Test du comptage de likes quand il n'y en a aucun."""
        self.assertEqual(self.article.get_total_likes(), 0)
    
    def test_get_total_likes_with_likes(self):
        """Test du comptage de likes avec plusieurs likes."""
        Like.objects.create(user=self.user1, article=self.article)
        Like.objects.create(user=self.user2, article=self.article)
        
        self.assertEqual(self.article.get_total_likes(), 2)
    
    def test_is_liked_by_authenticated_user_true(self):
        """Test is_liked_by pour un utilisateur qui a liké l'article."""
        Like.objects.create(user=self.user1, article=self.article)
        
        self.assertTrue(self.article.is_liked_by(self.user1))
    
    def test_is_liked_by_authenticated_user_false(self):
        """Test is_liked_by pour un utilisateur qui n'a pas liké l'article."""
        self.assertFalse(self.article.is_liked_by(self.user1))
    
    def test_is_liked_by_anonymous_user(self):
        """Test is_liked_by pour un utilisateur anonyme."""
        from django.contrib.auth.models import AnonymousUser
        anonymous_user = AnonymousUser()
        
        self.assertFalse(self.article.is_liked_by(anonymous_user))


class LikeViewTestCase(TestCase):
    """Tests pour la vue toggle_like."""
    
    def setUp(self):
        """Configuration des données de test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.category = Category.objects.create(nom='Test Category')
        self.article = Article.objects.create(
            titre='Article de Test',
            contenu='Contenu de test.',
            auteur='Test Author',
            category=self.category
        )
        
        self.like_url = reverse('toggle_like', args=[self.article.id])
    
    def test_toggle_like_requires_authentication(self):
        """Test que la vue nécessite une authentification."""
        response = self.client.post(self.like_url)
        
        # Doit rediriger vers la page de login
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_toggle_like_requires_post(self):
        """Test que la vue nécessite une requête POST."""
        self.client.login(username='testuser', password='testpass123')
        
        # Test avec GET
        response = self.client.get(self.like_url)
        self.assertEqual(response.status_code, 405)  # Method Not Allowed
    
    def test_toggle_like_create_like(self):
        """Test de création d'un nouveau like."""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(self.like_url)
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 1)
        
        # Vérifier en base de données
        self.assertTrue(Like.objects.filter(user=self.user, article=self.article).exists())
    
    def test_toggle_like_remove_like(self):
        """Test de suppression d'un like existant."""
        # Créer d'abord un like
        Like.objects.create(user=self.user, article=self.article)
        
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(self.like_url)
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['liked'])
        self.assertEqual(data['total_likes'], 0)
        
        # Vérifier en base de données
        self.assertFalse(Like.objects.filter(user=self.user, article=self.article).exists())
    
    def test_toggle_like_nonexistent_article(self):
        """Test avec un article qui n'existe pas."""
        self.client.login(username='testuser', password='testpass123')
        
        nonexistent_url = reverse('toggle_like', args=[99999])
        response = self.client.post(nonexistent_url)
        
        self.assertEqual(response.status_code, 404)


class LikeIntegrationTestCase(TestCase):
    """Tests d'intégration pour la fonctionnalité de like complète."""
    
    def setUp(self):
        """Configuration des données de test."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.category = Category.objects.create(nom='Test Category')
        self.article = Article.objects.create(
            titre='Article de Test',
            contenu='Contenu de test.',
            auteur='Test Author',
            category=self.category
        )
    
    def test_like_workflow_complete(self):
        """Test du workflow complet : like → unlike → like."""
        self.client.login(username='testuser', password='testpass123')
        like_url = reverse('toggle_like', args=[self.article.id])
        
        # 1. Premier like
        response = self.client.post(like_url)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 1)
        
        # 2. Unlike
        response = self.client.post(like_url)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertFalse(data['liked'])
        self.assertEqual(data['total_likes'], 0)
        
        # 3. Re-like
        response = self.client.post(like_url)
        data = json.loads(response.content)
        
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 1)
    
    def test_multiple_users_like_workflow(self):
        """Test avec plusieurs utilisateurs qui likent le même article."""
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        
        like_url = reverse('toggle_like', args=[self.article.id])
        
        # User 1 like
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(like_url)
        data = json.loads(response.content)
        self.assertEqual(data['total_likes'], 1)
        
        # User 2 like
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(like_url)
        data = json.loads(response.content)
        self.assertEqual(data['total_likes'], 2)
        
        # User 1 unlike
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(like_url)
        data = json.loads(response.content)
        self.assertEqual(data['total_likes'], 1)
