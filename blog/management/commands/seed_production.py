from django.core.management.base import BaseCommand
from blog.models import Role, Category
from django.contrib.auth.models import User
from django.utils import timezone
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer uniquement les données essentielles pour la production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--admin-password',
            type=str,
            default='ProdAdmin2024!',
            help='Mot de passe pour le compte admin (défaut: ProdAdmin2024!)'
        )
        parser.add_argument(
            '--skip-if-exists',
            action='store_true',
            help='Ignorer si des données existent déjà'
        )

    def handle(self, *args, **options):
        admin_password = options['admin_password']
        skip_if_exists = options['skip_if_exists']
        
        self.stdout.write(self.style.SUCCESS('🚀 Seeding production - données essentielles...'))
        
        # Vérifier si des données existent déjà
        if skip_if_exists:
            if Role.objects.exists() and Category.objects.exists() and User.objects.exists():
                self.stdout.write(
                    self.style.WARNING('⚠️ Données déjà présentes - seeding ignoré')
                )
                return
        
        # 1. Créer les rôles essentiels
        roles_data = [
            {'name': 'lecteur'},
            {'name': 'journaliste'},
            {'name': 'admin'},
        ]
        
        self.stdout.write('📋 Création des rôles essentiels...')
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(name=role_data['name'])
            if created:
                self.stdout.write(f'  ✅ Rôle créé: {role.name}')
            else:
                self.stdout.write(f'  ⚠️ Rôle existant: {role.name}')
        
        # 2. Créer les catégories essentielles
        categories_data = [
            {'nom': 'Actualités', 'description': 'Actualités générales'},
            {'nom': 'Technologie', 'description': 'Actualités technologiques'},
            {'nom': 'Économie', 'description': 'Actualités économiques'},
        ]
        
        self.stdout.write('📂 Création des catégories essentielles...')
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                nom=cat_data['nom'],
                defaults={
                    'description': cat_data['description'],
                    'date_creation': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'  ✅ Catégorie créée: {category.nom}')
            else:
                self.stdout.write(f'  ⚠️ Catégorie existante: {category.nom}')
          # 3. Créer les comptes essentiels pour la production
        from blog.models import UserProfile
        
        # Données des utilisateurs essentiels
        essential_users = [
            {
                'username': 'admin',
                'email': 'admin@monprojet.com',
                'first_name': 'Admin',
                'last_name': 'Principal',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True
            },
            {
                'username': 'journaliste',
                'email': 'journaliste@monprojet.com',
                'first_name': 'Jean',
                'last_name': 'Journaliste',
                'role': 'journaliste',
                'is_staff': True,
                'is_superuser': False
            },
            {
                'username': 'lecteur',
                'email': 'lecteur@monprojet.com',
                'first_name': 'Marie',
                'last_name': 'Lectrice',
                'role': 'lecteur',
                'is_staff': False,
                'is_superuser': False
            }
        ]
        
        self.stdout.write('👥 Création des comptes essentiels...')
        
        created_users = []
        existing_users = []
        
        for user_data in essential_users:
            # Vérifier si l'utilisateur existe déjà
            if not User.objects.filter(username=user_data['username']).exists():
                # Créer l'utilisateur
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=admin_password,
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_staff=user_data['is_staff'],
                    is_superuser=user_data['is_superuser'],
                    is_active=True,
                    date_joined=timezone.now()
                )
                
                # Créer le profil avec le bon rôle
                role = Role.objects.get(name=user_data['role'])
                UserProfile.objects.create(
                    user=user,
                    role=role,
                    date_creation=timezone.now()
                )
                
                created_users.append(user_data)
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✅ Compte créé: {user_data["username"]} ({user_data["role"]})'
                    )
                )
                logger.info(f"Compte créé en production: {user_data['username']} avec rôle {user_data['role']}")
            else:
                existing_users.append(user_data)
                self.stdout.write(
                    self.style.WARNING(
                        f'  ⚠️ Compte existant: {user_data["username"]}'
                    )
                )
        
        # Afficher le résumé
        if created_users:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n📊 Comptes créés ({len(created_users)}):\n' +
                    '\n'.join([
                        f'   - {user["username"]} ({user["email"]}) - Rôle: {user["role"]}'
                        for user in created_users
                    ]) +
                    f'\n   - Mot de passe pour tous: {admin_password}'
                )
            )
        
        if existing_users:
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠️ Comptes existants ignorés ({len(existing_users)}): ' +
                    ', '.join([user['username'] for user in existing_users])
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Seeding production terminé !\n'
                'Les données essentielles ont été créées.'
            )
        )
