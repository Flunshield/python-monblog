from django.core.management.base import BaseCommand
from blog.models import Article, Category
from django.utils import timezone
import random
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer des articles de test pour l\'application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Nombre d\'articles à créer (défaut: 20)'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS(f'🚀 Début du seeding de {count} articles...'))
        
        # Récupérer les catégories existantes
        categories = list(Category.objects.all())
        if not categories:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Aucune catégorie trouvée. Exécutez d\'abord: python manage.py seed_categories'
                )
            )
            return
        
        auteurs = [
            'Jean Dupont', 'Marie Martin', 'Pierre Durand', 'Sophie Lemoine',
            'Thomas Bernard', 'Julie Moreau', 'Alexandre Petit', 'Camille Roux',
            'Nicolas Fournier', 'Isabelle Mercier', 'Julien Blanc', 'Nathalie Andre'
        ]
        
        articles_templates = [
            {
                'titre_template': 'Les dernières innovations en {}',
                'contenu_template': '''
                Dans un monde en constante évolution, le domaine de {} continue de nous surprendre avec des avancées remarquables.
                
                Les experts s'accordent à dire que les développements récents dans ce secteur ouvrent de nouvelles perspectives passionnantes. Cette évolution représente un tournant majeur qui pourrait transformer notre façon de voir et d'appréhender {}.
                
                ## Points clés à retenir
                
                - Innovation constante dans le secteur
                - Impact positif sur la société
                - Nouvelles opportunités d'emploi
                - Développement durable au cœur des préoccupations
                
                Les professionnels du secteur anticipent des changements encore plus significatifs dans les mois à venir. Cette dynamique positive s'inscrit dans une démarche globale d'amélioration continue.
                
                ## Perspectives d'avenir
                
                L'avenir s'annonce prometteur avec des projets ambitieux en cours de développement. Les investissements dans la recherche et développement témoignent de l'engagement fort des acteurs du marché.
                
                Cette tendance devrait se poursuivre et s'amplifier, créant un écosystème favorable à l'innovation et à la créativité.
                '''
            },
            {
                'titre_template': 'Analyse approfondie : l\'impact de {} sur notre quotidien',
                'contenu_template': '''
                L'influence croissante de {} dans notre vie quotidienne mérite une attention particulière. Cette analyse détaillée explore les multiples facettes de cette évolution.
                
                ## Contexte et enjeux
                
                Depuis plusieurs années, {} occupe une place de plus en plus importante dans nos habitudes. Cette transformation progressive s'accompagne de questionnements légitimes sur ses implications à long terme.
                
                Les données récentes montrent une adoption massive qui dépasse toutes les prévisions initiales. Cette croissance exponentielle soulève des défis inédits mais aussi des opportunités exceptionnelles.
                
                ## Impacts observés
                
                Les effets de cette évolution se manifestent dans plusieurs domaines :
                
                - Modification des comportements sociaux
                - Transformation des méthodes de travail
                - Évolution des relations interpersonnelles
                - Nouvelle approche de la consommation
                
                ## Recommandations
                
                Pour tirer le meilleur parti de cette révolution, il convient d'adopter une approche équilibrée qui préserve les aspects positifs tout en minimisant les risques potentiels.
                
                La clé du succès réside dans une adaptation progressive et réfléchie aux nouveaux paradigmes imposés par {}.
                '''
            },
            {
                'titre_template': 'Guide complet : tout savoir sur {}',
                'contenu_template': '''
                Ce guide exhaustif vous propose de découvrir tous les aspects essentiels de {}. Des bases fondamentales aux applications avancées, explorez un univers riche en possibilités.
                
                ## Introduction
                
                Comprendre {} nécessite une approche méthodique et structurée. Ce domaine complexe recèle de nombreuses subtilités qu'il convient d'appréhender progressivement.
                
                ## Les fondamentaux
                
                Avant d'explorer les aspects avancés, il est crucial de maîtriser les concepts de base. Ces éléments constituent le socle sur lequel repose toute expertise dans ce domaine.
                
                ### Principes de base
                - Définitions et terminologie
                - Concepts fondamentaux
                - Méthodes d'application
                - Bonnes pratiques
                
                ## Applications pratiques
                
                La théorie prend tout son sens lorsqu'elle est mise en pratique. Voici quelques exemples concrets d'utilisation de {} dans des contextes variés.
                
                Ces applications démontrent la polyvalence et l'adaptabilité de cette approche à différents environnements et contraintes.
                
                ## Conseils d'experts
                
                Les professionnels expérimentés recommandent une approche progressive pour acquérir une maîtrise solide de {}. La patience et la persévérance sont des qualités indispensables dans cet apprentissage.
                
                ## Conclusion
                
                Maîtriser {} représente un atout considérable dans le contexte actuel. Les investissements en formation et en expérimentation pratique sont rapidement rentabilisés.
                '''
            }
        ]
        
        created_count = 0
        
        for i in range(count):
            category = random.choice(categories)
            auteur = random.choice(auteurs)
            template = random.choice(articles_templates)
            
            # Adapter le contenu à la catégorie
            category_topic = category.nom.lower()
            titre = template['titre_template'].format(category_topic)
            contenu = template['contenu_template'].format(category_topic, category_topic, category_topic)
            
            # Créer une date aléatoire dans les 60 derniers jours
            days_ago = random.randint(0, 60)
            date_creation = timezone.now() - timezone.timedelta(days=days_ago)
            
            article = Article.objects.create(
                titre=titre,
                contenu=contenu,
                auteur=auteur,
                category=category,
                date_creation=date_creation
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'✅ Article créé: "{article.titre[:50]}..." par {auteur}')
            )
            logger.info(f"Article créé lors du seeding: {article.titre} par {auteur}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Résumé du seeding des articles:\n'
                f'   - Articles créés: {created_count}\n'
                f'   - Catégories utilisées: {len(categories)}\n'
                f'   - Auteurs différents: {len(auteurs)}'
            )
        )
