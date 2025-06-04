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
        
        # 3. Créer un compte admin si aucun superuser n'existe
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write('👑 Création du compte administrateur...')
            
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@monprojet.com',
                password=admin_password,
                first_name='Admin',
                last_name='Principal',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                date_joined=timezone.now()
            )
            
            # Créer le profil avec le rôle admin
            from blog.models import UserProfile
            admin_role = Role.objects.get(name='admin')
            UserProfile.objects.create(
                user=admin_user,
                role=admin_role,
                date_creation=timezone.now()
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'  ✅ Compte admin créé:\n'
                    f'     - Username: admin\n'
                    f'     - Email: admin@monprojet.com\n'
                    f'     - Password: {admin_password}'
                )
            )
            logger.info(f"Compte admin créé en production: admin")
        else:
            self.stdout.write('  ⚠️ Un superuser existe déjà')
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 Seeding production terminé !\n'
                'Les données essentielles ont été créées.'
            )
        )
