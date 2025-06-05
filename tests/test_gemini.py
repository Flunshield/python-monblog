#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from blog.services.gemini_service import GeminiService

print("🤖 Test du service Gemini")
print("=" * 40)

try:
    # Initialiser le service
    gemini = GeminiService()
    print("✅ Service Gemini initialisé avec succès")
    
    # Test de génération avec un résumé simple
    resume = "Comment préparer un café français traditionnel avec une presse française"
    print(f"\n📝 Résumé de test: {resume}")
    print("\n⏳ Génération en cours...")
    
    result = gemini.generate_article_content(resume, 'fr')
    
    print("\n🎉 Résultat généré:")
    print("-" * 30)
    print(f"📰 Titre: {result['titre']}")
    print(f"\n📖 Contenu (premiers 200 caractères):")
    print(result['contenu'][:200] + "..." if len(result['contenu']) > 200 else result['contenu'])
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
