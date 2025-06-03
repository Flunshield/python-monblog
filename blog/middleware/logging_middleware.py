"""
Middleware de logging pour le projet MonBlog
"""
import logging
import time
import uuid
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('monprojet.middleware')


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware pour logger automatiquement toutes les requêtes HTTP
    """
    
    def process_request(self, request):
        """Traitement au début de chaque requête"""
        # Générer un ID unique pour la requête
        request.request_id = str(uuid.uuid4())[:8]
        request.start_time = time.time()
        
        # Logger les informations de la requête
        user_info = "anonyme" if request.user.is_anonymous else request.user.username
        logger.info(
            f"[{request.request_id}] {request.method} {request.get_full_path()} "
            f"- Utilisateur: {user_info} - IP: {self.get_client_ip(request)}"
        )
        
        # Logger les paramètres GET/POST (attention aux données sensibles)
        if request.GET:
            safe_get = {k: v for k, v in request.GET.items() if not self.is_sensitive_param(k)}
            if safe_get:
                logger.debug(f"[{request.request_id}] Paramètres GET: {safe_get}")
        
        if request.method == 'POST' and hasattr(request, 'POST'):
            safe_post = {k: v for k, v in request.POST.items() if not self.is_sensitive_param(k)}
            if safe_post:
                logger.debug(f"[{request.request_id}] Paramètres POST: {safe_post}")
    
    def process_response(self, request, response):
        """Traitement à la fin de chaque requête"""
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            request_id = getattr(request, 'request_id', 'unknown')
            
            # Déterminer le niveau de log selon le code de statut et la durée
            if response.status_code >= 500:
                log_level = logging.ERROR
            elif response.status_code >= 400:
                log_level = logging.WARNING
            elif duration > 2.0:  # Requête lente
                log_level = logging.WARNING
            else:
                log_level = logging.INFO
              # Gestion des différents types de réponse
            try:
                if hasattr(response, 'content'):
                    content_size = len(response.content)
                elif hasattr(response, 'streaming_content'):
                    content_size = "streaming"
                else:
                    content_size = "unknown"
                
                logger.log(
                    log_level,
                    f"[{request_id}] Réponse {response.status_code} "
                    f"en {duration:.3f}s - Taille: {content_size} bytes"
                )
            except Exception as e:
                logger.log(
                    log_level,
                    f"[{request_id}] Réponse {response.status_code} "
                    f"en {duration:.3f}s - Erreur taille: {e}"
                )
        
        return response
    
    def process_exception(self, request, exception):
        """Traitement des exceptions"""
        request_id = getattr(request, 'request_id', 'unknown')
        logger.error(
            f"[{request_id}] Exception non gérée: {type(exception).__name__}: {exception}",
            exc_info=True
        )
        
        # Ne pas intercepter l'exception, la laisser passer
        return None
    
    @staticmethod
    def get_client_ip(request):
        """Obtenir l'adresse IP du client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def is_sensitive_param(param_name):
        """Vérifier si un paramètre contient des données sensibles"""
        sensitive_keywords = [
            'password', 'passwd', 'pwd', 'token', 'secret', 'key',
            'csrf', 'csrfmiddlewaretoken', 'api_key', 'auth'
        ]
        return any(keyword in param_name.lower() for keyword in sensitive_keywords)


class UserActionLoggingMiddleware(MiddlewareMixin):
    """
    Middleware pour logger les actions importantes des utilisateurs
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """Traitement avant l'exécution de la vue"""
        # Logger les actions importantes
        important_views = [
            'ajouter_article', 'modifier_article', 'supprimer_article',
            'login', 'logout', 'register', 'ajouter_categorie'
        ]
        
        view_name = getattr(view_func, '__name__', 'unknown')
        if view_name in important_views:
            user_info = "anonyme" if request.user.is_anonymous else request.user.username
            request_id = getattr(request, 'request_id', 'unknown')
            
            logger.info(
                f"[{request_id}] Action importante: {view_name} "
                f"par l'utilisateur {user_info}"
            )
        
        return None
