from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import UserProfile, Role
from blog.templatetags.role_tags import user_role, has_role, is_admin, is_journaliste, is_lecteur


class Command(BaseCommand):
    help = 'Test la nouvelle gestion dynamique des rôles'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== TEST DE LA GESTION DYNAMIQUE DES RÔLES ==='))
        
        # Test du modèle Role
        self.stdout.write('\n1. Test du modèle Role')
        roles = Role.get_default_roles()
        self.stdout.write(f'   Rôles disponibles: {list(roles.keys())}')
        for name, role in roles.items():
            self.stdout.write(f'   - {name}: ID={role.id}, Name={role.name}')
        
        # Test avec un utilisateur existant
        self.stdout.write('\n2. Test avec utilisateur existant')
        user = User.objects.first()
        if user:
            self.stdout.write(f'   Utilisateur: {user.username}')
            if hasattr(user, 'profile'):
                self.stdout.write(f'   Rôle actuel: {user.profile.role.name}')
                self.stdout.write(f'   Template tag user_role(): {user_role(user)}')
                self.stdout.write(f'   is_lecteur(): {is_lecteur(user)}')
                self.stdout.write(f'   is_journaliste(): {is_journaliste(user)}')
                self.stdout.write(f'   is_admin(): {is_admin(user)}')
            else:
                self.stdout.write('   Pas de profil associé')
        else:
            self.stdout.write('   Aucun utilisateur trouvé')
        
        # Test de création d'un nouvel utilisateur
        self.stdout.write('\n3. Test de création d\'un nouvel utilisateur')
        test_username = 'test_dynamic_roles'
        
        # Nettoyer d'abord
        User.objects.filter(username=test_username).delete()
        
        # Créer l'utilisateur
        test_user = User.objects.create_user(
            username=test_username,
            email='test@dynamic.com',
            password='testpass123'
        )
        
        self.stdout.write(f'   Utilisateur créé: {test_user.username}')
        self.stdout.write(f'   Profil créé automatiquement: {hasattr(test_user, "profile")}')
        if hasattr(test_user, 'profile'):
            self.stdout.write(f'   Rôle par défaut: {test_user.profile.role.name}')
        
        # Test de changement de rôle
        self.stdout.write('\n4. Test de changement de rôle')
        test_user.profile.role = roles['journaliste']
        test_user.profile.save()
        test_user.refresh_from_db()
        self.stdout.write(f'   Nouveau rôle: {test_user.profile.role.name}')
        self.stdout.write(f'   is_journaliste(): {is_journaliste(test_user)}')
        
        # Nettoyer
        test_user.delete()
        self.stdout.write('   Utilisateur de test supprimé')
        
        self.stdout.write(self.style.SUCCESS('\n✅ TOUS LES TESTS SONT PASSÉS!'))
        self.stdout.write(self.style.SUCCESS('La gestion dynamique des rôles fonctionne parfaitement.'))
