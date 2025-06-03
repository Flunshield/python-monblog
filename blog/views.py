from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
import logging
from .forms import ArticleForm, CommentForm, CategoryForm
from .models import Article, Category, UserProfile

# Configuration du logger pour ce module
logger = logging.getLogger('blog')


def home(request):
    logger.info(f"Accès à la page d'accueil par l'utilisateur {request.user}")
    
    try:
        articles = Article.objects.all()
        categories = Category.objects.all()
        category_filter = request.GET.get('category')
        
        if category_filter:
            logger.debug(f"Filtrage par catégorie: {category_filter}")
            articles = articles.filter(category_id=category_filter)
        
        logger.debug(f"Nombre d'articles trouvés: {articles.count()}")
        
        context = {
            'articles': articles,
            'categories': categories,
            'selected_category': int(category_filter) if category_filter else None
        }
        return render(request, 'blog/home.html', context)
    
    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page d'accueil: {e}")
        messages.error(request, _('Une erreur est survenue lors du chargement de la page.'))
        return render(request, 'blog/home.html', {'articles': [], 'categories': []})


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
