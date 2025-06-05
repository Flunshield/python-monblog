#!/usr/bin/env python
"""
Test du service Gemini avec le modèle Flash 2.0
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from blog.services.gemini_service import GeminiService

def test_gemini_service():
    print("🧪 Test du service Gemini avec le modèle Flash 2.0")
    print("=" * 60)
    
    try:
        # Initialiser le service
        print("📡 Initialisation du service Gemini...")
        service = GeminiService()
        print("✅ Service initialisé avec succès!")
        
        # Test de connexion
        print("\n🔗 Test de connexion...")
        if service.test_connection():
            print("✅ Connexion réussie!")
        else:
            print("❌ Échec de la connexion")
            return False
        
        # Test de génération d'article
        print("\n📝 Test de génération d'article...")
        resume = "Les nouvelles technologies d'intelligence artificielle transforment le monde du travail et de l'éducation"
        
        print(f"📋 Résumé: {resume}")
        print("⏳ Génération en cours...")
        
        result = service.generate_article_content(resume, "fr")
        
        print("\n🎉 Article généré avec succès!")
        print("-" * 40)
        print(f"📰 Titre: {result['titre']}")
        print("-" * 40)
        print(f"📄 Contenu ({len(result['contenu'])} caractères):")
        print(result['contenu'][:300] + "..." if len(result['contenu']) > 300 else result['contenu'])
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_service()
    print(f"\n{'✅ Test réussi!' if success else '❌ Test échoué!'}")
