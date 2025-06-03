from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import ArticleForm, CommentForm, CategoryForm
from .models import Article, Category, UserProfile


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


@login_required
def ajouter_categorie(request):
    # Vérifier que l'utilisateur est administrateur
    try:
        profile = request.user.profile
        if profile.role != 'admin':
            return HttpResponseForbidden("Accès interdit : seuls les administrateurs peuvent gérer les catégories.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les administrateurs peuvent gérer les catégories.")
    
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


@login_required
def gerer_categories(request):
    """Vue pour afficher la liste des catégories avec options de gestion"""
    # Vérifier que l'utilisateur est journaliste ou administrateur
    try:
        profile = request.user.profile
        if profile.role not in ['journaliste', 'admin']:
            return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent consulter les catégories.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent consulter les catégories.")
    
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'user_role': profile.role,  # Passer le rôle pour contrôler l'affichage des boutons
    }
    return render(request, 'blog/gerer_categories.html', context)


@login_required
def modifier_categorie(request, category_id):
    """Vue pour modifier une catégorie existante"""
    # Vérifier que l'utilisateur est administrateur
    try:
        profile = request.user.profile
        if profile.role != 'admin':
            return HttpResponseForbidden("Accès interdit : seuls les administrateurs peuvent modifier les catégories.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les administrateurs peuvent modifier les catégories.")
    
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


@login_required
def supprimer_categorie(request, category_id):
    """Vue pour supprimer une catégorie"""
    # Vérifier que l'utilisateur est administrateur
    try:
        profile = request.user.profile
        if profile.role != 'admin':
            return HttpResponseForbidden("Accès interdit : seuls les administrateurs peuvent supprimer les catégories.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les administrateurs peuvent supprimer les catégories.")
    
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

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('Registration successful!'))
            return redirect('home')
    else:
        form = UserCreationForm()    # Ajoute les langues dans le contexte
    languages = []  # Simplifié pour éviter l'erreur d'import

    return render(request, 'blog/auth/register.html', {
        'form': form,
        'languages': languages,  # Ajoute ça
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _(f'Welcome, {username}! You are now logged in.'))
                return redirect('home')
            else:
                messages.error(request, _('Invalid username or password.'))
        else:
            messages.error(request, _('Invalid username or password.'))
    else:
        form = AuthenticationForm()
    return render(request, 'blog/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, _('You have been logged out.'))
    return render(request, 'blog/auth/logout.html')


@login_required
def set_role(request):
    """Vue pour changer le rôle de l'utilisateur connecté"""
    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['lecteur', 'journaliste', 'admin']:
            # Créer ou récupérer le profil utilisateur
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.role = role
            profile.save()
            messages.success(request, _(f'Votre rôle a été changé pour {role}'))
    return redirect(request.META.get('HTTP_REFERER', '/'))


def page_admin(request):
    """Vue réservée aux administrateurs"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Vérifier le rôle de l'utilisateur
    try:
        profile = request.user.profile
        if profile.role != 'admin':
            return HttpResponseForbidden("Accès interdit : vous devez être administrateur pour accéder à cette page.")
    except UserProfile.DoesNotExist:
        # Créer un profil par défaut si il n'existe pas
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : vous devez être administrateur pour accéder à cette page.")
    
    return render(request, 'blog/admin/page_admin.html', {
        'title': 'Page Administrateur',
        'message': 'Bienvenue dans l\'espace administrateur !'
    })


def page_journaliste(request):
    """Vue réservée aux journalistes et admins"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        profile = request.user.profile
        if profile.role not in ['journaliste', 'admin']:
            return HttpResponseForbidden("Accès interdit : vous devez être journaliste ou administrateur pour accéder à cette page.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : vous devez être journaliste ou administrateur pour accéder à cette page.")
    
    return render(request, 'blog/admin/page_journaliste.html', {
        'title': 'Espace Journaliste',
        'message': 'Bienvenue dans l\'espace journaliste !'
    })
