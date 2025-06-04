from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Exécuter tous les seeders dans l\'ordre correct'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users-password',
            type=str,
            default='TestPass123!',
            help='Mot de passe pour les utilisateurs de test (défaut: TestPass123!)'
        )
        parser.add_argument(
            '--articles-count',
            type=int,
            default=20,
            help='Nombre d\'articles à créer (défaut: 20)'
        )
        parser.add_argument(
            '--comments-count',
            type=int,
            default=50,
            help='Nombre de commentaires à créer (défaut: 50)'
        )
        parser.add_argument(
            '--likes-count',
            type=int,
            default=100,
            help='Nombre de likes à créer (défaut: 100)'
        )
        parser.add_argument(
            '--skip-users',
            action='store_true',
            help='Ignorer la création d\'utilisateurs de test'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                '🎉 Début du seeding complet de la base de données !\n'
                '=' * 60
            )
        )
        
        try:
            # 1. Seeder les rôles
            self.stdout.write(self.style.HTTP_INFO('\n📋 Étape 1/6: Création des rôles'))
            call_command('seed_roles')
            
            # 2. Seeder les catégories
            self.stdout.write(self.style.HTTP_INFO('\n📂 Étape 2/6: Création des catégories'))
            call_command('seed_categories')
            
            # 3. Seeder les utilisateurs (optionnel)
            if not options['skip_users']:
                self.stdout.write(self.style.HTTP_INFO('\n👥 Étape 3/6: Création des utilisateurs'))
                call_command('seed_users', password=options['users_password'])
            else:
                self.stdout.write(self.style.WARNING('\n⏭️  Étape 3/6: Utilisateurs ignorés'))
            
            # 4. Seeder les articles
            self.stdout.write(self.style.HTTP_INFO('\n📝 Étape 4/6: Création des articles'))
            call_command('seed_articles', count=options['articles_count'])
            
            # 5. Seeder les commentaires
            self.stdout.write(self.style.HTTP_INFO('\n💬 Étape 5/6: Création des commentaires'))
            call_command('seed_comments', count=options['comments_count'])
            
            # 6. Seeder les likes
            self.stdout.write(self.style.HTTP_INFO('\n❤️  Étape 6/6: Création des likes'))
            call_command('seed_likes', count=options['likes_count'])
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n' + '=' * 60 + '\n'
                    '🎊 SEEDING TERMINÉ AVEC SUCCÈS ! 🎊\n'
                    '=' * 60 + '\n'
                    'Votre base de données est maintenant remplie avec des données de test.\n'
                    '\n📊 Récapitulatif:'
                )
            )
            
            # Afficher un résumé
            from blog.models import Role, Category, Article, Comment, Like
            from django.contrib.auth.models import User
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'   - Rôles: {Role.objects.count()}\n'
                    f'   - Catégories: {Category.objects.count()}\n'
                    f'   - Utilisateurs: {User.objects.count()}\n'
                    f'   - Articles: {Article.objects.count()}\n'
                    f'   - Commentaires: {Comment.objects.count()}\n'
                    f'   - Likes: {Like.objects.count()}\n'
                )
            )
            
            if not options['skip_users']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n🔑 Connexions de test:\n'
                        f'   - Admin: admin_test / {options["users_password"]}\n'
                        f'   - Journaliste: journaliste_test / {options["users_password"]}\n'
                        f'   - Lecteur: lecteur_test / {options["users_password"]}\n'
                    )
                )
            
            logger.info("Seeding complet terminé avec succès")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Erreur lors du seeding: {str(e)}')
            )
            logger.error(f"Erreur lors du seeding complet: {str(e)}")
            raise
