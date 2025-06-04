from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging

# Configuration du logger pour les modèles
logger = logging.getLogger('blog.models')


class Role(models.Model):
    """
    Modèle pour gérer les rôles des utilisateurs de manière dynamique
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"
        ordering = ['name']

    @classmethod
    def get_default_roles(cls):
        """Créer et retourner les rôles par défaut"""
        lecteur_role, _ = cls.objects.get_or_create(name='lecteur')
        journaliste_role, _ = cls.objects.get_or_create(name='journaliste') 
        admin_role, _ = cls.objects.get_or_create(name='admin')
        return {
            'lecteur': lecteur_role,
            'journaliste': journaliste_role,
            'admin': admin_role
        }


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
    is_approved = models.BooleanField(default=False, verbose_name="Approuvé")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name="Commentaire parent")
    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé")

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=False, blank=False)
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Profil de {self.user.username} - {self.role.name}'

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"

    def save(self, *args, **kwargs):
        # Si aucun rôle n'est défini, attribuer le rôle "lecteur" par défaut
        if not self.role_id:
            default_roles = Role.get_default_roles()
            self.role = default_roles['lecteur']
        super().save(*args, **kwargs)


# Signaux pour créer automatiquement un profil utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Assurer que les rôles par défaut existent
        default_roles = Role.get_default_roles()
        UserProfile.objects.create(user=instance, role=default_roles['lecteur'])


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Assurer que les rôles par défaut existent
        default_roles = Role.get_default_roles()
        UserProfile.objects.create(user=instance, role=default_roles['lecteur'])
