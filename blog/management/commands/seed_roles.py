from django.core.management.base import BaseCommand
from blog.models import Role
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer les rôles de base pour l\'application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Début du seeding des rôles...'))
        
        roles_data = [
            {'name': 'lecteur'},
            {'name': 'journaliste'},
            {'name': 'admin'},
            {'name': 'modérateur'},
            {'name': 'éditeur'},
        ]
        
        created_count = 0
        existing_count = 0
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                name=role_data['name']
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Rôle créé: {role.name}')
                )
                logger.info(f"Rôle créé lors du seeding: {role.name}")
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Rôle existant: {role.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Résumé du seeding des rôles:\n'
                f'   - Rôles créés: {created_count}\n'
                f'   - Rôles existants: {existing_count}\n'
                f'   - Total: {created_count + existing_count}'
            )
        )
