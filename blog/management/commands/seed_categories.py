from django.core.management.base import BaseCommand
from blog.models import Category
from django.utils import timezone
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer des catégories d\'articles pour l\'application'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Début du seeding des catégories...'))
        
        categories_data = [
            {
                'nom': 'Actualités',
                'description': 'Les dernières nouvelles et événements d\'actualité'
            },
            {
                'nom': 'Technologie',
                'description': 'Articles sur les nouvelles technologies, l\'innovation et le numérique'
            },
            {
                'nom': 'Sport',
                'description': 'Actualités sportives, résultats et analyses'
            },
            {
                'nom': 'Culture',
                'description': 'Arts, littérature, cinéma et événements culturels'
            },
            {
                'nom': 'Économie',
                'description': 'Analyses économiques, marchés financiers et entreprises'
            },
            {
                'nom': 'Santé',
                'description': 'Conseils santé, recherches médicales et bien-être'
            },
            {
                'nom': 'Environnement',
                'description': 'Écologie, développement durable et changement climatique'
            },
            {
                'nom': 'Politique',
                'description': 'Actualités politiques nationales et internationales'
            },
            {
                'nom': 'Sciences',
                'description': 'Découvertes scientifiques et recherches académiques'
            },
            {
                'nom': 'Voyage',
                'description': 'Destinations, conseils de voyage et découvertes culturelles'
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                nom=category_data['nom'],
                defaults={
                    'description': category_data['description'],
                    'date_creation': timezone.now()
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Catégorie créée: {category.nom}')
                )
                logger.info(f"Catégorie créée lors du seeding: {category.nom}")
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Catégorie existante: {category.nom}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Résumé du seeding des catégories:\n'
                f'   - Catégories créées: {created_count}\n'
                f'   - Catégories existantes: {existing_count}\n'
                f'   - Total: {created_count + existing_count}'
            )
        )
