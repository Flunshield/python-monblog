from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
from django.db.models import Q, Count, Case, When, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
import re
from .forms import ArticleForm, CommentForm, CategoryForm, SearchForm, CommentReplyForm
from .models import Article, Category, UserProfile, Like, Comment

# Configuration du logger pour ce module
logger = logging.getLogger('blog')


def home(request):
    """
    Page d'accueil optimisée avec articles récents et populaires
    """
    logger.info(f"Accès à la page d'accueil par l'utilisateur {request.user}")
    
    try:
        # Optimisation des requêtes avec select_related et prefetch_related
        base_queryset = Article.objects.select_related('category').prefetch_related('likes', 'comments')
        
        # Articles récents (limite à 10)
        articles_recents = base_queryset.order_by('-date_creation')[:10]
        
        # Articles populaires basés sur le nombre de likes (limite à 10)
        articles_populaires = base_queryset.annotate(
            total_likes=models.Count('likes')
        ).order_by('-total_likes', '-date_creation')[:10]
        
        # Catégories pour le filtre
        categories = Category.objects.all()
        
        # Filtrage par catégorie si demandé
        category_filter = request.GET.get('category')
        if category_filter:
            logger.debug(f"Filtrage par catégorie: {category_filter}")
            articles_recents = articles_recents.filter(category_id=category_filter)
            articles_populaires = articles_populaires.filter(category_id=category_filter)
        
        logger.debug(f"Articles récents: {len(articles_recents)}, Articles populaires: {len(articles_populaires)}")
        
        context = {
            'articles_recents': articles_recents,
            'articles_populaires': articles_populaires,
            'categories': categories,
            'selected_category': int(category_filter) if category_filter else None,
        }
        return render(request, 'blog/home.html', context)
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page d'accueil: {e}")
        messages.error(request, _('Une erreur est survenue lors du chargement de la page.'))
        return render(request, 'blog/home.html', {
            'articles_recents': [],
            'articles_populaires': [],
            'categories': []
        })


def tous_les_articles(request):
    """
    Vue pour afficher tous les articles avec pagination
    """
    logger.info(f"Accès à la liste complète des articles par l'utilisateur {request.user}")
    
    try:
        articles = Article.objects.select_related('category').prefetch_related('likes', 'comments')
        categories = Category.objects.all()
        category_filter = request.GET.get('category')
        
        if category_filter:
            logger.debug(f"Filtrage par catégorie: {category_filter}")
            articles = articles.filter(category_id=category_filter)
        
        logger.debug(f"Nombre d'articles trouvés: {articles.count()}")
        
        context = {
            'articles': articles,
            'categories': categories,
            'selected_category': int(category_filter) if category_filter else None,
            'page_title': _('Tous les articles')
        }
        return render(request, 'blog/tous_les_articles.html', context)
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la liste des articles: {e}")
        messages.error(request, _('Une erreur est survenue lors du chargement de la page.'))
        return render(request, 'blog/tous_les_articles.html', {'articles': [], 'categories': []})


