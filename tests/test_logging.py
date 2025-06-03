#!/usr/bin/env python
"""
Script de test pour vérifier le fonctionnement du système de logging
"""
import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

import logging
from utils.logging_utils import get_logger, log_user_action, log_method_call, log_performance, DatabaseLogger

def test_basic_logging():
    """Test des fonctionnalités de base du logging"""
    print("=== Test du logging de base ===")
    
    # Obtenir un logger pour les tests
    logger = get_logger('test')
    
    # Tester tous les niveaux de log
    logger.debug("Ceci est un message DEBUG")
    logger.info("Ceci est un message INFO")
    logger.warning("Ceci est un message WARNING")
    logger.error("Ceci est un message ERROR")
    logger.critical("Ceci est un message CRITICAL")
    
    print("Messages de log envoyés. Vérifiez les fichiers dans le dossier logs/")


def test_blog_logger():
    """Test du logger spécifique au blog"""
    print("\n=== Test du logger du blog ===")
    
    blog_logger = get_logger('blog')
    
    blog_logger.info("Test du logger du blog - opération utilisateur")
    blog_logger.debug("Détails de débogage du blog")
    blog_logger.warning("Avertissement du blog")
    blog_logger.error("Erreur simulée du blog")
    
    print("Messages du blog envoyés")


@log_performance(threshold_seconds=0.1)
def slow_function():
    """Fonction lente pour tester le logging des performances"""
    import time
    time.sleep(0.2)  # Simulation d'une opération lente
    return "Opération terminée"


@log_method_call
def test_method(param1, param2="default"):
    """Méthode de test pour le décorateur log_method_call"""
    return f"Résultat: {param1} - {param2}"


class MockRequest:
    """Mock object pour simuler une requête Django"""
    def __init__(self, username="testuser"):
        self.user = MockUser(username)


class MockUser:
    """Mock object pour simuler un utilisateur Django"""
    def __init__(self, username):
        self.username = username


@log_user_action("test d'action utilisateur")
def test_user_action(request):
    """Test du décorateur log_user_action"""
    return "Action utilisateur simulée"


def test_decorators():
    """Test des décorateurs de logging"""
    print("\n=== Test des décorateurs ===")
    
    # Test du décorateur de performance
    print("Test de performance (devrait générer un warning):")
    result = slow_function()
    print(f"Résultat: {result}")
    
    # Test du décorateur de méthode
    print("\nTest de log de méthode:")
    result = test_method("param1", param2="param2")
    print(f"Résultat: {result}")
    
    # Test du décorateur d'action utilisateur
    print("\nTest d'action utilisateur:")
    mock_request = MockRequest("utilisateur_test")
    result = test_user_action(mock_request)
    print(f"Résultat: {result}")


def test_database_logger():
    """Test du logger de base de données"""
    print("\n=== Test du logger de base de données ===")
    
    db_logger = DatabaseLogger('test.database')
    
    # Simuler différentes opérations de base de données
    db_logger.log_query('Article', 'SELECT', {'category': 'tech'}, 5)
    db_logger.log_query('User', 'INSERT', None, 1)
    
    db_logger.log_transaction_start('tx_001')
    db_logger.log_query('Article', 'UPDATE', {'id': 1}, 1)
    db_logger.log_transaction_commit('tx_001')
    
    db_logger.log_transaction_start('tx_002')
    db_logger.log_transaction_rollback('tx_002', "Violation de contrainte")
    
    print("Opérations de base de données loggées")


def test_error_handling():
    """Test de gestion d'erreurs avec logging"""
    print("\n=== Test de gestion d'erreurs ===")
    
    logger = get_logger('test.errors')
    
    try:
        # Simuler une erreur
        1 / 0
    except ZeroDivisionError as e:
        logger.error(f"Erreur de division par zéro: {e}")
        logger.debug("Détails supplémentaires de l'erreur", exc_info=True)
    
    try:
        # Simuler une autre erreur
        raise ValueError("Valeur incorrecte pour le test")
    except ValueError as e:
        logger.critical(f"Erreur critique simulée: {e}")
    
    print("Erreurs simulées et loggées")


def check_log_files():
    """Vérifier que les fichiers de log ont été créés"""
    print("\n=== Vérification des fichiers de log ===")
    
    logs_dir = Path(__file__).parent / 'logs'
    expected_files = ['debug.log', 'info.log', 'warning.log', 'error.log', 'critical.log']
    
    for filename in expected_files:
        filepath = logs_dir / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✓ {filename} existe ({size} bytes)")
        else:
            print(f"✗ {filename} n'existe pas")


def main():
    """Fonction principale du script de test"""
    print("Script de test du système de logging")
    print("=" * 50)
    
    # Exécuter tous les tests
    test_basic_logging()
    test_blog_logger()
    test_decorators()
    test_database_logger()
    test_error_handling()
    check_log_files()
    
    print("\n" + "=" * 50)
    print("Tests terminés. Consultez les fichiers dans le dossier logs/ pour voir les résultats.")


if __name__ == "__main__":
    main()
