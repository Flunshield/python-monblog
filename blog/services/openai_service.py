"""
Service pour l'intégration avec l'API OpenAI (GPT et DALL-E)
"""
import logging
import requests
import os
from typing import Dict, Optional
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import uuid

logger = logging.getLogger('blog.openai')


class OpenAIService:
    """Service pour générer du contenu et des images avec OpenAI"""
    
    def __init__(self):
        """Initialise le service OpenAI avec la clé API"""
        try:
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            if not api_key:
                raise ValueError("OPENAI_API_KEY n'est pas configurée dans les settings")
                
            self.api_key = api_key
            self.headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            logger.info("Service OpenAI initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du service OpenAI: {e}")
            raise
    
    def generate_image_description(self, query: str, langue: str = "fr") -> Optional[str]:
        """
        Génère une description d'image avec GPT
        
        Args:
            query (str): Le sujet de l'article
            langue (str): La langue de génération (fr, en, es)
            
        Returns:
            Optional[str]: Description de l'image générée
        """
        try:
            # Construction du prompt selon la langue
            prompts = {
                "fr": f"Génère une description d'image courte et précise (maximum 100 mots) pour illustrer ce sujet d'article : {query}. La description doit être visuelle, descriptive et adaptée à un article de blog professionnel.",
                "en": f"Generate a short and precise image description (maximum 100 words) to illustrate this article topic: {query}. The description should be visual, descriptive and suitable for a professional blog article.",
                "es": f"Genera una descripción de imagen corta y precisa (máximo 100 palabras) para ilustrar este tema de artículo: {query}. La descripción debe ser visual, descriptiva y adecuada para un artículo de blog profesional."
            }
            
            image_prompt = prompts.get(langue, prompts["fr"])
            
            logger.info(f"Génération de description d'image pour: {query[:50]}...")
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=self.headers,
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': image_prompt}],
                    'max_tokens': 150,
                    'temperature': 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                description = result['choices'][0]['message']['content'].strip()
                logger.info("Description d'image générée avec succès")
                return description
            else:
                logger.error(f"Erreur API GPT: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération de description d'image: {e}")
            return None
    
    def generate_image_with_dalle(self, description: str) -> Optional[str]:
        """
        Génère une image avec DALL-E
        
        Args:
            description (str): Description de l'image à générer
            
        Returns:
            Optional[str]: URL relative de l'image sauvegardée
        """
        try:
            logger.info("Génération d'image avec DALL-E...")
            
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=self.headers,
                json={
                    'prompt': description,
                    'n': 1,
                    'size': '512x512',
                    'response_format': 'url'
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                
                # Télécharger et sauvegarder l'image
                image_path = self._download_and_save_image(image_url)
                if image_path:
                    logger.info(f"Image générée et sauvegardée: {image_path}")
                    return image_path
                else:
                    logger.error("Échec de la sauvegarde de l'image")
                    return None
            else:
                logger.error(f"Erreur API DALL-E: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération d'image DALL-E: {e}")
            return None
    
    def _download_and_save_image(self, image_url: str) -> Optional[str]:
        """
        Télécharge et sauvegarde une image depuis une URL
        
        Args:
            image_url (str): URL de l'image à télécharger
            
        Returns:
            Optional[str]: Chemin relatif de l'image sauvegardée
        """
        try:
            # Télécharger l'image
            response = requests.get(image_url, timeout=30)
            if response.status_code == 200:
                # Générer un nom de fichier unique
                filename = f"ai_generated_{uuid.uuid4().hex[:8]}.png"
                file_path = f"articles/{filename}"
                
                # Sauvegarder dans le système de fichiers Django
                saved_path = default_storage.save(file_path, ContentFile(response.content))
                
                return saved_path
            else:
                logger.error(f"Échec du téléchargement d'image: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde d'image: {e}")
            return None
    
    def generate_image_for_article(self, query: str, langue: str = "fr") -> Optional[str]:
        """
        Génère une image complète pour un article (description + génération)
        
        Args:
            query (str): Le sujet de l'article
            langue (str): La langue de génération
            
        Returns:
            Optional[str]: Chemin relatif de l'image générée
        """
        try:
            # Étape 1: Générer la description
            description = self.generate_image_description(query, langue)
            if not description:
                return None
            
            # Étape 2: Générer l'image
            image_path = self.generate_image_with_dalle(description)
            return image_path
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération complète d'image: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API OpenAI
        
        Returns:
            bool: True si la connexion fonctionne
        """
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=self.headers,
                json={
                    'model': 'gpt-3.5-turbo',
                    'messages': [{'role': 'user', 'content': 'Test de connexion. Réponds juste "OK".'}],
                    'max_tokens': 5
                }
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Test de connexion OpenAI échoué: {e}")
            return False
