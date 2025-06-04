from django.core.management.base import BaseCommand
from blog.models import Article, Comment
from django.utils import timezone
import random
import logging

logger = logging.getLogger('blog')

class Command(BaseCommand):
    help = 'Créer des commentaires de test pour les articles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Nombre de commentaires à créer (défaut: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS(f'🚀 Début du seeding de {count} commentaires...'))
        
        # Récupérer les articles existants
        articles = list(Article.objects.all())
        if not articles:
            self.stdout.write(
                self.style.ERROR(
                    '❌ Aucun article trouvé. Exécutez d\'abord: python manage.py seed_articles'
                )
            )
            return
        
        commentateurs = [
            {'nom': 'Alice Dubois', 'email': 'alice.dubois@email.com'},
            {'nom': 'Bob Martin', 'email': 'bob.martin@email.com'},
            {'nom': 'Claire Rousseau', 'email': 'claire.rousseau@email.com'},
            {'nom': 'David Leroy', 'email': 'david.leroy@email.com'},
            {'nom': 'Emma Girard', 'email': 'emma.girard@email.com'},
            {'nom': 'François Meyer', 'email': 'francois.meyer@email.com'},
            {'nom': 'Gabrielle Simon', 'email': 'gabrielle.simon@email.com'},
            {'nom': 'Henri Faure', 'email': 'henri.faure@email.com'},
            {'nom': 'Isabelle Roy', 'email': 'isabelle.roy@email.com'},
            {'nom': 'Julien Morel', 'email': 'julien.morel@email.com'},
        ]
        
        commentaires_positifs = [
            "Excellent article ! Très instructif et bien écrit.",
            "Merci pour ce partage, j'ai appris beaucoup de choses.",
            "Analyse très pertinente, bravo pour ce travail de qualité.",
            "Article très intéressant, j'attends la suite avec impatience.",
            "Parfait ! Exactement ce que je cherchais comme information.",
            "Très bon point de vue, merci pour cet éclairage.",
            "Article de qualité, bien documenté et accessible.",
            "Formidable ! Cette lecture était très enrichissante.",
            "Merci pour ce contenu de qualité, très utile.",
            "Excellente synthèse, félicitations à l'auteur."
        ]
        
        commentaires_neutres = [
            "Intéressant, même si j'aurais aimé plus de détails sur certains points.",
            "Bon article dans l'ensemble, quelques aspects mériteraient d'être approfondis.",
            "Point de vue intéressant, il y aurait d'autres angles à explorer.",
            "Article correct, mais j'ai trouvé des informations similaires ailleurs.",
            "Pas mal, même si certains exemples auraient pu être plus concrets.",
            "Lecture instructive, malgré quelques longueurs.",
            "Contenu solide, qui gagnerait à être un peu plus synthétique.",
            "Bonne base de réflexion, à compléter avec d'autres sources.",
            "Article informatif, qui pose les bonnes questions.",
            "Approche intéressante, même si perfectible sur certains aspects."
        ]
        
        commentaires_questions = [
            "Très intéressant ! Auriez-vous des sources pour aller plus loin ?",
            "Merci pour cet article. Où peut-on trouver plus d'informations sur ce sujet ?",
            "Article passionnant ! Y a-t-il des études récentes sur cette question ?",
            "Excellent travail ! Prévoyez-vous un article de suivi ?",
            "Très informatif ! Existe-t-il des applications pratiques de ces concepts ?",
            "Merci pour ce partage ! Connaissez-vous d'autres experts sur ce sujet ?",
            "Article captivant ! Y a-t-il des formations disponibles dans ce domaine ?",
            "Très utile ! Avez-vous des recommandations de lecture complémentaire ?",
            "Fascinant ! Quelles sont les prochaines étapes de recherche ?",
            "Merci ! Pourriez-vous nous en dire plus sur les implications pratiques ?"
        ]
        
        created_count = 0
        
        for i in range(count):
            article = random.choice(articles)
            commentateur = random.choice(commentateurs)
            
            # Choisir un type de commentaire
            comment_type = random.choice(['positif', 'neutre', 'question'])
            if comment_type == 'positif':
                contenu = random.choice(commentaires_positifs)
            elif comment_type == 'neutre':
                contenu = random.choice(commentaires_neutres)
            else:
                contenu = random.choice(commentaires_questions)
            
            # Créer une date aléatoire après la création de l'article
            days_after_article = random.randint(0, 30)
            date_creation = article.date_creation + timezone.timedelta(days=days_after_article)
            
            # Si la date est dans le futur, la ramener à maintenant
            if date_creation > timezone.now():
                date_creation = timezone.now() - timezone.timedelta(hours=random.randint(1, 48))
            
            # Probabilité d'approbation (80% approuvés)
            is_approved = random.random() < 0.8
            
            comment = Comment.objects.create(
                article=article,
                nom=commentateur['nom'],
                email=commentateur['email'],
                contenu=contenu,
                date_creation=date_creation,
                is_approved=is_approved
            )
            
            created_count += 1
            approval_status = "✅ approuvé" if is_approved else "⏳ en attente"
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Commentaire créé: {commentateur["nom"]} sur "{article.titre[:30]}..." ({approval_status})'
                )
            )
            logger.info(f"Commentaire créé lors du seeding: {commentateur['nom']} sur {article.titre}")
        
        # Créer quelques réponses aux commentaires
        comments_with_replies = random.sample(
            list(Comment.objects.filter(parent=None)), 
            min(5, Comment.objects.filter(parent=None).count())
        )
        
        replies_count = 0
        for parent_comment in comments_with_replies:
            # 1-2 réponses par commentaire sélectionné
            num_replies = random.randint(1, 2)
            for _ in range(num_replies):
                commentateur = random.choice(commentateurs)
                contenu = random.choice([
                    f"@{parent_comment.nom} Merci pour votre commentaire, très pertinent !",
                    f"@{parent_comment.nom} Je partage votre point de vue.",
                    f"@{parent_comment.nom} Intéressant, je n'avais pas pensé à cet aspect.",
                    f"@{parent_comment.nom} Exactement ! Vous avez résumé ma pensée.",
                    f"@{parent_comment.nom} Merci pour cet éclairage supplémentaire."
                ])
                
                date_creation = parent_comment.date_creation + timezone.timedelta(
                    hours=random.randint(1, 72)
                )
                if date_creation > timezone.now():
                    date_creation = timezone.now() - timezone.timedelta(minutes=random.randint(30, 120))
                
                Comment.objects.create(
                    article=parent_comment.article,
                    nom=commentateur['nom'],
                    email=commentateur['email'],
                    contenu=contenu,
                    date_creation=date_creation,
                    is_approved=True,
                    parent=parent_comment
                )
                replies_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Résumé du seeding des commentaires:\n'
                f'   - Commentaires créés: {created_count}\n'
                f'   - Réponses créées: {replies_count}\n'
                f'   - Articles commentés: {len(set(Comment.objects.values_list("article_id", flat=True)))}\n'
                f'   - Commentateurs différents: {len(commentateurs)}'
            )
        )
