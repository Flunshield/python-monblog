"""
Test des restrictions de rôles pour la gestion des catégories
"""
import os
import sys
import django

# Configuration Django pour les tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import UserProfile, Category


class CategoryRoleRestrictionsTest(TestCase):
    """Tests pour vérifier que seuls les admins peuvent gérer les catégories"""
    
    def setUp(self):
        """Configuration initiale pour chaque test"""
        self.client = Client()
        
        # Créer différents types d'utilisateurs
        self.admin_user = User.objects.create_user(
            username='admin_test',
            password='testpass123'
        )
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user,
            role='admin'
        )
        
        self.journaliste_user = User.objects.create_user(
            username='journaliste_test',
            password='testpass123'
        )
        self.journaliste_profile = UserProfile.objects.create(
            user=self.journaliste_user,
            role='journaliste'
        )
        
        self.lecteur_user = User.objects.create_user(
            username='lecteur_test',
            password='testpass123'
        )
        self.lecteur_profile = UserProfile.objects.create(
            user=self.lecteur_user,
            role='lecteur'
        )
        
        # Créer une catégorie de test
        self.test_category = Category.objects.create(
            nom='Catégorie Test',
            description='Une catégorie pour les tests'
        )
    
    def test_admin_can_access_category_management(self):
        """Test que l'admin peut accéder à la gestion des catégories"""
        self.client.login(username='admin_test', password='testpass123')
        
        # Test d'accès à la page de gestion des catégories
        response = self.client.get(reverse('gerer_categories'))
        self.assertEqual(response.status_code, 200)
        
        # Test d'accès à la page d'ajout de catégorie
        response = self.client.get(reverse('ajouter_categorie'))
        self.assertEqual(response.status_code, 200)
        
        # Test d'accès à la modification
        response = self.client.get(reverse('modifier_categorie', args=[self.test_category.id]))
        self.assertEqual(response.status_code, 200)
        
        print("✅ Admin peut accéder à toutes les fonctions de gestion des catégories")
    
    def test_journaliste_cannot_access_category_management(self):
        """Test que le journaliste ne peut PAS accéder à la gestion des catégories"""
        self.client.login(username='journaliste_test', password='testpass123')
        
        # Test d'accès à la page de gestion des catégories
        response = self.client.get(reverse('gerer_categories'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test d'accès à la page d'ajout de catégorie
        response = self.client.get(reverse('ajouter_categorie'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test d'accès à la modification
        response = self.client.get(reverse('modifier_categorie', args=[self.test_category.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test d'accès à la suppression
        response = self.client.get(reverse('supprimer_categorie', args=[self.test_category.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        print("✅ Journaliste ne peut PAS accéder aux fonctions de gestion des catégories")
    
    def test_lecteur_cannot_access_category_management(self):
        """Test que le lecteur ne peut PAS accéder à la gestion des catégories"""
        self.client.login(username='lecteur_test', password='testpass123')
        
        # Test d'accès à la page de gestion des catégories
        response = self.client.get(reverse('gerer_categories'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Test d'accès à la page d'ajout de catégorie
        response = self.client.get(reverse('ajouter_categorie'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        print("✅ Lecteur ne peut PAS accéder aux fonctions de gestion des catégories")
    
    def test_anonymous_user_redirected_to_login(self):
        """Test que les utilisateurs non connectés sont redirigés vers la connexion"""
        # Test d'accès à la page de gestion des catégories
        response = self.client.get(reverse('gerer_categories'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test d'accès à la page d'ajout de catégorie
        response = self.client.get(reverse('ajouter_categorie'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        print("✅ Utilisateurs anonymes sont redirigés vers la connexion")
    
    def test_admin_can_create_category(self):
        """Test que l'admin peut créer une nouvelle catégorie"""
        self.client.login(username='admin_test', password='testpass123')
        
        category_data = {
            'nom': 'Nouvelle Catégorie',
            'description': 'Description de la nouvelle catégorie'
        }
        
        response = self.client.post(reverse('ajouter_categorie'), data=category_data)
        self.assertEqual(response.status_code, 302)  # Redirect après création réussie
        
        # Vérifier que la catégorie a été créée
        self.assertTrue(Category.objects.filter(nom='Nouvelle Catégorie').exists())
        print("✅ Admin peut créer une nouvelle catégorie")
    
    def test_journaliste_cannot_create_category(self):
        """Test que le journaliste ne peut PAS créer une nouvelle catégorie"""
        self.client.login(username='journaliste_test', password='testpass123')
        
        category_data = {
            'nom': 'Catégorie Interdite',
            'description': 'Cette catégorie ne devrait pas être créée'
        }
        
        response = self.client.post(reverse('ajouter_categorie'), data=category_data)
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Vérifier que la catégorie n'a PAS été créée
        self.assertFalse(Category.objects.filter(nom='Catégorie Interdite').exists())
        print("✅ Journaliste ne peut PAS créer une nouvelle catégorie")


def run_tests():
    """Exécute tous les tests"""
    print("🔐 Tests des restrictions de rôles pour la gestion des catégories")
    print("=" * 60)
    
    import unittest
    
    # Créer une suite de tests
    suite = unittest.TestSuite()
    suite.addTest(CategoryRoleRestrictionsTest('test_admin_can_access_category_management'))
    suite.addTest(CategoryRoleRestrictionsTest('test_journaliste_cannot_access_category_management'))
    suite.addTest(CategoryRoleRestrictionsTest('test_lecteur_cannot_access_category_management'))
    suite.addTest(CategoryRoleRestrictionsTest('test_anonymous_user_redirected_to_login'))
    suite.addTest(CategoryRoleRestrictionsTest('test_admin_can_create_category'))
    suite.addTest(CategoryRoleRestrictionsTest('test_journaliste_cannot_create_category'))
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 Tous les tests sont passés ! Les restrictions de rôles fonctionnent correctement.")
        print(f"✅ {result.testsRun} tests exécutés avec succès")
    else:
        print("❌ Certains tests ont échoué.")
        print(f"🔍 {len(result.failures)} échecs, {len(result.errors)} erreurs")
        
        for test, error in result.failures:
            print(f"❌ ÉCHEC: {test}")
            print(f"   {error}")
        
        for test, error in result.errors:
            print(f"❌ ERREUR: {test}")
            print(f"   {error}")


if __name__ == '__main__':
    run_tests()
