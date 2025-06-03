"""
Tests pour la fonctionnalité Like/Bookmark des articles
"""
import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Article, Like, Category


class LikeFunctionalityTestCase(TestCase):
    def setUp(self):
        """Configuration des données de test"""
        self.client = Client()
        
        # Créer des utilisateurs
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@test.com',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@test.com',
            password='testpass123'
        )
        
        # Créer une catégorie
        self.category = Category.objects.create(
            nom='Test Category',
            description='Description de test'
        )
        
        # Créer un article
        self.article = Article.objects.create(
            titre='Article de test',
            contenu='Contenu de test pour l\'article',
            auteur='TestAuthor',
            category=self.category
        )

    def test_like_model_creation(self):
        """Test de création d'un Like"""
        # Créer un like
        like = Like.objects.create(
            user=self.user1,
            article=self.article
        )
        
        # Vérifier que le like a été créé
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(like.user, self.user1)
        self.assertEqual(like.article, self.article)
        
    def test_unique_constraint(self):
        """Test de la contrainte d'unicité user-article"""
        # Créer un premier like
        Like.objects.create(user=self.user1, article=self.article)
        
        # Essayer de créer un deuxième like pour le même couple
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user1, article=self.article)
    
    def test_article_methods(self):
        """Test des méthodes get_total_likes et is_liked_by"""
        # Initialement, aucun like
        self.assertEqual(self.article.get_total_likes(), 0)
        self.assertFalse(self.article.is_liked_by(self.user1))
        
        # Ajouter un like
        Like.objects.create(user=self.user1, article=self.article)
        
        # Vérifier les compteurs
        self.assertEqual(self.article.get_total_likes(), 1)
        self.assertTrue(self.article.is_liked_by(self.user1))
        self.assertFalse(self.article.is_liked_by(self.user2))
        
        # Ajouter un deuxième like d'un autre utilisateur
        Like.objects.create(user=self.user2, article=self.article)
        
        # Vérifier le nouveau total
        self.assertEqual(self.article.get_total_likes(), 2)
        self.assertTrue(self.article.is_liked_by(self.user2))

    def test_toggle_like_view_authentication(self):
        """Test que la vue nécessite une authentification"""
        response = self.client.post(
            reverse('toggle_like', args=[self.article.id])
        )
        # Doit rediriger vers la page de login
        self.assertEqual(response.status_code, 302)

    def test_toggle_like_view_functionality(self):
        """Test du fonctionnement de la vue toggle_like"""
        # Se connecter
        self.client.login(username='testuser1', password='testpass123')
        
        # Premier clic - créer un like
        response = self.client.post(
            reverse('toggle_like', args=[self.article.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertTrue(data['liked'])
        self.assertEqual(data['total_likes'], 1)
        
        # Vérifier que le like a été créé en base
        self.assertEqual(Like.objects.count(), 1)
        self.assertTrue(self.article.is_liked_by(self.user1))
        
        # Deuxième clic - supprimer le like
        response = self.client.post(
            reverse('toggle_like', args=[self.article.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertFalse(data['liked'])
        self.assertEqual(data['total_likes'], 0)
        
        # Vérifier que le like a été supprimé
        self.assertEqual(Like.objects.count(), 0)
        self.assertFalse(self.article.is_liked_by(self.user1))

    def test_multiple_users_likes(self):
        """Test avec plusieurs utilisateurs"""
        # User1 like l'article
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.post(
            reverse('toggle_like', args=[self.article.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        data = json.loads(response.content)
        self.assertEqual(data['total_likes'], 1)
        
        # User2 like aussi l'article
        self.client.login(username='testuser2', password='testpass123')
        response = self.client.post(
            reverse('toggle_like', args=[self.article.id]),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        data = json.loads(response.content)
        self.assertEqual(data['total_likes'], 2)
        
        # Vérifier en base
        self.assertEqual(Like.objects.count(), 2)
        self.assertEqual(self.article.get_total_likes(), 2)

    def test_article_deletion_cascades_likes(self):
        """Test que la suppression d'un article supprime ses likes"""
        # Créer des likes
        Like.objects.create(user=self.user1, article=self.article)
        Like.objects.create(user=self.user2, article=self.article)
        
        self.assertEqual(Like.objects.count(), 2)
        
        # Supprimer l'article
        self.article.delete()
        
        # Les likes doivent être supprimés aussi (CASCADE)
        self.assertEqual(Like.objects.count(), 0)

    def test_user_deletion_cascades_likes(self):
        """Test que la suppression d'un utilisateur supprime ses likes"""
        # Créer un like
        Like.objects.create(user=self.user1, article=self.article)
        
        self.assertEqual(Like.objects.count(), 1)
        
        # Supprimer l'utilisateur
        self.user1.delete()
        
        # Le like doit être supprimé aussi (CASCADE)
        self.assertEqual(Like.objects.count(), 0)
