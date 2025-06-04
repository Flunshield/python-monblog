from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Article, Like
from django.utils import timezone
import random
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer des likes de test pour les articles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Nombre de likes à créer (défaut: 100)'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS(f'🚀 Début du seeding de {count} likes...'))
        
        # Récupérer les utilisateurs et articles existants
        users = list(User.objects.all())
        articles = list(Article.objects.all())
        
        if not users:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Aucun utilisateur trouvé. Exécutez d\'abord: python manage.py seed_users'
                )
            )
            return
            
        if not articles:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Aucun article trouvé. Exécutez d\'abord: python manage.py seed_articles'
                )
            )
            return
        
        created_count = 0
        skipped_count = 0
        
        # Créer des likes aléatoirement
        for i in range(count):
            user = random.choice(users)
            article = random.choice(articles)
            
            # Vérifier si ce like existe déjà (contrainte unique)
            if Like.objects.filter(user=user, article=article).exists():
                skipped_count += 1
                continue
            
            # Créer une date aléatoire après la création de l'article
            days_after_article = random.randint(0, 30)
            created_at = article.date_creation + timezone.timedelta(
                days=days_after_article,
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Si la date est dans le futur, la ramener à maintenant
            if created_at > timezone.now():
                created_at = timezone.now() - timezone.timedelta(
                    hours=random.randint(1, 48)
                )
            
            like = Like.objects.create(
                user=user,
                article=article,
                created_at=created_at
            )
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'❤️  Like créé: {user.username} a liké "{article.titre[:30]}..."'
                )
            )
            logger.info(f"Like créé lors du seeding: {user.username} -> {article.titre}")
        
        # Statistiques par article
        articles_with_likes = Article.objects.filter(likes__isnull=False).distinct()
        most_liked_article = articles_with_likes.order_by('-likes__count').first() if articles_with_likes else None
        
        # Statistiques par utilisateur
        users_with_likes = User.objects.filter(likes__isnull=False).distinct()
        most_active_user = users_with_likes.order_by('-likes__count').first() if users_with_likes else None
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Résumé du seeding des likes:\n'
                f'   - Likes créés: {created_count}\n'
                f'   - Likes ignorés (doublons): {skipped_count}\n'
                f'   - Articles avec likes: {articles_with_likes.count()}\n'
                f'   - Utilisateurs actifs: {users_with_likes.count()}'
            )
        )
        
        if most_liked_article:
            likes_count = most_liked_article.get_total_likes()
            self.stdout.write(
                self.style.SUCCESS(
                    f'   - Article le plus aimé: "{most_liked_article.titre[:40]}..." ({likes_count} likes)'
                )
            )
            
        if most_active_user:
            user_likes_count = most_active_user.likes.count()
            self.stdout.write(
                self.style.SUCCESS(
                    f'   - Utilisateur le plus actif: {most_active_user.username} ({user_likes_count} likes)'
                )
            )
