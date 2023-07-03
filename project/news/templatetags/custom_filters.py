from django import template

register = template.Library()

obscene_words = ['козел', 'редиска']
@register.filter()

def censor(word):
    if isinstance(word, str):
        for i in word.split():
            if i in obscene_words:
                word = word.lower().replace(i, i[0] + '*' * len(i))
    else:
        raise ValueError ('Должна быть строка')
    return word