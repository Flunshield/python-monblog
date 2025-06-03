from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import UserProfile, Category


class JournalistCategoryAccessTest(TestCase):
    def setUp(self):
        """Configuration initiale pour les tests"""
        self.client = Client()
        
        # Créer les utilisateurs
        self.admin_user = User.objects.create_user(username='admin', password='admin123')
        self.journalist_user = User.objects.create_user(username='journalist', password='journalist123')
        self.reader_user = User.objects.create_user(username='reader', password='reader123')
        
        # Créer ou mettre à jour les profils avec les rôles appropriés
        admin_profile, _ = UserProfile.objects.get_or_create(user=self.admin_user)
        admin_profile.role = 'admin'
        admin_profile.save()
        
        journalist_profile, _ = UserProfile.objects.get_or_create(user=self.journalist_user)
        journalist_profile.role = 'journaliste'
        journalist_profile.save()
        
        reader_profile, _ = UserProfile.objects.get_or_create(user=self.reader_user)
        reader_profile.role = 'lecteur'
        reader_profile.save()
        
        # Créer une catégorie de test
        self.test_category = Category.objects.create(
            nom='Test Category',
            description='Une catégorie de test'
        )

    def test_journalist_can_access_category_page(self):
        """Test que le journaliste peut accéder à la page de gestion des catégories"""
        self.client.login(username='journalist', password='journalist123')
        response = self.client.get(reverse('gerer_categories'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gestion des catégories')
        self.assertContains(response, 'Test Category')

    def test_journalist_cannot_see_action_buttons(self):
        """Test que le journaliste ne voit pas les boutons d'action"""
        self.client.login(username='journalist', password='journalist123')
        response = self.client.get(reverse('gerer_categories'))
        
        # Vérifier que les boutons d'action ne sont pas présents
        self.assertNotContains(response, 'Ajouter une catégorie')
        self.assertNotContains(response, 'bi-pencil')  # Icône modifier
        self.assertNotContains(response, 'bi-trash')   # Icône supprimer
        self.assertContains(response, 'Mode consultation')

    def test_admin_can_see_action_buttons(self):
        """Test que l'administrateur voit les boutons d'action"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('gerer_categories'))
        
        # Vérifier que les boutons d'action sont présents
        self.assertContains(response, 'Ajouter une catégorie')
        self.assertContains(response, 'bi-pencil')  # Icône modifier
        self.assertContains(response, 'bi-trash')   # Icône supprimer

    def test_reader_cannot_access_category_page(self):
        """Test qu'un lecteur ne peut pas accéder à la page de gestion des catégories"""
        self.client.login(username='reader', password='reader123')
        response = self.client.get(reverse('gerer_categories'))
        
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_journalist_cannot_add_category(self):
        """Test qu'un journaliste ne peut pas ajouter de catégorie"""
        self.client.login(username='journalist', password='journalist123')
        response = self.client.get(reverse('ajouter_categorie'))
        
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_journalist_cannot_modify_category(self):
        """Test qu'un journaliste ne peut pas modifier une catégorie"""
        self.client.login(username='journalist', password='journalist123')
        response = self.client.get(reverse('modifier_categorie', args=[self.test_category.id]))
        
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_journalist_cannot_delete_category(self):
        """Test qu'un journaliste ne peut pas supprimer une catégorie"""
        self.client.login(username='journalist', password='journalist123')
        response = self.client.get(reverse('supprimer_categorie', args=[self.test_category.id]))
        
        self.assertEqual(response.status_code, 403)  # Forbidden    def test_journalist_sees_category_link_in_nav(self):
        """Test que le journaliste voit le lien Catégories dans la navigation"""
        self.client.login(username='journalist', password='journalist123')
        response = self.client.get(reverse('home'))
        
        self.assertContains(response, 'gerer-categories')
        self.assertContains(response, 'Catégories')

    def test_reader_does_not_see_category_link_in_nav(self):
        """Test qu'un lecteur ne voit pas le lien Catégories dans la navigation"""
        self.client.login(username='reader', password='reader123')
        response = self.client.get(reverse('home'))
        
        self.assertNotContains(response, 'href="/gerer-categories/"')


if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner

    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'blog',
            ],
            SECRET_KEY='test-secret-key',
            USE_TZ=True,
        )
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['__main__'])
