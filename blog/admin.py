from django.contrib import admin
from .models import Article, Comment, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_creation')
    search_fields = ('nom',)
    ordering = ('nom',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'category', 'date_creation')
    list_filter = ('category', 'date_creation', 'auteur')
    search_fields = ('titre', 'contenu', 'auteur')
    ordering = ('-date_creation',)
    fields = ('titre', 'contenu', 'auteur', 'category', 'image')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'article', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('nom', 'contenu')
    ordering = ('-date_creation',)
