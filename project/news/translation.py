from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('post_type', 'title', 'content')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