def ajouter_article(request):
    logger.info(f"Tentative d'ajout d'article par l'utilisateur {request.user}")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                article = form.save()
                logger.info(f"Article '{article.titre}' créé avec succès par {request.user}")
                messages.success(request, _('Article ajouté avec succès!'))
                return redirect('home')
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde de l'article: {e}")
                messages.error(request, _('Erreur lors de la sauvegarde de l\'article.'))
        else:
            logger.warning(f"Formulaire d'article invalide pour l'utilisateur {request.user}: {form.errors}")
    else:
        # Pré-remplir le champ auteur avec l'username de l'utilisateur connecté
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['auteur'] = request.user.username
            logger.debug(f"Pré-remplissage du formulaire avec l'auteur: {request.user.username}")
        form = ArticleForm(initial=initial_data)

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
    
    # Afficher seulement les commentaires approuvés aux visiteurs
    # Les modérateurs peuvent voir tous les commentaires
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.role in ['journaliste', 'admin']:
                # Les journalistes voient tous les commentaires sur leurs articles
                # Les admins voient tous les commentaires
                if profile.role == 'admin' or article.auteur.lower() == request.user.username.lower():
                    comments = article.comments.all()
                else:
                    comments = article.comments.filter(is_approved=True)
            else:
                comments = article.comments.filter(is_approved=True)
        except UserProfile.DoesNotExist:
            comments = article.comments.filter(is_approved=True)
    else:
        comments = article.comments.filter(is_approved=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            # Les nouveaux commentaires nécessitent une approbation
            comment.is_approved = False
            comment.save()
            messages.success(request, _('Commentaire ajouté avec succès! Il sera visible après modération.'))
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


@login_required
def modifier_article(request, article_id):
    """Vue pour modifier un article existant"""
    # Vérifier que l'utilisateur est journaliste ou administrateur
    try:
        profile = request.user.profile
        if profile.role not in ['journaliste', 'admin']:
            return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent modifier les articles.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent modifier les articles.")
    
    article = get_object_or_404(Article, id=article_id)
    
    # Si l'utilisateur est journaliste, vérifier qu'il est l'auteur de l'article
    if profile.role == 'journaliste':
        if article.auteur.lower() != request.user.username.lower():
            return HttpResponseForbidden("Accès interdit : vous ne pouvez modifier que vos propres articles.")
    
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


@login_required
def supprimer_article(request, article_id):
    """Vue pour supprimer un article"""
    # Vérifier que l'utilisateur est journaliste ou administrateur
    try:
        profile = request.user.profile
        if profile.role not in ['journaliste', 'admin']:
            return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent supprimer les articles.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent supprimer les articles.")
    
    article = get_object_or_404(Article, id=article_id)
    
    # Si l'utilisateur est journaliste, vérifier qu'il est l'auteur de l'article
    if profile.role == 'journaliste':
        if article.auteur.lower() != request.user.username.lower():
            return HttpResponseForbidden("Accès interdit : vous ne pouvez supprimer que vos propres articles.")
    
    if request.method == 'POST':
        article_title = article.titre
        article.delete()
        messages.success(request, _(f'Article "{article_title}" supprimé avec succès!'))
        return redirect('home')
    
    context = {
        'article': article,
    }
    return render(request, 'blog/supprimer_article.html', context)


@login_required
def gerer_articles(request):
    """Vue pour afficher la liste des articles avec options de gestion"""
    # Vérifier que l'utilisateur est journaliste ou administrateur
    try:
        profile = request.user.profile
        if profile.role not in ['journaliste', 'admin']:
            return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent gérer les articles.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent gérer les articles.")
    
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
    
    # Calcul des statistiques pour le journaliste
    from django.utils import timezone
    from datetime import datetime, timedelta
    from .models import Comment
    
    # Articles de l'utilisateur actuel (si journaliste) ou tous les articles (si admin)
    if profile.role == 'journaliste':
        # Pour un journaliste, on cherche les articles qui correspondent à son nom d'utilisateur 
        # ou aux variations possibles de son nom
        user_articles = Article.objects.filter(
            auteur__icontains=request.user.username
        ) or Article.objects.filter(
            auteur__icontains=request.user.first_name
        ) or Article.objects.filter(
            auteur__icontains=request.user.last_name
        )
        # Si aucun article trouvé avec ces critères, utiliser le nom d'utilisateur exact
        if not user_articles.exists():
            user_articles = Article.objects.filter(auteur=request.user.username)
    else:
        # Pour un admin, afficher tous les articles
        user_articles = Article.objects.all()
    
    # Articles créés ce mois-ci
    current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    recent_articles = user_articles.filter(date_creation__gte=current_month)
    
    # Commentaires reçus sur les articles de l'utilisateur
    user_comments = Comment.objects.filter(article__in=user_articles)
    
    context = {
        'title': 'Espace Journaliste',
        'message': 'Bienvenue dans l\'espace journaliste !',
        'user_articles': user_articles.count(),
        'recent_articles': recent_articles.count(),
        'user_comments': user_comments.count(),
        'user_role': profile.role,
    }
    
    return render(request, 'blog/admin/page_journaliste.html', context)


def diagnostic_images(request):
    """Vue Django complète pour le diagnostic des images - Remplace le JavaScript"""
    logger.info(f"Diagnostic des images demandé par l'utilisateur {request.user}")
    
    import os
    from urllib.parse import unquote
    import mimetypes
    
    # Récupération des articles avec images
    articles = Article.objects.exclude(image='')
    
    # Informations système
    system_info = {
        'total_articles': Article.objects.count(),
        'articles_with_images': articles.count(),
        'media_root': settings.MEDIA_ROOT,
        'media_url': settings.MEDIA_URL,
        'debug_mode': settings.DEBUG,
    }
    
    # Test de chaque image
    image_tests = []
    for article in articles:
        if article.image:
            # Chemin physique du fichier
            image_path = os.path.join(settings.MEDIA_ROOT, article.image.name)
            
            # Tests de validation
            test_result = {
                'article_title': article.titre,
                'image_name': article.image.name,
                'image_url': article.image.url,
                'image_path': image_path,
                'file_exists': os.path.exists(image_path),
                'file_size': 0,
                'file_size_human': '0 B',
                'mime_type': 'unknown',
                'is_readable': False,
                'url_encoded_correctly': False,
                'status': 'unknown'
            }
            
            # Vérification de l'existence du fichier
            if test_result['file_exists']:
                try:
                    # Taille du fichier
                    test_result['file_size'] = os.path.getsize(image_path)
                    test_result['file_size_human'] = format_file_size(test_result['file_size'])
                    
                    # Type MIME
                    mime_type, _ = mimetypes.guess_type(image_path)
                    test_result['mime_type'] = mime_type or 'unknown'
                    
                    # Test de lecture
                    test_result['is_readable'] = os.access(image_path, os.R_OK)
                    
                    # Test d'encodage URL
                    decoded_url = unquote(article.image.url)
                    test_result['url_encoded_correctly'] = decoded_url == article.image.url
                    
                    # Statut global
                    if test_result['is_readable'] and test_result['file_size'] > 0:
                        test_result['status'] = 'success'
                    else:
                        test_result['status'] = 'warning'
                        
                except Exception as e:
                    logger.error(f"Erreur lors du test de l'image {article.image.name}: {e}")
                    test_result['status'] = 'error'
                    test_result['error_message'] = str(e)
            else:
                test_result['status'] = 'error'
                test_result['error_message'] = 'Fichier non trouvé'
            
            image_tests.append(test_result)
    
    # Vérification du dossier media/articles
    articles_dir = os.path.join(settings.MEDIA_ROOT, 'articles')
    directory_info = {
        'path': articles_dir,
        'exists': os.path.exists(articles_dir),
        'is_writable': os.access(articles_dir, os.W_OK) if os.path.exists(articles_dir) else False,
        'files': []
    }
    
    if directory_info['exists']:
        try:
            files = os.listdir(articles_dir)
            for file in files:
                file_path = os.path.join(articles_dir, file)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    directory_info['files'].append({
                        'name': file,
                        'size': file_size,
                        'size_human': format_file_size(file_size),
                        'is_used': any(test['image_name'].endswith(file) for test in image_tests)
                    })
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du dossier media: {e}")
            directory_info['error'] = str(e)
    
    # Statistiques globales
    stats = {
        'total_tests': len(image_tests),
        'successful_tests': len([t for t in image_tests if t['status'] == 'success']),
        'warning_tests': len([t for t in image_tests if t['status'] == 'warning']),
        'error_tests': len([t for t in image_tests if t['status'] == 'error']),
    }
    
    context = {
        'system_info': system_info,
        'image_tests': image_tests,
        'directory_info': directory_info,
        'stats': stats,
        'debug_mode': settings.DEBUG,
    }
    
    logger.info(f"Diagnostic terminé: {stats['successful_tests']}/{stats['total_tests']} images OK")
    
    return render(request, 'blog/diagnostic_images.html', context)


def format_file_size(size_bytes):
    """Formate la taille de fichier en format humain"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


@login_required
@require_POST
def toggle_like(request, article_id):
    """
    Vue pour liker/unliker un article.
    Redirige vers la page d'origine avec un message de confirmation.
    """
    try:
        article = get_object_or_404(Article, id=article_id)
        like, created = Like.objects.get_or_create(
            user=request.user,
            article=article
        )
        
        if not created:
            # L'utilisateur avait déjà liké, on supprime le like
            like.delete()
            message = _("Like retiré")
            logger.info(f"Utilisateur {request.user.username} a retiré son like de l'article '{article.titre}'")
        else:
            # Nouveau like créé
            message = _("Article liké")
            logger.info(f"Utilisateur {request.user.username} a liké l'article '{article.titre}'")
        
        # Ajouter le message de succès
        messages.success(request, message)
        
        # Rediriger vers la page précédente ou vers l'article
        redirect_url = request.META.get('HTTP_REFERER')
        if redirect_url:
            return redirect(redirect_url)
        else:
            return redirect('article_detail', article_id=article.id)
        
    except Exception as e:
        logger.error(f"Erreur lors du toggle like pour l'article {article_id}: {e}")
        messages.error(request, _("Une erreur s'est produite lors du like"))
        # Rediriger vers la page précédente ou vers l'article en cas d'erreur
        redirect_url = request.META.get('HTTP_REFERER')
        if redirect_url:
            return redirect(redirect_url)
        else:
            return redirect('article_detail', article_id=article.id)


def test_like_debug(request):
    """Vue de debug pour tester la fonctionnalité Like"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Récupérer le premier article pour le test
    article = Article.objects.first()
    if not article:
        return HttpResponse("Aucun article trouvé. Créez d'abord un article.")
    
    context = {
        'article': article,
        'is_liked': article.is_liked_by(request.user),
        'total_likes': article.get_total_likes(),
    }
    
    return render(request, 'blog/debug_like.html', context)


@login_required
def profile_view(request):
    """
    Vue pour afficher le profil utilisateur avec ses statistiques
    """
    logger.info(f"Accès au profil par l'utilisateur {request.user}")
    
    try:
        user = request.user
        
        # Récupérer ou créer le profil utilisateur
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Statistiques des likes
        liked_articles = Article.objects.filter(
            likes__user=user
        ).select_related('category').order_by('-likes__created_at')[:10]
        
        # Nombre total d'articles likés
        total_liked_articles = user.likes.count()
        
        # Commentaires postés par l'utilisateur
        user_comments = Comment.objects.filter(
            email=user.email
        ).select_related('article').order_by('-date_creation')[:10]
        total_comments = Comment.objects.filter(email=user.email).count()
        
        # Articles récemment likés (5 derniers)
        recent_liked_articles = Article.objects.filter(
            likes__user=user
        ).select_related('category').order_by('-likes__created_at')[:5]
        
        # Statistiques générales
        total_articles_platform = Article.objects.count()
        total_categories = Category.objects.count()
        
        logger.debug(f"Profil chargé pour {user.username}: {total_liked_articles} likes, {total_comments} commentaires")
        
        context = {
            'user_profile': profile,
            'liked_articles': liked_articles,
            'total_liked_articles': total_liked_articles,
            'user_comments': user_comments,
            'total_comments': total_comments,
            'recent_liked_articles': recent_liked_articles,
            'total_articles_platform': total_articles_platform,
            'total_categories': total_categories,
        }
        
        return render(request, 'blog/profile.html', context)
        
    except Exception as e:
        logger.error(f"Erreur lors du chargement du profil pour {request.user}: {e}")
        messages.error(request, _('Une erreur est survenue lors du chargement de votre profil.'))
        return redirect('home')


def search_view(request):
    """
    Vue de recherche avancée pour les articles avec pagination et tri par pertinence
    """
    logger.info(f"Recherche effectuée par l'utilisateur {request.user}")
    
    form = SearchForm(request.GET or None)
    articles = []
    query = ""
    total_results = 0
    page_obj = None
    
    if form.is_valid():
        query = form.cleaned_data.get('query', '').strip()
        
        if query:
            logger.debug(f"Requête de recherche: '{query}'")
            
            # Diviser la requête en mots individuels pour une recherche plus flexible
            search_terms = [term.strip() for term in query.split() if term.strip()]
            
            if search_terms:
                # Construction de la requête Q pour rechercher dans plusieurs champs
                q_objects = Q()
                
                for term in search_terms:
                    # Recherche dans le titre, contenu et auteur
                    term_query = (
                        Q(titre__icontains=term) |
                        Q(contenu__icontains=term) |
                        Q(auteur__icontains=term)
                    )
                    q_objects &= term_query
                
                # Récupération des articles avec calcul de pertinence
                articles_queryset = Article.objects.filter(q_objects).select_related('category').annotate(
                    # Calcul du score de pertinence
                    relevance_score=Count(
                        Case(
                            # Titre : poids plus élevé
                            *[When(titre__icontains=term, then=1) for term in search_terms],
                            # Contenu : poids moyen  
                            *[When(contenu__icontains=term, then=1) for term in search_terms],
                            # Auteur : poids plus faible
                            *[When(auteur__icontains=term, then=1) for term in search_terms],
                            output_field=IntegerField(),
                        )
                    ),
                    # Ajout du nombre de likes pour affichage
                    total_likes=Count('likes')
                ).order_by('-relevance_score', '-date_creation').distinct()
                
                total_results = articles_queryset.count()
                logger.debug(f"Nombre de résultats trouvés: {total_results}")
                
                # Pagination avec 10 résultats par page
                paginator = Paginator(articles_queryset, 10)
                page_number = request.GET.get('page', 1)
                
                try:
                    page_obj = paginator.get_page(page_number)
                    articles = page_obj.object_list
                except (PageNotAnInteger, EmptyPage):
                    logger.warning(f"Numéro de page invalide: {page_number}")
                    page_obj = paginator.get_page(1)
                    articles = page_obj.object_list
            else:
                logger.debug("Requête de recherche vide après nettoyage")
        else:
            logger.debug("Aucune requête de recherche fournie")
    else:
        logger.debug("Formulaire de recherche invalide")
    
    # Préparation du contexte
    context = {
        'form': form,
        'articles': articles,
        'query': query,
        'total_results': total_results,
        'page_obj': page_obj,
        'search_terms': query.split() if query else [],
    }
    
    return render(request, 'blog/search_results.html', context)


def highlight_search_terms(text, search_terms, max_length=200):
    """
    Fonction utilitaire pour surligner les termes de recherche dans le texte
    et créer un extrait pertinent
    """
    if not search_terms or not text:
        return text[:max_length] + '...' if len(text) > max_length else text
    
    # Trouver la première occurrence d'un terme de recherche
    text_lower = text.lower()
    first_match_pos = len(text)
    
    for term in search_terms:
        term_lower = term.lower()
        pos = text_lower.find(term_lower)
        if pos != -1 and pos < first_match_pos:
            first_match_pos = pos
    
    # Si aucun terme trouvé, retourner le début du texte
    if first_match_pos == len(text):
        return text[:max_length] + '...' if len(text) > max_length else text
    
    # Créer un extrait centré sur la première occurrence
    start = max(0, first_match_pos - 50)
    end = min(len(text), start + max_length)
    excerpt = text[start:end]
    
    # Ajouter des points de suspension si nécessaire
    if start > 0:
        excerpt = '...' + excerpt
    if end < len(text):
        excerpt = excerpt + '...'
    
    # Surligner les termes de recherche
    for term in search_terms:
        if term:
            # Utiliser une regex insensible à la casse
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            excerpt = pattern.sub(f'<mark class="search-highlight">{term}</mark>', excerpt)
    
    return excerpt


@login_required
def comment_moderation_view(request):
    """
    Vue pour la modération des commentaires.
    Les admins peuvent voir tous les commentaires.
    Les journalistes ne peuvent voir que les commentaires sur leurs articles.
    """
    # Vérifier que l'utilisateur est journaliste ou administrateur
    try:
        profile = request.user.profile
        if profile.role not in ['journaliste', 'admin']:
            return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent modérer les commentaires.")
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=request.user, role='lecteur')
        return HttpResponseForbidden("Accès interdit : seuls les journalistes et administrateurs peuvent modérer les commentaires.")
    
    # Traitement des actions POST
    if request.method == 'POST':
        action = request.POST.get('action')
        comment_id = request.POST.get('comment_id')
        
        if comment_id:
            try:
                comment = Comment.objects.select_related('article').get(id=comment_id)
                
                # Vérifier les permissions pour les journalistes
                if profile.role == 'journaliste':
                    if comment.article.auteur.lower() != request.user.username.lower():
                        return HttpResponseForbidden("Vous ne pouvez modérer que les commentaires sur vos propres articles.")
                
                if action == 'approve':
                    comment.is_approved = True
                    comment.save()
                    messages.success(request, _('Commentaire approuvé avec succès'))
                    logger.info(f"Utilisateur {request.user.username} a approuvé le commentaire {comment_id}")
                    
                elif action == 'disapprove':
                    comment.is_approved = False
                    comment.save()
                    messages.success(request, _('Commentaire désapprouvé avec succès'))
                    logger.info(f"Utilisateur {request.user.username} a désapprouvé le commentaire {comment_id}")
                    
                elif action == 'delete':
                    comment_info = f"'{comment.contenu[:50]}...' de {comment.nom}"
                    comment.delete()
                    messages.success(request, _('Commentaire supprimé avec succès'))
                    logger.info(f"Utilisateur {request.user.username} a supprimé le commentaire {comment_info}")
                    
                elif action == 'reply':
                    reply_content = request.POST.get('reply_content', '').strip()
                    if reply_content:
                        Comment.objects.create(
                            article=comment.article,
                            nom=f"{request.user.username} (Modérateur)",
                            email=request.user.email or 'moderateur@blog.com',
                            contenu=reply_content,
                            parent=comment,
                            is_approved=True  # Les réponses des modérateurs sont automatiquement approuvées
                        )
                        messages.success(request, _('Réponse ajoutée avec succès'))
                        logger.info(f"Utilisateur {request.user.username} a répondu au commentaire {comment_id}")
                    else:
                        messages.error(request, _('Le contenu de la réponse ne peut pas être vide'))
                        
            except Comment.DoesNotExist:
                messages.error(request, _('Commentaire introuvable'))
        
        return redirect('comment_moderation')
    
    # Récupération et filtrage des commentaires
    comments_query = Comment.objects.select_related('article', 'parent').prefetch_related('replies')
    
    # Filtrage selon le rôle
    if profile.role == 'journaliste':
        # Les journalistes ne voient que les commentaires sur leurs articles (auteur = username exact, insensible à la casse)
        user_articles = Article.objects.filter(auteur__iexact=request.user.username)
        comments_query = comments_query.filter(article__in=user_articles)
        available_articles = user_articles
    else:
        # Les admins voient tous les commentaires
        available_articles = Article.objects.all()
    
    # Filtres de l'interface
    status_filter = request.GET.get('status', '')
    article_filter = request.GET.get('article', '')
    
    # Appliquer les filtres
    if status_filter == 'pending':
        comments_query = comments_query.filter(is_approved=False)
    elif status_filter == 'approved':
        comments_query = comments_query.filter(is_approved=True)
    
    if article_filter:
        comments_query = comments_query.filter(article_id=article_filter)
    
    # Tri par date de création (plus récents en premier)
    comments_query = comments_query.order_by('-date_creation')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(comments_query, 20)  # 20 commentaires par page
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    
    # Statistiques
    total_comments = Comment.objects.count() if profile.role == 'admin' else Comment.objects.filter(article__in=available_articles).count()
    pending_comments = Comment.objects.filter(is_approved=False).count() if profile.role == 'admin' else Comment.objects.filter(article__in=available_articles, is_approved=False).count()
    approved_comments = Comment.objects.filter(is_approved=True).count() if profile.role == 'admin' else Comment.objects.filter(article__in=available_articles, is_approved=True).count()
    
    context = {
        'comments': comments,
        'available_articles': available_articles,
        'selected_status': status_filter,
        'selected_article': int(article_filter) if article_filter else None,
        'user_role': profile.role,
        'total_comments': total_comments,
        'pending_comments': pending_comments,
        'approved_comments': approved_comments,
        'is_paginated': comments.has_other_pages(),
    }
    
    return render(request, 'blog/moderation.html', context)
