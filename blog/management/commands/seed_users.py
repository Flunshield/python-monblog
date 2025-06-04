from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Role, UserProfile
from django.utils import timezone
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer des utilisateurs de test avec différents rôles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='TestPass123!',
            help='Mot de passe pour tous les utilisateurs de test (défaut: TestPass123!)'
        )

    def handle(self, *args, **options):
        password = options['password']
        self.stdout.write(self.style.SUCCESS('🚀 Début du seeding des utilisateurs...'))
        
        # S'assurer que les rôles existent
        roles = Role.get_default_roles()
        
        users_data = [
            {
                'username': 'admin_test',
                'email': 'admin@test.com',
                'first_name': 'Admin',
                'last_name': 'Test',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'journaliste_test',
                'email': 'journaliste@test.com',
                'first_name': 'Jean',
                'last_name': 'Journaliste',
                'role': 'journaliste',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'moderateur_test',
                'email': 'moderateur@test.com',
                'first_name': 'Marie',
                'last_name': 'Modératrice',
                'role': 'modérateur',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'editeur_test',
                'email': 'editeur@test.com',
                'first_name': 'Paul',
                'last_name': 'Éditeur',
                'role': 'éditeur',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'lecteur_test',
                'email': 'lecteur@test.com',
                'first_name': 'Sophie',
                'last_name': 'Lectrice',
                'role': 'lecteur',
                'is_staff': False,
                'is_superuser': False
            },
            {
                'username': 'lecteur2_test',
                'email': 'lecteur2@test.com',
                'first_name': 'Thomas',
                'last_name': 'Lecteur',
                'role': 'lecteur',
                'is_staff': False,
                'is_superuser': False
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_staff': user_data['is_staff'],
                    'is_superuser': user_data['is_superuser'],
                    'is_active': True,
                    'date_joined': timezone.now()
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                
                # Créer le profil avec le bon rôle
                role_name = user_data['role']
                if role_name in roles:
                    role = roles[role_name]
                else:
                    # Si le rôle n'existe pas dans les rôles par défaut, le créer ou le trouver
                    role, _ = Role.objects.get_or_create(name=role_name)
                
                # Créer ou mettre à jour le profil
                profile, profile_created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': role,
                        'date_creation': timezone.now()
                    }
                )
                
                if not profile_created:
                    profile.role = role
                    profile.save()
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Utilisateur créé: {user.username} ({role.name})'
                    )
                )
                logger.info(f"Utilisateur créé lors du seeding: {user.username} avec rôle {role.name}")
                
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Utilisateur existant: {user.username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Résumé du seeding des utilisateurs:\n'
                f'   - Utilisateurs créés: {created_count}\n'
                f'   - Utilisateurs existants: {existing_count}\n'
                f'   - Total: {created_count + existing_count}\n'
                f'   - Mot de passe utilisé: {password}'
            )
        )
