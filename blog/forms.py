from django import forms
from .models import Article, Comment, Category


class ArticleForm(forms.ModelForm):
    # Champ optionnel pour l'assistance IA
    resume_ia = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Décrivez brièvement le sujet de votre article pour utiliser l\'assistance IA...',
            'class': 'form-control'
        }),
        help_text="Optionnel : Décrivez votre article en quelques phrases pour que l'IA génère automatiquement le titre et le contenu."
    )
    
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'auteur', 'category', 'image']
        widgets = {
            'titre': forms.TextInput(attrs={'placeholder': 'Titre de l\'article', 'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Contenu', 'class': 'form-control'}),
            'auteur': forms.TextInput(attrs={'placeholder': 'Nom de l\'auteur', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si le champ auteur a une valeur initiale, le rendre en lecture seule
        if self.initial.get('auteur'):
            self.fields['auteur'].widget.attrs['readonly'] = True
            self.fields['auteur'].help_text = "Ce champ est automatiquement rempli avec votre nom d'utilisateur."


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['nom', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Nom de la catégorie', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description (optionnel)', 'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['nom', 'email', 'contenu']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre commentaire'}),
        }

class SearchForm(forms.Form):
    """Formulaire de recherche pour les articles"""
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Rechercher des articles...',
            'class': 'form-control',
            'aria-label': 'Recherche'
        }),
        label='',
        required=False
    )
    
    def clean_query(self):
        """Nettoie et valide la requête de recherche"""
        query = self.cleaned_data.get('query', '').strip()
        
        # Limiter la longueur de la requête pour éviter les abus
        if len(query) > 200:
            raise forms.ValidationError("La requête de recherche est trop longue.")
        
        return query

class CommentReplyForm(forms.ModelForm):
    """Formulaire pour répondre à un commentaire (pour les modérateurs)"""
    class Meta:
        model = Comment
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Votre réponse...',
                'required': True
            }),
        }
        labels = {
            'contenu': 'Réponse'
        }