# Dockerfile pour MonProjet Django Blog (production)
FROM python:3.10-slim

# Variables d'environnement de base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_DEBUG False
ENV DJANGO_ADMIN_PASSWORD ProdAdmin2024!

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

# Préparer les seeders au build (validation syntaxique)
RUN python manage.py check --deploy || echo "Warning: Check failed, continuing..."

# Collecte statique et compilation des messages à la création de l'image
RUN python manage.py collectstatic --noinput --settings=monprojet.settings_build || true
RUN python manage.py compilemessages || true

# Port exposé
EXPOSE 8000

# Scripts d'entrée pour les migrations, seeding et démarrage
COPY entrypoint.sh /entrypoint.sh
COPY entrypoint-with-seeding.sh /entrypoint-with-seeding.sh
RUN chmod +x /entrypoint.sh /entrypoint-with-seeding.sh

# Commande de démarrage
ENTRYPOINT ["/entrypoint-with-seeding.sh"]
