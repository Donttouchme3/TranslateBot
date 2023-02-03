from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Configs import LANGUAGES
def MainButton():
    Markup = ReplyKeyboardMarkup(resize_keyboard=True)
    Button = KeyboardButton(text='Перевести', )
    Markup.add(Button)
    return Markup

def GenerateMarkup():
    Markup = ReplyKeyboardMarkup()
    Buttons = []

    for i in LANGUAGES.values():
        btn = KeyboardButton(text=i)
        Buttons.append(i)

    Markup.add(*Buttons)
    return Markup
