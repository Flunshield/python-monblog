#!/usr/bin/env python3
"""
Test direct de l'endpoint Gemini pour déboguer
"""
import requests
import json
import time

def test_gemini_endpoint():
    """Test direct de l'endpoint avec simulation d'un utilisateur connecté"""
    
    print("🧪 Test de l'endpoint Gemini...")
    
    # Simuler une session utilisateur connecté
    session = requests.Session()
    
    # Essayer d'accéder à la page d'accueil pour obtenir les cookies de session
    try:
        home_response = session.get('http://localhost:8000/fr/')
        print(f"📄 Page d'accueil: {home_response.status_code}")
        
        # Extraire le token CSRF
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', home_response.text)
        if not csrf_match:
            print("❌ Impossible de trouver le token CSRF")
            return
        
        csrf_token = csrf_match.group(1)
        print(f"🔑 Token CSRF: {csrf_token[:20]}...")
        
        # Test de l'endpoint de génération d'article
        test_data = {
            'resume': 'Écris un court article sur les chats domestiques',
            'langue': 'fr'
        }
        
        headers = {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
            'Referer': 'http://localhost:8000/fr/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
          print("🚀 Envoi de la requête de génération...")
        start_time = time.time()
        
        response = session.post(
            'http://localhost:8000/fr/generate-article-ai/',
            json=test_data,
            headers=headers
        )
        
        elapsed_time = time.time() - start_time
        print(f"⏱️  Temps de réponse: {elapsed_time:.2f}s")
        print(f"📡 Status: {response.status_code}")
        print(f"📝 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("✅ Article généré avec succès!")
                    print(f"📰 Titre: {result.get('titre', 'N/A')}")
                    print(f"📄 Contenu: {result.get('contenu', 'N/A')[:100]}...")
                else:
                    print(f"❌ Échec: {result.get('error', 'Erreur inconnue')}")
            except json.JSONDecodeError:
                print(f"❌ Réponse non-JSON: {response.text[:200]}")
        else:
            print(f"❌ Erreur HTTP {response.status_code}")
            print(f"📄 Contenu: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_gemini_endpoint()
