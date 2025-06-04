from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Role, Category, Article, Comment, Like, UserProfile
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Nettoyer toutes les données de test créées par les seeders'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirmer la suppression (requis pour éviter les suppressions accidentelles)'
        )
        parser.add_argument(
            '--keep-users',
            action='store_true',
            help='Conserver les utilisateurs (supprimer seulement le contenu)'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.ERROR(
                    '⚠️  ATTENTION: Cette commande va supprimer toutes les données de test !\n'
                    'Pour confirmer, utilisez: python manage.py clear_seed_data --confirm'
                )
            )
            return
        
        self.stdout.write(
            self.style.WARNING(
                '🧹 Début du nettoyage des données de test...\n'
                '⚠️  Cette action est irréversible !'
            )
        )
        
        # Compter avant suppression
        initial_counts = {
            'users': User.objects.count(),
            'articles': Article.objects.count(),
            'comments': Comment.objects.count(),
            'likes': Like.objects.count(),
            'categories': Category.objects.count(),
            'roles': Role.objects.count(),
        }
        
        try:
            # 1. Supprimer les likes
            likes_deleted = Like.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ Likes supprimés: {likes_deleted}'))
            
            # 2. Supprimer les commentaires
            comments_deleted = Comment.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ Commentaires supprimés: {comments_deleted}'))
            
            # 3. Supprimer les articles
            articles_deleted = Article.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ Articles supprimés: {articles_deleted}'))
            
            # 4. Supprimer les catégories
            categories_deleted = Category.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ Catégories supprimées: {categories_deleted}'))
            
            # 5. Supprimer les utilisateurs de test (optionnel)
            if not options['keep_users']:
                # Supprimer les profils utilisateurs en premier
                profiles_deleted = UserProfile.objects.all().delete()[0]
                self.stdout.write(self.style.SUCCESS(f'✅ Profils utilisateurs supprimés: {profiles_deleted}'))
                
                # Supprimer tous les utilisateurs sauf les superusers existants
                test_users = User.objects.filter(username__endswith='_test')
                users_deleted = test_users.delete()[0]
                self.stdout.write(self.style.SUCCESS(f'✅ Utilisateurs de test supprimés: {users_deleted}'))
            else:
                self.stdout.write(self.style.WARNING('⏭️  Utilisateurs conservés'))
            
            # 6. Supprimer les rôles
            roles_deleted = Role.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ Rôles supprimés: {roles_deleted}'))
            
            # Afficher le résumé
            final_counts = {
                'users': User.objects.count(),
                'articles': Article.objects.count(),
                'comments': Comment.objects.count(),
                'likes': Like.objects.count(),
                'categories': Category.objects.count(),
                'roles': Role.objects.count(),
            }
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n📊 Résumé du nettoyage:\n'
                    f'   - Utilisateurs: {initial_counts["users"]} → {final_counts["users"]}\n'
                    f'   - Articles: {initial_counts["articles"]} → {final_counts["articles"]}\n'
                    f'   - Commentaires: {initial_counts["comments"]} → {final_counts["comments"]}\n'
                    f'   - Likes: {initial_counts["likes"]} → {final_counts["likes"]}\n'
                    f'   - Catégories: {initial_counts["categories"]} → {final_counts["categories"]}\n'
                    f'   - Rôles: {initial_counts["roles"]} → {final_counts["roles"]}\n'
                )
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n🎉 Nettoyage terminé avec succès !\n'
                    'La base de données a été nettoyée.'
                )
            )
            
            logger.info("Nettoyage des données de test terminé avec succès")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Erreur lors du nettoyage: {str(e)}')
            )
            logger.error(f"Erreur lors du nettoyage: {str(e)}")
            raise
