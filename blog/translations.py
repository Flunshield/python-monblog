from modeltranslation.translator import translator, TranslationOptions
from .models import Article, Category

class ArticleTranslationOptions(TranslationOptions):
    fields = ('titre', 'contenu',)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('nom', 'description',)

translator.register(Article, ArticleTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
