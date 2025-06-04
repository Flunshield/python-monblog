from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.tous_les_articles, name='tous_les_articles'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('ajouter-categorie/', views.ajouter_categorie, name='ajouter_categorie'),
    path('gerer-categories/', views.gerer_categories, name='gerer_categories'),
    path('gerer-articles/', views.gerer_articles, name='gerer_articles'),
    path('modifier-categorie/<int:category_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('supprimer-categorie/<int:category_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('modifier-article/<int:article_id>/', views.modifier_article, name='modifier_article'),
    path('supprimer-article/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
    path('supprimer-article/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),    path('logout/', views.logout_view, name='logout'),
    path('set-role/', views.set_role, name='set_role'),
    path('admin-page/', views.page_admin, name='page_admin'),
    path('journaliste-page/', views.page_journaliste, name='page_journaliste'),
    path('like/<int:article_id>/', views.toggle_like, name='toggle_like'),
    path('debug-like/', views.test_like_debug, name='debug_like'),
    path('diagnostic-images/', views.diagnostic_images, name='diagnostic_images'),  # Diagnostic Django complet
]
