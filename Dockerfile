# Dockerfile pour MonProjet Django Blog (production)
FROM python:3.10-slim

# Variables d'environnement de production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=False
ENV DJANGO_ADMIN_PASSWORD=ProdAdmin2024!
ENV DJANGO_SETTINGS_MODULE=monprojet.settings

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev gettext netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt ./

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Créer le dossier des logs avec permissions appropriées
RUN mkdir -p logs && chmod 755 logs

# Créer les fichiers de logs nécessaires et donner les droits à django
RUN touch logs/critical.log logs/error.log logs/warning.log logs/info.log logs/debug.log logs/access.log \
    && chown django:django logs/*.log

# Créer un utilisateur non-root pour la sécurité en production
RUN groupadd -r django && useradd -r -g django django

# Préparer les seeders au build (validation syntaxique)
RUN python manage.py check --deploy || echo "Warning: Check failed, continuing..."

# Collecte statique et compilation des messages à la création de l'image
RUN python manage.py collectstatic --noinput --settings=monprojet.settings_build || true
RUN python manage.py compilemessages || true

# Définir les permissions pour l'utilisateur django
RUN chown -R django:django /app

# Port exposé
EXPOSE 8000

# Scripts d'entrée pour la production
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown django:django /entrypoint.sh

# Basculer vers l'utilisateur non-root
USER django

# Commande de démarrage en mode production
# Crée automatiquement : admin, journaliste, lecteur avec mot de passe ${DJANGO_ADMIN_PASSWORD}
ENTRYPOINT ["/entrypoint.sh"]
