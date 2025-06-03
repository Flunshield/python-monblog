# Dockerfile pour MonProjet Django Blog (production)
FROM python:3.10-slim

# Variables d'environnement de base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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

# Créer le dossier des logs si besoin
RUN mkdir -p logs

# Collecte statique et compilation des messages à la création de l'image (optionnel)
# RUN python manage.py collectstatic --noinput || true
# RUN python manage.py compilemessages || true

# Port exposé
EXPOSE 8000

# Script d'entrée pour les migrations et démarrage
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Commande de démarrage
ENTRYPOINT ["/entrypoint.sh"]
