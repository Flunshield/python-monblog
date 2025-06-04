"""
Tests pour la modération des commentaires
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Article, Comment, Category, UserProfile


class CommentModerationTest(TestCase):
    def setUp(self):
        """Configuration des données de test"""
        # Créer une catégorie
        self.category = Category.objects.create(
            nom="Test Category",
            description="Description de test"
        )
        
        # Créer des utilisateurs
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='testpass123'
        )
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user,
            role='admin'
        )
        
        self.journalist_user = User.objects.create_user(
            username='journalist_test',
            email='journalist@test.com',
            password='testpass123'
        )
        self.journalist_profile = UserProfile.objects.create(
            user=self.journalist_user,
            role='journaliste'
        )
        
        self.reader_user = User.objects.create_user(
            username='reader_test',
            email='reader@test.com',
            password='testpass123'
        )
        self.reader_profile = UserProfile.objects.create(
            user=self.reader_user,
            role='lecteur'
        )
        
        # Créer des articles
        self.admin_article = Article.objects.create(
            titre="Article Admin",
            contenu="Contenu de l'article admin",
            auteur="admin_test",
            category=self.category
        )
        
        self.journalist_article = Article.objects.create(
            titre="Article Journaliste",
            contenu="Contenu de l'article journaliste",
            auteur="journalist_test",
            category=self.category
        )
        
        # Créer des commentaires
        self.approved_comment = Comment.objects.create(
            article=self.admin_article,
            nom="Utilisateur Test",
            email="user@test.com",
            contenu="Commentaire approuvé",
            is_approved=True
        )
        
        self.pending_comment = Comment.objects.create(
            article=self.journalist_article,
            nom="Autre Utilisateur",
            email="autre@test.com",
            contenu="Commentaire en attente",
            is_approved=False
        )
        
        self.client = Client()

    def test_moderation_access_admin(self):
        """Test d'accès à la modération pour un admin"""
        self.client.login(username='admin_test', password='testpass123')
        response = self.client.get(reverse('comment_moderation'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modération des commentaires")
        self.assertContains(response, "Admin")

    def test_moderation_access_journalist(self):
        """Test d'accès à la modération pour un journaliste"""
        self.client.login(username='journalist_test', password='testpass123')
        response = self.client.get(reverse('comment_moderation'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modération des commentaires")
        self.assertContains(response, "Journaliste")

    def test_moderation_access_denied_reader(self):
        """Test de refus d'accès à la modération pour un lecteur"""
        self.client.login(username='reader_test', password='testpass123')
        response = self.client.get(reverse('comment_moderation'))
        
        self.assertEqual(response.status_code, 403)

    def test_admin_sees_all_comments(self):
        """Test que l'admin voit tous les commentaires"""
        self.client.login(username='admin_test', password='testpass123')
        response = self.client.get(reverse('comment_moderation'))
        
        self.assertContains(response, self.approved_comment.contenu)
        self.assertContains(response, self.pending_comment.contenu)

    def test_journalist_sees_only_own_article_comments(self):
        """Test que le journaliste ne voit que les commentaires sur ses articles"""
        self.client.login(username='journalist_test', password='testpass123')
        response = self.client.get(reverse('comment_moderation'))
        
        # Le journaliste devrait voir le commentaire sur son article
        self.assertContains(response, self.pending_comment.contenu)
        # Mais pas le commentaire sur l'article de l'admin
        self.assertNotContains(response, self.approved_comment.contenu)

    def test_approve_comment(self):
        """Test d'approbation d'un commentaire"""
        self.client.login(username='admin_test', password='testpass123')
        
        response = self.client.post(reverse('comment_moderation'), {
            'action': 'approve',
            'comment_id': self.pending_comment.id
        })
        
        self.assertEqual(response.status_code, 302)  # Redirection
        
        # Vérifier que le commentaire a été approuvé
        self.pending_comment.refresh_from_db()
        self.assertTrue(self.pending_comment.is_approved)

    def test_disapprove_comment(self):
        """Test de désapprobation d'un commentaire"""
        self.client.login(username='admin_test', password='testpass123')
        
        response = self.client.post(reverse('comment_moderation'), {
            'action': 'disapprove',
            'comment_id': self.approved_comment.id
        })
        
        self.assertEqual(response.status_code, 302)  # Redirection
        
        # Vérifier que le commentaire a été désapprouvé
        self.approved_comment.refresh_from_db()
        self.assertFalse(self.approved_comment.is_approved)

    def test_delete_comment(self):
        """Test de suppression d'un commentaire"""
        self.client.login(username='admin_test', password='testpass123')
        comment_id = self.pending_comment.id
        
        response = self.client.post(reverse('comment_moderation'), {
            'action': 'delete',
            'comment_id': comment_id
        })
        
        self.assertEqual(response.status_code, 302)  # Redirection
        
        # Vérifier que le commentaire a été supprimé
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def test_reply_to_comment(self):
        """Test de réponse à un commentaire"""
        self.client.login(username='admin_test', password='testpass123')
        
        response = self.client.post(reverse('comment_moderation'), {
            'action': 'reply',
            'comment_id': self.approved_comment.id,
            'reply_content': 'Réponse du modérateur'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirection
        
        # Vérifier qu'une réponse a été créée
        reply = Comment.objects.filter(
            parent=self.approved_comment,
            contenu='Réponse du modérateur'
        ).first()
        
        self.assertIsNotNone(reply)
        self.assertTrue(reply.is_approved)  # Les réponses des modérateurs sont auto-approuvées
        self.assertIn("Modérateur", reply.nom)

    def test_journalist_permission_restriction(self):
        """Test que le journaliste ne peut pas modérer les commentaires d'autres articles"""
        self.client.login(username='journalist_test', password='testpass123')
        
        # Tenter de modérer un commentaire sur l'article de l'admin
        response = self.client.post(reverse('comment_moderation'), {
            'action': 'approve',
            'comment_id': self.approved_comment.id
        })
        
        self.assertEqual(response.status_code, 403)  # Accès interdit

    def test_filter_by_status(self):
        """Test du filtrage par statut"""
        self.client.login(username='admin_test', password='testpass123')
        
        # Filtrer par commentaires en attente
        response = self.client.get(reverse('comment_moderation') + '?status=pending')
        self.assertContains(response, self.pending_comment.contenu)
        
        # Filtrer par commentaires approuvés
        response = self.client.get(reverse('comment_moderation') + '?status=approved')
        self.assertContains(response, self.approved_comment.contenu)

    def test_filter_by_article(self):
        """Test du filtrage par article"""
        self.client.login(username='admin_test', password='testpass123')
        
        # Filtrer par article spécifique
        response = self.client.get(reverse('comment_moderation') + f'?article={self.admin_article.id}')
        self.assertContains(response, self.approved_comment.contenu)
        self.assertNotContains(response, self.pending_comment.contenu)

    def test_comments_display_on_article_detail(self):
        """Test que seuls les commentaires approuvés s'affichent sur la page de détail"""
        # Visiteur non connecté
        response = self.client.get(reverse('article_detail', args=[self.admin_article.id]))
        self.assertContains(response, self.approved_comment.contenu)
        
        # Vérifier pour l'article avec commentaire en attente
        response = self.client.get(reverse('article_detail', args=[self.journalist_article.id]))
        self.assertNotContains(response, self.pending_comment.contenu)

    def test_new_comments_require_approval(self):
        """Test que les nouveaux commentaires nécessitent une approbation"""
        response = self.client.post(reverse('article_detail', args=[self.admin_article.id]), {
            'nom': 'Nouveau Commentateur',
            'email': 'nouveau@test.com',
            'contenu': 'Nouveau commentaire de test'
        })
        
        # Vérifier que le commentaire a été créé mais non approuvé
        new_comment = Comment.objects.filter(contenu='Nouveau commentaire de test').first()
        self.assertIsNotNone(new_comment)
        self.assertFalse(new_comment.is_approved)


if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}},
            INSTALLED_APPS=['blog'],
        )
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['__main__'])
