# 🌱 Guide des Seeders avec Docker

Ce guide explique comment utiliser les seeders automatiquement lors du déploiement Docker.

## 📋 Configurations disponibles

### 🚀 Production (`docker-compose.yml`)
- **Seeding minimal** : Rôles essentiels, catégories de base, comptes essentiels
- **Script** : `entrypoint.sh` → `seed_production`
- **Données** : Minimum nécessaire pour démarrer
- **Utilisateurs créés** : `admin`, `journaliste`, `lecteur` / `${DJANGO_ADMIN_PASSWORD}`

### 🛠️ Développement (`docker-compose.dev.yml`)
- **Seeding complet** : Données de test complètes
- **Script** : `entrypoint-with-seeding.sh` → `seed_all`
- **Données** : Utilisateurs de test, articles d'exemple, commentaires, likes
- **Mode debug** : Articles et commentaires d'exemple activés

## 🚀 Démarrage

### Production
```bash
# Démarrage production avec seeding minimal
docker-compose up -d

# Avec mot de passe admin personnalisé
DJANGO_ADMIN_PASSWORD="MonMotDePasseSecurise123!" docker-compose up -d
```

### Développement
```bash
# Démarrage développement avec données de test complètes
docker-compose -f docker-compose.dev.yml up -d

# Avec mot de passe personnalisé pour les comptes de test
DJANGO_ADMIN_PASSWORD="DevPassword123!" docker-compose -f docker-compose.dev.yml up -d
```

## 🔧 Variables d'environnement

| Variable | Description | Défaut | Environnement |
|----------|-------------|---------|---------------|
| `DJANGO_ADMIN_PASSWORD` | Mot de passe admin | `ProdAdmin2024!` | Production |
| `DJANGO_DEBUG` | Active le mode debug | `False` | Développement |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Paramètres base de données | Voir `.env` | Tous |

## 📊 Données créées

### Production (`seed_production`)
- **Rôles** : lecteur, journaliste, admin
- **Catégories** : Actualités, Technologie, Économie
- **Utilisateurs** : 3 comptes essentiels (admin, journaliste, lecteur)
- **Articles** : Aucun

### Développement (`seed_all`)
- **Rôles** : lecteur, journaliste, admin, modérateur, éditeur
- **Catégories** : 10 catégories variées
- **Utilisateurs** : 6 comptes de test avec différents rôles
- **Articles** : 15 articles d'exemple
- **Commentaires** : 30 commentaires + réponses
- **Likes** : 50 likes aléatoires

## 🔑 Comptes créés

### Production (`seed_production`)
| Username | Email | Rôle | Mot de passe |
|----------|-------|------|--------------|
| `admin` | admin@monprojet.com | admin | `${DJANGO_ADMIN_PASSWORD}` |
| `journaliste` | journaliste@monprojet.com | journaliste | `${DJANGO_ADMIN_PASSWORD}` |
| `lecteur` | lecteur@monprojet.com | lecteur | `${DJANGO_ADMIN_PASSWORD}` |

### Développement (comptes de test)
| Username | Email | Rôle | Mot de passe |
|----------|-------|------|--------------|
| `admin_test` | admin@test.com | admin | `${DJANGO_ADMIN_PASSWORD}` |
| `journaliste_test` | journaliste@test.com | journaliste | `${DJANGO_ADMIN_PASSWORD}` |
| `moderateur_test` | moderateur@test.com | modérateur | `${DJANGO_ADMIN_PASSWORD}` |
| `editeur_test` | editeur@test.com | éditeur | `${DJANGO_ADMIN_PASSWORD}` |
| `lecteur_test` | lecteur@test.com | lecteur | `${DJANGO_ADMIN_PASSWORD}` |
| `lecteur2_test` | lecteur2@test.com | lecteur | `${DJANGO_ADMIN_PASSWORD}` |

## 🛡️ Logique de seeding

### Sécurité
- ✅ Vérification des données existantes avant seeding
- ✅ Pas de re-création si données déjà présentes
- ✅ Mots de passe configurables via variables d'environnement
- ✅ Logs de toutes les opérations

### Comportement intelligent
- **Production** : Seeding uniquement si base vide
- **Développement** : Seeding complet si `DJANGO_DEBUG=True`
- **Idempotence** : Peut être relancé sans problème

## 🔄 Commandes manuelles

Si vous voulez seeder manuellement après démarrage :

```bash
# Entrer dans le conteneur
docker exec -it monprojet_web bash

# Seeding production
python manage.py seed_production

# Seeding complet
python manage.py seed_all

# Seeding individuel
python manage.py seed_roles
python manage.py seed_categories
python manage.py seed_users --password "MotDePasse123!"
python manage.py seed_articles --count 20
python manage.py seed_comments --count 50
python manage.py seed_likes --count 100

# Nettoyage
python manage.py clear_seed_data --confirm
```

## 🐳 Reconstruction avec nouveau seeding

```bash
# Production
docker-compose down -v  # Supprime les volumes (base de données)
docker-compose up -d    # Redémarre avec nouveau seeding

# Développement
docker-compose -f docker-compose.dev.yml down -v
docker-compose -f docker-compose.dev.yml up -d
```

## 📝 Logs

Les logs de seeding sont disponibles dans :
- Container : `/app/logs/info.log`
- Host : `./logs/info.log`

```bash
# Voir les logs de seeding
docker exec monprojet_web tail -f /app/logs/info.log
```

## ⚠️ Notes importantes

1. **Production** : Utilisez toujours des mots de passe forts
2. **Volumes** : Les données persistent entre redémarrages (sauf si `-v`)
3. **Première fois** : Le seeding se fait automatiquement au premier démarrage
4. **Mise à jour** : Pour re-seeder, supprimez les volumes Docker
