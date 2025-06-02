from django.db import models
from django.utils import timezone


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
