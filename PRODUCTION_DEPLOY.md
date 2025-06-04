# 🚀 Déploiement Production - MonProjet Django Blog

Ce guide explique comment déployer l'application en mode production avec le Dockerfile optimisé.

## 📋 Caractéristiques du Mode Production

### 🔒 Sécurité
- **Utilisateur non-root** : L'application s'exécute avec l'utilisateur `django`
- **Variables d'environnement** : Configuration sécurisée par défaut
- **Debug désactivé** : `DJANGO_DEBUG=False`

### 👥 Comptes Créés Automatiquement
Le seeding de production crée **3 comptes essentiels** :

| Username | Email | Rôle | Privilèges |
|----------|-------|------|------------|
| `admin` | admin@monprojet.com | admin | Superuser + Staff |
| `journaliste` | journaliste@monprojet.com | journaliste | Staff |
| `lecteur` | lecteur@monprojet.com | lecteur | Utilisateur standard |

**Mot de passe par défaut :** `ProdAdmin2024!` (configurable)

## 🚀 Déploiement Rapide

### Option 1 : Avec Docker Compose (Recommandé)
```bash
# Démarrage production standard
docker-compose up -d

# Avec mot de passe personnalisé
DJANGO_ADMIN_PASSWORD="MonMotDePasseSecurise2024!" docker-compose up -d
```

### Option 2 : Docker Run Direct
```bash
# Build de l'image
docker build -t monprojet-prod .

# Run avec base de données externe
docker run -d \
  --name monprojet_web \
  -p 8000:8000 \
  -e DJANGO_ADMIN_PASSWORD="VotreMotDePasse123!" \
  -e DB_HOST="votre_db_host" \
  -e DB_NAME="votre_db_name" \
  -e DB_USER="votre_db_user" \
  -e DB_PASSWORD="votre_db_password" \
  monprojet-prod
```

## 🔧 Variables d'Environnement

### Obligatoires
| Variable | Description | Défaut |
|----------|-------------|---------|
| `DJANGO_ADMIN_PASSWORD` | Mot de passe pour tous les comptes | `ProdAdmin2024!` |

### Base de Données
| Variable | Description | Défaut |
|----------|-------------|---------|
| `DB_HOST` | Host de la base de données | `db` |
| `DB_NAME` | Nom de la base de données | `monprojet` |
| `DB_USER` | Utilisateur de la base | `monprojet` |
| `DB_PASSWORD` | Mot de passe de la base | Voir `.env` |

### Optionnelles
| Variable | Description | Défaut |
|----------|-------------|---------|
| `DJANGO_DEBUG` | Mode debug (NE PAS ACTIVER EN PROD) | `False` |
| `DJANGO_SETTINGS_MODULE` | Module de settings | `monprojet.settings` |

## 📊 Processus de Démarrage

1. **🔄 Attente base de données** : Vérification de la connectivité
2. **🗄️ Migrations** : Application automatique des migrations
3. **🌱 Seeding production** : Création des données essentielles
4. **📁 Collecte statique** : Préparation des fichiers statiques
5. **🌐 Traductions** : Compilation des messages
6. **⚡ Gunicorn** : Démarrage du serveur de production

## 🔐 Sécurité en Production

### ✅ Bonnes Pratiques Appliquées
- Utilisateur non-root dans le conteneur
- Debug désactivé par défaut
- Collecte statique sécurisée
- Seeding intelligent (évite la duplication)
- Logs structurés

### 🚨 Important
1. **Changez le mot de passe par défaut** avant le déploiement
2. **Utilisez HTTPS** en production avec un reverse proxy
3. **Configurez les logs externes** pour la surveillance
4. **Sauvegardes régulières** de la base de données

## 📝 Logs

Les logs sont disponibles dans le conteneur :
```bash
# Voir les logs de l'application
docker logs monprojet_web

# Logs détaillés du seeding
docker exec monprojet_web cat /app/logs/info.log
```

## 🔄 Mise à Jour

Pour mettre à jour l'application :
```bash
# Arrêter l'application
docker-compose down

# Reconstruire l'image
docker-compose build

# Redémarrer
docker-compose up -d
```

## ⚠️ Dépannage

### Problème de connexion base de données
```bash
# Vérifier les logs
docker logs monprojet_web

# Tester la connectivité DB
docker exec monprojet_web nc -z db 5432
```

### Recréer les comptes utilisateurs
```bash
# Entrer dans le conteneur
docker exec -it monprojet_web bash

# Re-seeder manuellement
python manage.py seed_production --admin-password "NouveauMotDePasse123!"
```

---

**📞 Support** : Consultez les logs dans `/app/logs/` pour diagnostiquer les problèmes.
