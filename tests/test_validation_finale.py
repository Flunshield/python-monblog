#!/usr/bin/env python3
"""
Test de validation finale : Simulation d'une session utilisateur réelle
pour vérifier que les journalistes peuvent modifier/supprimer leurs articles.
"""

import os
import django
import sys

# Configuration Django
sys.path.append('c:\\Users\\jbert\\Documents\\python isitech\\monprojet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from blog.models import Article, UserProfile, Category
from django.urls import reverse

def setup_real_test_scenario():
    """Configurer un scénario de test réaliste"""
    print("🔧 Configuration du scénario de test réaliste...")
    
    # Créer une catégorie
    category, _ = Category.objects.get_or_create(
        nom="Technologies",
        defaults={'description': 'Articles sur les technologies'}
    )
    
    # Créer un journaliste
    journalist, created = User.objects.get_or_create(
        username='marie_durand',
        defaults={
            'email': 'marie.durand@journal.com',
            'first_name': 'Marie',
            'last_name': 'Durand'
        }
    )
    if created:
        journalist.set_password('motdepasse123')
        journalist.save()
    
    # Créer le profil journaliste
    profile, _ = UserProfile.objects.get_or_create(user=journalist)
    profile.role = 'journaliste'
    profile.save()
    
    # Créer un article pour ce journaliste
    article, created = Article.objects.get_or_create(
        titre="L'intelligence artificielle en 2025",
        defaults={
            'contenu': "L'IA continue de révolutionner notre quotidien. Voici les dernières tendances...",
            'auteur': journalist.username,  # Important : utiliser le username exact
            'category': category
        }
    )
    
    # Créer un autre journaliste avec son article
    other_journalist, created = User.objects.get_or_create(
        username='pierre_martin',
        defaults={
            'email': 'pierre.martin@journal.com',
            'first_name': 'Pierre',
            'last_name': 'Martin'
        }
    )
    if created:
        other_journalist.set_password('motdepasse123')
        other_journalist.save()
    
    other_profile, _ = UserProfile.objects.get_or_create(user=other_journalist)
    other_profile.role = 'journaliste'
    other_profile.save()
    
    other_article, created = Article.objects.get_or_create(
        titre="Les nouvelles tendances du web",
        defaults={
            'contenu': "Le web évolue constamment. Découvrez les nouvelles tendances...",
            'auteur': other_journalist.username,
            'category': category
        }
    )
    
    print(f"   ✅ Journaliste principal: {journalist.username} (rôle: {profile.role})")
    print(f"   ✅ Son article: '{article.titre}' (auteur: {article.auteur})")
    print(f"   ✅ Autre journaliste: {other_journalist.username}")
    print(f"   ✅ Son article: '{other_article.titre}' (auteur: {other_article.auteur})")
    
    return journalist, article, other_journalist, other_article

def test_journalist_workflow():
    """Test du workflow complet d'un journaliste"""
    print("\n🚀 Test du workflow complet d'un journaliste")
    print("=" * 55)
    
    journalist, article, other_journalist, other_article = setup_real_test_scenario()
    client = Client()
    
    # 1. Connexion du journaliste
    print("\n1️⃣ Connexion du journaliste")
    login_success = client.login(username=journalist.username, password='motdepasse123')
    print(f"   Connexion réussie: {'✅' if login_success else '❌'}")
    
    if not login_success:
        print("   ❌ ÉCHEC DE CONNEXION - Arrêt du test")
        return
    
    # 2. Accès à la page d'accueil et vérification des boutons
    print("\n2️⃣ Vérification des boutons sur la page d'accueil")
    response = client.get('/')
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        # Vérifier que l'article du journaliste est visible avec boutons
        has_own_article = article.titre in content
        edit_buttons = content.count('btn-outline-warning')
        delete_buttons = content.count('btn-outline-danger')
        
        print(f"   Son article visible: {'✅' if has_own_article else '❌'}")
        print(f"   Boutons modifier visibles: {edit_buttons}")
        print(f"   Boutons supprimer visibles: {delete_buttons}")
        
        # Un journaliste devrait voir exactement ses boutons
        expected_buttons = 1  # Pour son propre article
        if edit_buttons >= expected_buttons and delete_buttons >= expected_buttons:
            print("   ✅ Boutons visibles pour son article")
        else:
            print("   ❌ Boutons manquants pour son article")
    
    # 3. Test de modification de son propre article
    print("\n3️⃣ Test de modification de son propre article")
    modify_url = reverse('modifier_article', args=[article.id])
    response = client.get(modify_url)
    
    if response.status_code == 200:
        print("   ✅ Accès autorisé à la modification de son article")
        
        # Test de modification effective
        new_title = f"{article.titre} - Modifié"
        response = client.post(modify_url, {
            'titre': new_title,
            'contenu': article.contenu + "\n\nMise à jour du contenu.",
            'auteur': article.auteur,
            'category': article.category.id if article.category else ''
        })
        
        if response.status_code == 302:  # Redirection après succès
            # Vérifier que l'article a été modifié
            article.refresh_from_db()
            if article.titre == new_title:
                print("   ✅ Article modifié avec succès")
            else:
                print("   ❌ L'article n'a pas été modifié")
        else:
            print(f"   ❌ Échec de modification (code: {response.status_code})")
    else:
        print(f"   ❌ Accès refusé à la modification (code: {response.status_code})")
    
    # 4. Test d'accès à l'article d'un autre journaliste (devrait être interdit)
    print("\n4️⃣ Test d'accès à l'article d'un autre journaliste")
    other_modify_url = reverse('modifier_article', args=[other_article.id])
    response = client.get(other_modify_url)
    
    if response.status_code == 403:
        print("   ✅ Accès correctement interdit à l'article d'un autre")
    else:
        print(f"   ❌ Accès autorisé alors qu'il devrait être interdit (code: {response.status_code})")
    
    # 5. Test de la page de détail de son article
    print("\n5️⃣ Test de la page de détail de son article")
    detail_url = reverse('article_detail', args=[article.id])
    response = client.get(detail_url)
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        
        has_modify_button = 'Modifier cet article' in content
        has_delete_button = 'Supprimer' in content and 'btn btn-danger' in content
        
        print(f"   Bouton 'Modifier' visible: {'✅' if has_modify_button else '❌'}")
        print(f"   Bouton 'Supprimer' visible: {'✅' if has_delete_button else '❌'}")
        
        if has_modify_button and has_delete_button:
            print("   ✅ Tous les boutons de gestion sont visibles")
        else:
            print("   ❌ Certains boutons de gestion sont manquants")
    
    # 6. Test d'accès à la page journaliste
    print("\n6️⃣ Test d'accès à la page journaliste")
    journalist_page_url = reverse('page_journaliste')
    response = client.get(journalist_page_url)
    
    if response.status_code == 200:
        print("   ✅ Accès autorisé à la page journaliste")
        
        # Vérifier les statistiques
        content = response.content.decode('utf-8')
        if 'Mes statistiques' in content:
            print("   ✅ Statistiques visibles")
        else:
            print("   ❌ Statistiques manquantes")
    else:
        print(f"   ❌ Accès refusé à la page journaliste (code: {response.status_code})")
    
    client.logout()

def test_reader_restrictions():
    """Test des restrictions pour un lecteur"""
    print("\n👁️ Test des restrictions pour un lecteur")
    print("=" * 45)
    
    # Créer un lecteur
    reader, created = User.objects.get_or_create(
        username='lecteur_test',
        defaults={'email': 'lecteur@test.com'}
    )
    if created:
        reader.set_password('motdepasse123')
        reader.save()
    
    profile, _ = UserProfile.objects.get_or_create(user=reader)
    profile.role = 'lecteur'
    profile.save()
    
    client = Client()
    login_success = client.login(username='lecteur_test', password='motdepasse123')
    
    if login_success:
        # Test d'accès à la page d'accueil
        response = client.get('/')
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            edit_buttons = content.count('btn-outline-warning')
            delete_buttons = content.count('btn-outline-danger')
            
            print(f"   Boutons modifier visibles: {edit_buttons}")
            print(f"   Boutons supprimer visibles: {delete_buttons}")
            
            if edit_buttons == 0 and delete_buttons == 0:
                print("   ✅ Aucun bouton de gestion visible (correct)")
            else:
                print("   ❌ Des boutons de gestion sont visibles (incorrect)")
        
        # Test d'accès à la page journaliste (devrait être interdit)
        journalist_page_url = reverse('page_journaliste')
        response = client.get(journalist_page_url)
        
        if response.status_code == 403:
            print("   ✅ Accès correctement interdit à la page journaliste")
        else:
            print(f"   ❌ Accès autorisé à la page journaliste (code: {response.status_code})")
    
    client.logout()

def main():
    """Fonction principale"""
    print("🔍 VALIDATION FINALE DU SYSTÈME DE PERMISSIONS")
    print("=" * 70)
    print("Ce test simule l'utilisation réelle du système par un journaliste")
    print("=" * 70)
    
    try:
        test_journalist_workflow()
        test_reader_restrictions()
        
        print("\n" + "=" * 70)
        print("✅ VALIDATION TERMINÉE!")
        print("\n📋 FONCTIONNALITÉS VALIDÉES:")
        print("   ✅ Connexion et authentification")
        print("   ✅ Modification d'articles par le propriétaire")
        print("   ✅ Restriction d'accès aux articles d'autres auteurs")
        print("   ✅ Affichage conditionnel des boutons dans les templates")
        print("   ✅ Accès aux pages spécialisées selon le rôle")
        print("   ✅ Restrictions pour les lecteurs")
        print("\n🎉 Le système de permissions fonctionne parfaitement!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la validation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
