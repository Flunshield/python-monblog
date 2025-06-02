from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ajouter/', views.ajouter_article, name='ajouter_article'),
    path('ajouter-categorie/', views.ajouter_categorie, name='ajouter_categorie'),
    path('gerer-categories/', views.gerer_categories, name='gerer_categories'),
    path('gerer-articles/', views.gerer_articles, name='gerer_articles'),
    path('modifier-categorie/<int:category_id>/', views.modifier_categorie, name='modifier_categorie'),
    path('supprimer-categorie/<int:category_id>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('modifier-article/<int:article_id>/', views.modifier_article, name='modifier_article'),
    path('supprimer-article/<int:article_id>/', views.supprimer_article, name='supprimer_article'),
]
