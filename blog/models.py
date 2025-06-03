from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


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
