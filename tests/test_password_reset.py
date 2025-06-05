import os
import django
import pytest
from django.core import mail
from django.contrib.auth import get_user_model
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monprojet.settings')
django.setup()

@pytest.mark.django_db
def test_password_reset_view():
    """Test que le formulaire password-reset envoie bien un email à l'adresse saisie"""
    User = get_user_model()
    test_email = "contact@jbertrand.fr"
    # Créer un utilisateur avec cet email
    user = User.objects.create_user(username="testuser", email=test_email, password="testpass123")

    client = Client()
    response = client.post("/fr/password-reset/", {"email": test_email})

    # Vérifier la redirection (Django redirige après succès)
    assert response.status_code in (302, 200)

    # Vérifier qu'un email a été envoyé
    assert len(mail.outbox) == 1, "Aucun email envoyé !"
    assert test_email in mail.outbox[0].to, f"L'email n'a pas été envoyé à {test_email}"
    print("✓ Email envoyé à l'adresse saisie dans le formulaire !")
