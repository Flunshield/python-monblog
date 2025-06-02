from django import forms
from .models import Article, Comment, Category


class ArticleForm(forms.ModelForm):
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