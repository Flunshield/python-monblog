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