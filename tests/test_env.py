#!/usr/bin/env python3
import os
from decouple import config

print("=== Test des variables d'environnement ===")
print(f"DEBUG = {config('DEBUG', default='NOT_SET')}")
print(f"DB_NAME = {config('DB_NAME', default='NOT_SET')}")
print(f"DB_USER = {config('DB_USER', default='NOT_SET')}")
print(f"DB_PASSWORD = {config('DB_PASSWORD', default='NOT_SET')}")
print(f"DB_HOST = {config('DB_HOST', default='NOT_SET')}")
print(f"DB_PORT = {config('DB_PORT', default='NOT_SET')}")

print("\n=== Variables d'environnement système ===")
for key in ['DEBUG', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT']:
    value = os.environ.get(key, 'NOT_SET')
    print(f"{key} = {value}")

print("\n=== Fichier .env existe ===")
env_file = os.path.join(os.path.dirname(__file__), '.env')
print(f"Fichier .env: {env_file}")
print(f"Existe: {os.path.exists(env_file)}")

if os.path.exists(env_file):
    print("\n=== Contenu du fichier .env ===")
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Taille du fichier: {len(content)} caractères")
            if content:
                print("Contenu:")
                print(content[:500] + "..." if len(content) > 500 else content)
            else:
                print("Le fichier est vide!")
    except Exception as e:
        print(f"Erreur de lecture: {e}")
        
    # Test avec différents encodages
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            with open(env_file, 'r', encoding=encoding) as f:
                content = f.read()
                if content:
                    print(f"\n=== Contenu avec encodage {encoding} ===")
                    print(content[:200])
                    break
        except Exception as e:
            print(f"Erreur avec encodage {encoding}: {e}")
            
    # Test de lecture ligne par ligne
    try:
        print("\n=== Lecture ligne par ligne ===")
        with open(env_file, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                print(f"Ligne {i+1}: {repr(line)}")
                if i > 5:  # Limiter à 5 lignes
                    break
    except Exception as e:
        print(f"Erreur lecture ligne par ligne: {e}")
