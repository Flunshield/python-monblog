#!/usr/bin/env python3
"""
Script pour corriger les traductions françaises manquantes
"""
import os
import re

def fix_french_translations():
    """Corriger les traductions françaises en copiant les msgid français vers msgstr"""
    
    po_file_path = r"c:\Users\jbert\Documents\python isitech\monprojet\locale\fr\LC_MESSAGES\django.po"
    
    # Lire le fichier
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Liste des traductions à corriger (msgid en français -> msgstr correspondant)
    french_translations = {
        "Page Admin": "Page Admin",
        "Panneau d'Administration": "Panneau d'Administration", 
        "Accès Admin": "Accès Admin",
        "Articles": "Articles",
        "Gérer tous les articles du blog": "Gérer tous les articles du blog",
        "Voir tous les articles": "Voir tous les articles",
        "Ajouter un article": "Ajouter un article",
        "Catégories": "Catégories",
        "Gérer toutes les catégories": "Gérer toutes les catégories",
        "Voir toutes les catégories": "Voir toutes les catégories",
        "Ajouter une catégorie": "Ajouter une catégorie",
        "Utilisateurs": "Utilisateurs",
        "Gérer les utilisateurs et leurs rôles": "Gérer les utilisateurs et leurs rôles",
        "Gérer les utilisateurs": "Gérer les utilisateurs",
        "Modifier l'article": "Modifier l'article",
        "Titre": "Titre",
        "Contenu": "Contenu",
        "Sauvegarder les modifications": "Sauvegarder les modifications",
        "Auteur": "Auteur",
        "Catégorie": "Catégorie",
        "Image": "Image",
        "Créer une nouvelle catégorie": "Créer une nouvelle catégorie",
        "Supprimer l'article": "Supprimer l'article",
        "Supprimer définitivement": "Supprimer définitivement",
        "Annuler": "Annuler",
        "Gérer les articles": "Gérer les articles",
        "Effacer le filtre": "Effacer le filtre",
        "Actions": "Actions",
        "Modifier": "Modifier",
        "Supprimer": "Supprimer",
        "Aucun article trouvé": "Aucun article trouvé",
        "Commencer à publier": "Commencer à publier",
        "Nom": "Nom",
        "Email": "Email",
        "Commentaire": "Commentaire",
        "Publier le commentaire": "Publier le commentaire",
        "Ajouter un commentaire": "Ajouter un commentaire",
        "Mes Articles": "Mes Articles",
        "Créer et gérer vos articles": "Créer et gérer vos articles",
        "Voir mes articles": "Voir mes articles",
        "Créer un article": "Créer un article",
        "Consulter les catégories disponibles": "Consulter les catégories disponibles",
        "Voir les catégories": "Voir les catégories",
        "Créer une catégorie": "Créer une catégorie",
        "(Réservé aux admins)": "(Réservé aux admins)",
        "Guide rapide": "Guide rapide",
        "Ce que vous pouvez faire :": "Ce que vous pouvez faire :",
        "Restrictions :": "Restrictions :",
        "Créer et modifier vos articles": "Créer et modifier vos articles",
        "Voir toutes les catégories": "Voir toutes les catégories",
        "Gérer vos publications": "Gérer vos publications",
        "Consulter vos statistiques": "Consulter vos statistiques",
        "Pas de création de catégories": "Pas de création de catégories",
        "Pas d'accès à l'admin Django": "Pas d'accès à l'admin Django",
        "Statistiques personnelles": "Statistiques personnelles",
        "Vos articles": "Vos articles",
        "Articles ce mois": "Articles ce mois",
        "Commentaires reçus": "Commentaires reçus",
        "Ajouter un Nouvel Article": "Ajouter un Nouvel Article",
        "Titre de l'article": "Titre de l'article",
        "Contenu de l'article": "Contenu de l'article",
        "Formats acceptés: JPG, PNG, GIF (optionnel)": "Formats acceptés : JPG, PNG, GIF (optionnel)",
        "Ajouter l'article": "Ajouter l'article"
    }
    
    # Appliquer les corrections
    for msgid, msgstr in french_translations.items():
        # Pattern pour trouver les entrées avec msgstr vides
        pattern = rf'(msgid "{re.escape(msgid)}"\s*msgstr )""\s*'
        replacement = rf'\1"{msgstr}"\n'
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    
    # Sauvegarder le fichier modifié
    with open(po_file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Traductions françaises corrigées !")

if __name__ == '__main__':
    fix_french_translations()
