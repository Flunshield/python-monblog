"""
Utilitaires de logging pour le projet MonBlog
"""
import logging
import functools
import traceback
from django.contrib.auth.models import AnonymousUser


def get_logger(name):
    """
    Retourne un logger configuré pour le module spécifié
    
    Args:
        name (str): Nom du module (ex: 'blog.views', 'monprojet.models')
    
    Returns:
        logging.Logger: Logger configuré
    """
    return logging.getLogger(name)


def log_user_action(action_name):
    """
    Décorateur pour logger automatiquement les actions des utilisateurs
    
    Args:
        action_name (str): Nom de l'action à logger
    
    Usage:
        @log_user_action("création d'article")
        def create_article(request):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            logger = get_logger(func.__module__)
            
            user_info = "anonyme" if isinstance(request.user, AnonymousUser) else request.user.username
            logger.info(f"Action '{action_name}' initiée par l'utilisateur {user_info}")
            
            try:
                result = func(request, *args, **kwargs)
                logger.info(f"Action '{action_name}' réussie pour l'utilisateur {user_info}")
                return result
            except Exception as e:
                logger.error(f"Erreur lors de l'action '{action_name}' pour l'utilisateur {user_info}: {e}")
                logger.debug(f"Traceback complet: {traceback.format_exc()}")
                raise
        return wrapper
    return decorator


def log_method_call(func):
    """
    Décorateur pour logger automatiquement les appels de méthodes
    
    Usage:
        @log_method_call
        def my_method(self, arg1, arg2):
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # Construire les arguments pour le log
        args_str = ', '.join([str(arg) for arg in args[1:]])  # Exclure 'self'
        kwargs_str = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        
        logger.debug(f"Appel de {func.__name__}({all_args})")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} terminé avec succès")
            return result
        except Exception as e:
            logger.error(f"Erreur dans {func.__name__}: {e}")
            raise
    return wrapper


def log_performance(threshold_seconds=1.0):
    """
    Décorateur pour logger les performances des fonctions
    
    Args:
        threshold_seconds (float): Seuil en secondes au-delà duquel un warning est émis
    
    Usage:
        @log_performance(threshold_seconds=2.0)
        def slow_function():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            logger = get_logger(func.__module__)
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                
                if execution_time > threshold_seconds:
                    logger.warning(f"{func.__name__} a pris {execution_time:.2f}s à s'exécuter (seuil: {threshold_seconds}s)")
                else:
                    logger.debug(f"{func.__name__} exécuté en {execution_time:.2f}s")
                
                return result
            except Exception as e:
                end_time = time.time()
                execution_time = end_time - start_time
                logger.error(f"{func.__name__} a échoué après {execution_time:.2f}s: {e}")
                raise
        return wrapper
    return decorator


class DatabaseLogger:
    """
    Classe utilitaire pour logger les opérations de base de données
    """
    
    def __init__(self, logger_name='database'):
        self.logger = get_logger(logger_name)
    
    def log_query(self, model_name, operation, filters=None, count=None):
        """
        Log une requête de base de données
        
        Args:
            model_name (str): Nom du modèle
            operation (str): Type d'opération (SELECT, INSERT, UPDATE, DELETE)
            filters (dict): Filtres appliqués
            count (int): Nombre de résultats/lignes affectées
        """
        filters_str = f" avec filtres {filters}" if filters else ""
        count_str = f" ({count} résultats)" if count is not None else ""
        self.logger.debug(f"{operation} sur {model_name}{filters_str}{count_str}")
    
    def log_transaction_start(self, transaction_id=None):
        """Log le début d'une transaction"""
        tx_id = f" (ID: {transaction_id})" if transaction_id else ""
        self.logger.debug(f"Début de transaction{tx_id}")
    
    def log_transaction_commit(self, transaction_id=None):
        """Log le commit d'une transaction"""
        tx_id = f" (ID: {transaction_id})" if transaction_id else ""
        self.logger.debug(f"Commit de transaction{tx_id}")
    
    def log_transaction_rollback(self, transaction_id=None, reason=None):
        """Log le rollback d'une transaction"""
        tx_id = f" (ID: {transaction_id})" if transaction_id else ""
        reason_str = f" - Raison: {reason}" if reason else ""
        self.logger.warning(f"Rollback de transaction{tx_id}{reason_str}")


# Instance globale du logger de base de données
db_logger = DatabaseLogger()
