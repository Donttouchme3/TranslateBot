TOKEN = '5970931592:AAHIllr6Y60-jgvNqXkIYNdjJ5Xkxeey2RY'

LANGUAGES = {
    'ru': 'Русский',
    'it': 'Итальянский',
    'uz': 'Узбекский',
    'de': 'Немецкий',
    'en': 'Английский',
    'fr': 'Французский'
}

def GetKey(value):
    for k, v in LANGUAGES.items():
        if v == value:
            return k

