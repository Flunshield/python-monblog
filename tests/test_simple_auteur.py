#!/usr/bin/env python
"""
Script simple pour tester le pré-remplissage de l'auteur
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import UserProfile
from blog.forms import ArticleForm

def test_simple():
    print("🧪 Test simple du pré-remplissage auteur")
    print("=" * 50)
    
    # Créer un utilisateur de test
    username = 'test_simple_user'
    User.objects.filter(username=username).delete()
    
    user = User.objects.create_user(
        username=username,
        email='test@example.com',
        password='testpass123'
    )
    
    print(f"✅ Utilisateur créé: {user.username}")
    
    # Test du formulaire avec données initiales
    initial_data = {'auteur': user.username}
    form = ArticleForm(initial=initial_data)
    
    print(f"✅ Formulaire créé avec initial: {form.initial}")
    print(f"✅ Champ auteur initial: {form.initial.get('auteur')}")
    
    # Vérifier le widget readonly
    auteur_field = form.fields['auteur']
    is_readonly = auteur_field.widget.attrs.get('readonly', False)
    print(f"✅ Champ readonly: {is_readonly}")
    print(f"✅ Help text: {auteur_field.help_text}")
    
    # Nettoyer
    user.delete()
    print("✅ Test terminé avec succès!")

if __name__ == "__main__":
    test_simple()
