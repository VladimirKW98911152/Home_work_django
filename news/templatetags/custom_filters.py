from django import template
import re

register = template.Library()

CENSOR_WORDS = [
    'редиска', 'опущенный', 'шестерка', 'петух',
    'мохнорыл', 'гавно', 'обиженка', 'обиженные',
    'заточка', 'сходняк', 'кидалово', 'шухер',
    'феня', 'мат', 'брань', 'ботать', 'горбатый',
    'горбатого', 'уркаган', 'смотрящий', 'жаргоне'
]

@register.filter()
def censor(value):

    if not isinstance(value, str):
        return value
    
    result = value
    for word in CENSOR_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)

        def replace_match(match):
            matched_word = match.group(0)
            if len(matched_word) > 1:
                return matched_word[0] + '*' * (len(matched_word) - 1)
            return matched_word
        
        result = pattern.sub(replace_match, result)
    
    return result
