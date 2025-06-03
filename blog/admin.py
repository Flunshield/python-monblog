from django.contrib import admin
from .models import Article, Comment, Category, UserProfile, Like


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


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at', 'article__category')
    search_fields = ('user__username', 'article__titre')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'article')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'date_creation')
    list_filter = ('role', 'date_creation')
    search_fields = ('user__username', 'user__email')
    ordering = ('-date_creation',)
    readonly_fields = ('date_creation',)
