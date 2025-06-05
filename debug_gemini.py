#!/usr/bin/env python3
"""
Script de test pour diagnostiquer le problème de génération d'articles
"""

import requests
import json

def test_gemini_endpoint():
    """Test direct de l'endpoint de génération d'articles"""
    
    print("🔍 Test de l'endpoint de génération d'articles")
    print("=" * 50)
    
    # URL de l'endpoint
    url = 'http://localhost:8000/generate-article-ai/'
    
    # D'abord, obtenir un token CSRF
    session = requests.Session()
    
    try:
        # Obtenir la page du générateur pour récupérer le CSRF token
        page_response = session.get('http://localhost:8000/fr/gemini-generator/')
        
        if page_response.status_code == 302:
            print("❌ Redirection détectée - vous devez être connecté")
            print("Essayez de vous connecter d'abord sur l'interface web")
            return
        elif page_response.status_code != 200:
            print(f"❌ Erreur lors du chargement de la page: {page_response.status_code}")
            return
        
        # Extraire le token CSRF
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page_response.text)
        
        if not csrf_match:
            print("❌ Token CSRF non trouvé")
            return
        
        csrf_token = csrf_match.group(1)
        print(f"✅ Token CSRF obtenu: {csrf_token[:20]}...")
        
        # Préparer les données de test
        test_data = {
            'resume': 'Écris un court article sur les chats et leur comportement',
            'langue': 'fr'
        }
        
        headers = {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Referer': 'http://localhost:8000/fr/gemini-generator/'
        }
        
        print(f"📤 Envoi de la requête POST vers: {url}")
        print(f"📦 Données: {test_data}")
        
        # Envoyer la requête
        response = session.post(url, json=test_data, headers=headers)
        
        print(f"📡 Code de réponse: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Réponse JSON reçue:")
                print(f"   Success: {result.get('success', 'N/A')}")
                
                if result.get('success'):
                    print(f"   Titre: {result.get('titre', 'N/A')}")
                    print(f"   Contenu (préview): {result.get('contenu', '')[:100]}...")
                    print("🎉 Génération réussie!")
                else:
                    print(f"   Erreur: {result.get('error', 'Erreur inconnue')}")
                    
            except json.JSONDecodeError:
                print("❌ Réponse non-JSON:")
                print(response.text[:500])
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print("Réponse:", response.text[:500])
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur")
        print("Assurez-vous que le serveur Django fonctionne sur localhost:8000")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def test_gemini_service_directly():
    """Test direct du service Gemini"""
    
    print("\n🧪 Test direct du service Gemini")
    print("=" * 50)
    
    try:
        import sys
        import os
        
        # Ajouter le répertoire du projet au path
        project_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_dir)
        
        # Configurer Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
        
        import django
        django.setup()
        
        from blog.services.gemini_service import GeminiService
        
        print("✅ Service Gemini importé")
        
        # Tester la connexion
        service = GeminiService()
        print("✅ Service initialisé")
        
        # Test de connexion
        if service.test_connection():
            print("✅ Connexion API Gemini OK")
            
            # Test de génération
            result = service.generate_article_content(
                "Écris un court article sur les chats",
                "fr"
            )
            
            print("✅ Article généré avec succès!")
            print(f"   Titre: {result['titre']}")
            print(f"   Contenu (préview): {result['contenu'][:100]}...")
            
        else:
            print("❌ Échec de la connexion API Gemini")
            
    except Exception as e:
        print(f"❌ Erreur lors du test du service: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_endpoint()
    test_gemini_service_directly()
