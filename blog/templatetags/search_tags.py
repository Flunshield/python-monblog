from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html
import re

register = template.Library()

@register.filter
def highlight_search(text, search_terms):
    """
    Template filter pour surligner les termes de recherche dans un texte
    Usage: {{ text|highlight_search:search_terms }}
    """
    if not search_terms or not text:
        return text
    
    # Si search_terms est une chaîne, la convertir en liste
    if isinstance(search_terms, str):
        terms = [term.strip() for term in search_terms.split() if term.strip()]
    else:
        terms = [str(term).strip() for term in search_terms if str(term).strip()]
    
    highlighted_text = str(text)
    
    for term in terms:
        if term:
            # Utiliser une regex insensible à la casse pour remplacer
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            highlighted_text = pattern.sub(
                lambda m: f'<mark class="search-highlight">{m.group(0)}</mark>',
                highlighted_text
            )
    
    return mark_safe(highlighted_text)


@register.simple_tag
def search_excerpt(content, search_terms, max_length=250):
    """
    Crée un extrait de texte centré autour des termes de recherche
    Usage: {% search_excerpt article.contenu search_terms 250 %}
    """
    if not search_terms or not content:
        return content[:max_length] + '...' if len(content) > max_length else content
    
    # Si search_terms est une chaîne, la convertir en liste
    if isinstance(search_terms, str):
        terms = [term.strip().lower() for term in search_terms.split() if term.strip()]
    else:
        terms = [str(term).strip().lower() for term in search_terms if str(term).strip()]
    
    content_lower = content.lower()
    
    # Trouver la première occurrence d'un terme de recherche
    first_match_pos = len(content)
    for term in terms:
        if term:
            pos = content_lower.find(term)
            if pos != -1 and pos < first_match_pos:
                first_match_pos = pos
    
    # Si aucun terme trouvé, retourner le début du texte
    if first_match_pos == len(content):
        excerpt = content[:max_length]
        if len(content) > max_length:
            excerpt += '...'
        return excerpt
    
    # Créer un extrait centré sur la première occurrence
    start = max(0, first_match_pos - 50)
    end = min(len(content), start + max_length)
    
    # Ajuster le début pour éviter de couper au milieu d'un mot
    if start > 0:
        space_pos = content.find(' ', start)
        if space_pos != -1 and space_pos < start + 20:
            start = space_pos + 1
    
    # Ajuster la fin pour éviter de couper au milieu d'un mot
    if end < len(content):
        space_pos = content.rfind(' ', start, end)
        if space_pos != -1 and space_pos > end - 20:
            end = space_pos
    
    excerpt = content[start:end]
    
    # Ajouter des points de suspension si nécessaire
    if start > 0:
        excerpt = '...' + excerpt
    if end < len(content):
        excerpt = excerpt + '...'
    
    return excerpt


@register.inclusion_tag('blog/search_form.html', takes_context=True)
def search_form(context, placeholder="Rechercher..."):
    """
    Tag d'inclusion pour afficher le formulaire de recherche
    Usage: {% search_form "Rechercher des articles..." %}
    """
    request = context.get('request')
    current_query = request.GET.get('query', '') if request else ''
    
    return {
        'current_query': current_query,
        'placeholder': placeholder,
        'request': request,
    }


@register.simple_tag
def search_stats(total_results, query):
    """
    Génère le texte des statistiques de recherche
    Usage: {% search_stats total_results query %}
    """
    if not query:
        return ""
    
    if total_results == 0:
        return format_html(
            'Aucun résultat trouvé pour "<strong>{}</strong>"',
            query
        )
    elif total_results == 1:
        return format_html(
            '1 résultat trouvé pour "<strong>{}</strong>"',
            query
        )
    else:
        return format_html(
            '{} résultats trouvés pour "<strong>{}</strong>"',
            total_results,
            query
        )
