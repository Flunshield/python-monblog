from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def user_role(user):
    """Retourne le rôle de l'utilisateur."""
    if user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.role
    return 'lecteur'

@register.filter
def has_role(user, role):
    """Vérifie si l'utilisateur a un rôle spécifique."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    return user.profile.role == role

@register.filter
def can_access_admin(user):
    """Vérifie si l'utilisateur peut accéder aux fonctions admin."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    return user.profile.role in ['admin', 'journaliste']

@register.filter
def is_admin(user):
    """Vérifie si l'utilisateur est admin."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    return user.profile.role == 'admin'

@register.filter
def is_journaliste(user):
    """Vérifie si l'utilisateur est journaliste."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    return user.profile.role == 'journaliste'

@register.filter
def is_lecteur(user):
    """Vérifie si l'utilisateur est lecteur."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return True
    return user.profile.role == 'lecteur'

@register.filter
def can_edit_article(user, article):
    """Vérifie si l'utilisateur peut modifier un article."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    
    # Les admins peuvent modifier tous les articles
    if user.profile.role == 'admin':
        return True
    
    # Les journalistes peuvent modifier leurs propres articles
    if user.profile.role == 'journaliste':
        return article.auteur.lower() == user.username.lower()
    
    # Les lecteurs ne peuvent rien modifier
    return False

@register.filter
def can_delete_article(user, article):
    """Vérifie si l'utilisateur peut supprimer un article."""
    if not user.is_authenticated or not hasattr(user, 'profile'):
        return False
    
    # Les admins peuvent supprimer tous les articles
    if user.profile.role == 'admin':
        return True
    
    # Les journalistes peuvent supprimer leurs propres articles
    if user.profile.role == 'journaliste':
        return article.auteur.lower() == user.username.lower()
    
    # Les lecteurs ne peuvent rien supprimer
    return False

@register.filter
def is_liked_by(article, user):
    """Vérifie si un article est liké par l'utilisateur."""
    if not user.is_authenticated:
        return False
    return article.is_liked_by(user)