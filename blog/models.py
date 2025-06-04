from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging

# Configuration du logger pour les modèles
logger = logging.getLogger('blog.models')


class Category(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['nom']


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Image")
    date_creation = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            logger.info(f"Création d'un nouvel article: '{self.titre}' par {self.auteur}")
        else:
            logger.info(f"Modification de l'article ID {self.pk}: '{self.titre}'")
        
        try:
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"Article '{self.titre}' créé avec succès (ID: {self.pk})")
            else:
                logger.info(f"Article '{self.titre}' modifié avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de l'article '{self.titre}': {e}")
            raise

    def delete(self, *args, **kwargs):
        logger.warning(f"Suppression de l'article '{self.titre}' (ID: {self.pk})")
        try:
            super().delete(*args, **kwargs)
            logger.info(f"Article '{self.titre}' supprimé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'article '{self.titre}': {e}")
            raise

    def get_total_likes(self):
        """Retourne le nombre total de likes pour cet article"""
        return self.likes.count()

    def is_liked_by(self, user):
        """Vérifie si un utilisateur a liké cet article"""
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()
    
    def get_excerpt(self, max_length=150):
        """Retourne un extrait du contenu limité à max_length caractères"""
        if len(self.contenu) <= max_length:
            return self.contenu
        return self.contenu[:max_length].rsplit(' ', 1)[0] + '...'
    
    def get_reading_time(self):
        """Estime le temps de lecture en minutes (250 mots par minute)"""
        word_count = len(self.contenu.split())
        reading_time = max(1, round(word_count / 250))
        return reading_time

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ['-date_creation']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commentaire de {self.nom} sur {self.article.titre}'

    class Meta:
        ordering = ['date_creation']


class Like(models.Model):
    """
    Modèle pour gérer les likes/bookmarks des articles.
    Un utilisateur ne peut liker un article qu'une seule fois.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'article')  # Un utilisateur ne peut liker qu'une fois le même article
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} likes {self.article.titre}'


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('lecteur', 'Lecteur'),
        ('journaliste', 'Journaliste'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='lecteur')
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Profil de {self.user.username} - {self.get_role_display()}'

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"


# Signaux pour créer automatiquement un profil utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)
