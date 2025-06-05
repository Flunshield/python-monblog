#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

import google.generativeai as genai
from django.conf import settings

print("🔍 Vérification des modèles Gemini disponibles")
print("=" * 50)

try:
    # Configurer l'API
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # Lister les modèles disponibles
    models = genai.list_models()
    
    print("Modèles disponibles:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name} - {model.display_name}")
            print(f"   Méthodes supportées: {model.supported_generation_methods}")
            print()
    
except Exception as e:
    print(f"❌ Erreur lors de la liste des modèles: {e}")
    import traceback
    traceback.print_exc()
