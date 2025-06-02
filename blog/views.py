from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from .forms import ArticleForm, CommentForm, CategoryForm
from .models import Article, Category


def home(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    
    if category_filter:
        articles = articles.filter(category_id=category_filter)
    
    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': int(category_filter) if category_filter else None
    }
    return render(request, 'blog/home.html', context)


def ajouter_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _('Article ajouté avec succès!'))
            return redirect('home')
    else:
        form = ArticleForm()

    return render(request, 'blog/ajouter_article.html', {'form': form})


def ajouter_categorie(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Catégorie ajoutée avec succès!'))
            return redirect('home')
    else:
        form = CategoryForm()

    return render(request, 'blog/ajouter_categorie.html', {'form': form})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.save()
            messages.success(request, _('Commentaire ajouté avec succès!'))
            return redirect('article_detail', article_id=article.id)
    else:
        comment_form = CommentForm()

    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'blog/article_detail.html', context)


def gerer_categories(request):
    """Vue pour afficher la liste des catégories avec options de gestion"""
    # Translating the docstring for consistency, though not strictly displayed to user
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/gerer_categories.html', context)


def modifier_categorie(request, category_id):
    """Vue pour modifier une catégorie existante"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _(f'Catégorie "{category.nom}" modifiée avec succès!'))
            return redirect('gerer_categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'blog/modifier_categorie.html', context)


def supprimer_categorie(request, category_id):
    """Vue pour supprimer une catégorie"""
    # Translating the docstring for consistency
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category_name = category.nom
        category.delete()
        messages.success(request, _(f'Catégorie "{category_name}" supprimée avec succès!'))
        return redirect('gerer_categories')
    
    context = {
        'category': category,
    }
    return render(request, 'blog/supprimer_categorie.html', context)


def modifier_article(request, article_id):
    """Vue pour modifier un article existant"""
    # Translating the docstring for consistency
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, _(f'Article "{article.titre}" modifié avec succès!'))
            return redirect('article_detail', article_id=article.id)
    else:
        form = ArticleForm(instance=article)
    
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'blog/modifier_article.html', context)


def supprimer_article(request, article_id):
    """Vue pour supprimer un article"""
    # Translating the docstring for consistency
    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article_title = article.titre
        article.delete()
        messages.success(request, _(f'Article "{article_title}" supprimé avec succès!'))
        return redirect('home')
    
    context = {
        'article': article,
    }
    return render(request, 'blog/supprimer_article.html', context)


def gerer_articles(request):
    """Vue pour afficher la liste des articles avec options de gestion"""
    # Translating the docstring for consistency
    articles = Article.objects.all().order_by('-date_creation')
    categories = Category.objects.all()
    category_filter = request.GET.get('category')
    
    if category_filter:
        articles = articles.filter(category_id=category_filter)
    
    context = {
        'articles': articles,
        'categories': categories,
        'selected_category': int(category_filter) if category_filter else None
    }
    return render(request, 'blog/gerer_articles.html', context)

# Create your views here.
