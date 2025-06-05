"""
Service pour l'intégration avec l'API Gemini de Google
"""
import logging
import google.generativeai as genai
from django.conf import settings
from typing import Dict, Optional
import json

logger = logging.getLogger('blog.gemini')


class GeminiService:
    """Service pour générer du contenu avec l'API Gemini"""
    
    def __init__(self):
        """Initialise le service Gemini avec la clé API"""        
        try:
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not api_key:
                raise ValueError("GEMINI_API_KEY n'est pas configurée dans les settings")
                
            genai.configure(api_key=api_key)
            # Utilisation du modèle Gemini Flash 2.0 (le plus récent)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            logger.info("Service Gemini initialisé avec succès (modèle: gemini-2.0-flash)")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du service Gemini: {e}")
            raise
    
    def generate_article_content(self, resume: str, langue: str = "fr") -> Dict[str, str]:
        """
        Génère le titre et le contenu d'un article basé sur un résumé
        
        Args:
            resume (str): Le résumé de l'article à créer
            langue (str): La langue de génération (fr, en, es)
            
        Returns:
            Dict[str, str]: Dictionnaire contenant 'titre' et 'contenu'
        """
        try:
            # Construction du prompt selon la langue
            prompts = {
                "fr": f"""
Tu es un journaliste professionnel expérimenté. À partir du résumé suivant, génère un article de blog complet et engageant.

RÉSUMÉ: {resume}

INSTRUCTIONS:
1. Crée un titre accrocheur et informatif (maximum 100 caractères)
2. Écris un article de 300-800 mots bien structuré
3. Utilise un style journalistique professionnel mais accessible
4. Structure l'article avec une introduction, un développement et une conclusion
5. Reste factuel et informatif
6. Utilise des paragraphes courts pour faciliter la lecture

RETOURNE UNIQUEMENT un objet JSON avec cette structure exacte:
{{
    "titre": "Le titre de l'article",
    "contenu": "Le contenu complet de l'article avec des paragraphes séparés par des sauts de ligne"
}}
""",
                "en": f"""
You are an experienced professional journalist. Based on the following summary, generate a complete and engaging blog article.

SUMMARY: {resume}

INSTRUCTIONS:
1. Create a catchy and informative title (maximum 100 characters)
2. Write a 300-800 word well-structured article
3. Use a professional but accessible journalistic style
4. Structure the article with an introduction, development, and conclusion
5. Stay factual and informative
6. Use short paragraphs for easy reading

RETURN ONLY a JSON object with this exact structure:
{{
    "titre": "The article title",
    "contenu": "The complete article content with paragraphs separated by line breaks"
}}
""",
                "es": f"""
Eres un periodista profesional experimentado. Basándote en el siguiente resumen, genera un artículo de blog completo y atractivo.

RESUMEN: {resume}

INSTRUCCIONES:
1. Crea un título llamativo e informativo (máximo 100 caracteres)
2. Escribe un artículo bien estructurado de 300-800 palabras
3. Usa un estilo periodístico profesional pero accesible
4. Estructura el artículo con introducción, desarrollo y conclusión
5. Mantente factual e informativo
6. Usa párrafos cortos para facilitar la lectura

DEVUELVE ÚNICAMENTE un objeto JSON con esta estructura exacta:
{{
    "titre": "El título del artículo",
    "contenu": "El contenido completo del artículo con párrafos separados por saltos de línea"
}}
"""
            }
            
            prompt = prompts.get(langue, prompts["fr"])
            
            logger.info(f"Génération d'article avec Gemini pour le résumé: {resume[:50]}...")
            
            # Génération du contenu
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Réponse vide de l'API Gemini")
            
            # Tentative de parsing JSON
            try:
                # Nettoyer la réponse (supprimer les marqueurs de code si présents)
                content = response.text.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                content = content.strip()
                
                result = json.loads(content)
                
                # Validation des champs requis
                if 'titre' not in result or 'contenu' not in result:
                    raise ValueError("Format de réponse invalide")
                
                # Nettoyage et validation
                titre = str(result['titre']).strip()
                contenu = str(result['contenu']).strip()
                
                if not titre or not contenu:
                    raise ValueError("Titre ou contenu vide")
                
                # Limitation de la taille du titre
                if len(titre) > 200:
                    titre = titre[:197] + "..."
                
                logger.info(f"Article généré avec succès - Titre: {titre[:50]}...")
                
                return {
                    'titre': titre,
                    'contenu': contenu
                }
                
            except json.JSONDecodeError as e:
                logger.error(f"Erreur de parsing JSON: {e}")
                logger.error(f"Réponse brute: {response.text}")
                
                # Fallback: tentative d'extraction manuelle
                return self._extract_manual_content(response.text, resume)
        
        except Exception as e:
            logger.error(f"Erreur lors de la génération avec Gemini: {e}")
            raise
    
    def _extract_manual_content(self, raw_response: str, resume: str) -> Dict[str, str]:
        """
        Extraction manuelle en cas d'échec du parsing JSON
        """
        try:
            # Génération de fallback simple
            lines = raw_response.split('\n')
            
            # Chercher une ligne qui ressemble à un titre
            titre = None
            for line in lines[:10]:  # Chercher dans les 10 premières lignes
                line = line.strip()
                if line and len(line) < 150 and not line.startswith('{'):
                    titre = line.strip('"').strip("'").strip()
                    break
            
            if not titre:
                titre = f"Article sur {resume[:50]}..."
            
            # Utiliser tout le contenu comme contenu de l'article
            contenu = raw_response.strip()
            
            logger.warning("Utilisation du mode fallback pour l'extraction de contenu")
            
            return {
                'titre': titre,
                'contenu': contenu
            }
            
        except Exception as e:
            logger.error(f"Erreur dans l'extraction manuelle: {e}")
            # Dernier recours
            return {
                'titre': f"Article généré automatiquement",
                'contenu': f"Contenu basé sur: {resume}\n\n{raw_response}"
            }
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à l'API Gemini
        
        Returns:
            bool: True si la connexion fonctionne
        """
        try:
            response = self.model.generate_content("Test de connexion. Réponds juste 'OK'.")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Test de connexion Gemini échoué: {e}")
            return False
