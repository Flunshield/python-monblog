"""
Test pour vérifier l'assignation automatique du rôle "lecteur" lors de la création d'un compte
"""
from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import UserProfile, Role


class TestAutomaticRoleAssignment(TestCase):
    """Tests pour l'assignation automatique des rôles"""
    
    def setUp(self):
        """Initialisation des tests"""
        # S'assurer que les rôles par défaut existent
        Role.get_default_roles()
    
    def test_user_creation_assigns_lecteur_role(self):
        """Test que la création d'un utilisateur lui assigne automatiquement le rôle lecteur"""
        # Créer un nouvel utilisateur
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Vérifier que l'utilisateur a un profil
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsNotNone(user.profile)
        
        # Vérifier que le rôle est "lecteur"
        self.assertEqual(user.profile.role.name, 'lecteur')
        
        print("✅ Test assignation automatique rôle lecteur OK")
    
    def test_user_creation_with_superuser(self):
        """Test que même les superusers reçoivent le rôle lecteur par défaut"""
        # Créer un superuser
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        
        # Vérifier que même le superuser a un profil avec rôle lecteur par défaut
        self.assertTrue(hasattr(superuser, 'profile'))
        self.assertEqual(superuser.profile.role.name, 'lecteur')
        
        print("✅ Test assignation automatique rôle lecteur pour superuser OK")
    
    def test_profile_creation_without_role(self):
        """Test la création d'un profil sans rôle spécifique (doit assigner lecteur)"""
        # Créer un utilisateur
        user = User.objects.create_user(
            username='usertest2',
            email='test2@example.com',
            password='testpassword123'
        )
        
        # Supprimer le profil existant pour tester la création manuelle
        if hasattr(user, 'profile'):
            user.profile.delete()
        
        # Créer un nouveau profil sans spécifier de rôle
        profile = UserProfile.objects.create(user=user)
        
        # Vérifier que le rôle lecteur a été assigné automatiquement
        self.assertEqual(profile.role.name, 'lecteur')
        
        print("✅ Test création manuelle profil sans rôle OK")
    
    def test_role_defaults_exist(self):
        """Test que les rôles par défaut sont bien créés"""
        default_roles = Role.get_default_roles()
        
        # Vérifier que tous les rôles par défaut existent
        self.assertIn('lecteur', default_roles)
        self.assertIn('journaliste', default_roles)
        self.assertIn('admin', default_roles)
        
        # Vérifier qu'ils sont bien des instances de Role
        self.assertIsInstance(default_roles['lecteur'], Role)
        self.assertIsInstance(default_roles['journaliste'], Role)
        self.assertIsInstance(default_roles['admin'], Role)
        
        # Vérifier que les noms sont corrects
        self.assertEqual(default_roles['lecteur'].name, 'lecteur')
        self.assertEqual(default_roles['journaliste'].name, 'journaliste')
        self.assertEqual(default_roles['admin'].name, 'admin')
        
        print("✅ Test rôles par défaut OK")
    
    def test_multiple_users_creation(self):
        """Test la création de plusieurs utilisateurs successifs"""
        users_data = [
            {'username': 'user1', 'email': 'user1@example.com'},
            {'username': 'user2', 'email': 'user2@example.com'},
            {'username': 'user3', 'email': 'user3@example.com'},
        ]
        
        for user_data in users_data:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password='password123'
            )
            
            # Vérifier que chaque utilisateur a le rôle lecteur
            self.assertTrue(hasattr(user, 'profile'))
            self.assertEqual(user.profile.role.name, 'lecteur')
        
        print("✅ Test création multiple utilisateurs OK")


if __name__ == '__main__':
    # Exécution directe du test
    import django
    import os
    import sys
    
    # Configuration Django
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
    django.setup()
    
    # Exécution des tests
    test_case = TestAutomaticRoleAssignment()
    test_case.setUp()
    
    try:
        test_case.test_user_creation_assigns_lecteur_role()
        test_case.test_user_creation_with_superuser()
        test_case.test_profile_creation_without_role()
        test_case.test_role_defaults_exist()
        test_case.test_multiple_users_creation()
        
        print("\n🎉 Tous les tests d'assignation automatique des rôles sont passés avec succès!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
