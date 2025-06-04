#!/usr/bin/env python
"""
Tests Django pour vérifier la nouvelle gestion dynamique des rôles via la base de données.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import UserProfile, Role
from blog.templatetags.role_tags import user_role, has_role, is_admin, is_journaliste, is_lecteur


class DynamicRolesTestCase(TestCase):
    """Tests pour la gestion dynamique des rôles"""

    def setUp(self):
        """Configuration des tests"""
        # Créer les rôles par défaut
        Role.get_default_roles()
        
        # Créer un utilisateur de test
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_role_model_creation(self):
        """Test de création du modèle Role"""
        # Vérifier que les rôles par défaut sont créés
        roles = Role.get_default_roles()
        self.assertIn('lecteur', roles)
        self.assertIn('journaliste', roles)
        self.assertIn('admin', roles)
        
        # Vérifier que les objets sont bien créés en base
        self.assertTrue(Role.objects.filter(name='lecteur').exists())
        self.assertTrue(Role.objects.filter(name='journaliste').exists())
        self.assertTrue(Role.objects.filter(name='admin').exists())

    def test_user_profile_default_role(self):
        """Test que les nouveaux utilisateurs ont le rôle lecteur par défaut"""
        # Le profil devrait être créé automatiquement
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.role.name, 'lecteur')

    def test_template_tags_with_dynamic_roles(self):
        """Test des template tags avec les rôles dynamiques"""
        # Test avec rôle lecteur (par défaut)
        self.assertEqual(user_role(self.user), 'lecteur')
        self.assertTrue(has_role(self.user, 'lecteur'))
        self.assertTrue(is_lecteur(self.user))
        self.assertFalse(is_journaliste(self.user))
        self.assertFalse(is_admin(self.user))

    def test_role_change(self):
        """Test du changement de rôle"""
        # Changer le rôle vers journaliste
        journaliste_role = Role.objects.get(name='journaliste')
        self.user.profile.role = journaliste_role
        self.user.profile.save()
        
        # Vérifier le changement
        self.assertEqual(self.user.profile.role.name, 'journaliste')
        self.assertTrue(is_journaliste(self.user))
        self.assertFalse(is_lecteur(self.user))
        self.assertFalse(is_admin(self.user))
        
        # Changer vers admin
        admin_role = Role.objects.get(name='admin')
        self.user.profile.role = admin_role
        self.user.profile.save()
        
        # Vérifier le changement
        self.assertEqual(self.user.profile.role.name, 'admin')
        self.assertTrue(is_admin(self.user))
        self.assertFalse(is_journaliste(self.user))
        self.assertFalse(is_lecteur(self.user))

    def test_role_model_integrity(self):
        """Test de l'intégrité du modèle Role"""
        # Créer un rôle personnalisé
        custom_role = Role.objects.create(name='moderateur')
        self.assertEqual(custom_role.name, 'moderateur')
        
        # Assigner ce rôle à un utilisateur
        self.user.profile.role = custom_role
        self.user.profile.save()
        
        self.assertEqual(self.user.profile.role.name, 'moderateur')

    def test_multiple_users_different_roles(self):
        """Test avec plusieurs utilisateurs ayant des rôles différents"""
        # Créer d'autres utilisateurs
        user2 = User.objects.create_user(
            username='journalist',
            email='journalist@example.com',
            password='testpass123'
        )
        
        user3 = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        
        # Assigner des rôles différents
        journaliste_role = Role.objects.get(name='journaliste')
        admin_role = Role.objects.get(name='admin')
        
        user2.profile.role = journaliste_role
        user2.profile.save()
        
        user3.profile.role = admin_role
        user3.profile.save()
        
        # Vérifier les rôles
        self.assertEqual(self.user.profile.role.name, 'lecteur')  # rôle par défaut
        self.assertEqual(user2.profile.role.name, 'journaliste')
        self.assertEqual(user3.profile.role.name, 'admin')
        
        # Vérifier les template tags
        self.assertTrue(is_lecteur(self.user))
        self.assertTrue(is_journaliste(user2))
        self.assertTrue(is_admin(user3))

    def test_role_deletion_protection(self):
        """Test que la suppression d'un rôle utilisé est protégée"""
        # Tenter de supprimer un rôle utilisé devrait lever une exception
        from django.db.models import ProtectedError
        
        with self.assertRaises(ProtectedError):
            # Le rôle lecteur est utilisé par self.user
            lecteur_role = Role.objects.get(name='lecteur')
            lecteur_role.delete()

    def tearDown(self):
        """Nettoyage après les tests"""
        # Les tests Django nettoient automatiquement la base de données
        pass
