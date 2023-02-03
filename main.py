from aiogram import Dispatcher, executor, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from googletrans import Translator

import sqlite3

from Configs import *
from Keyboards import MainButton, GenerateMarkup

STORAGE = MemoryStorage()
BOT = Bot(token=TOKEN)
DB = Dispatcher(BOT, storage=STORAGE)


class Questions(StatesGroup):
    src = State()
    dest = State()
    text = State()


@DB.message_handler(commands=['start', 'help', 'about', 'history'])
async def CommandStart(message: Message):
    if message.text == '/start':
        await message.answer('Вас приветствует бот переводчик', reply_markup=MainButton())

    elif message.text == '/help':
        await message.answer('По вопросам и предложениям обращаться к @shavkatov3', reply_markup=MainButton())

    elif message.text == '/about':
        await message.answer('Данный бот умеет переводить.\n Создан не для коммерческих целей', reply_markup=MainButton())
    elif message.text == '/history':
        ChatId = message.chat.id
        DataBase = sqlite3.connect('DataBase.db')
        cursor = DataBase.cursor()
        cursor.execute('''
        SELECT src, dest, originalText, translatedText FROM history WHERE chatId = ?
        ''', (ChatId, ))
        History = cursor.fetchall()
        History = History[::-1]
        for src, dest, originalText, translatedText in History[:5]:
            await BOT.send_message(ChatId, f'''Вы перевели
С языка: {src}
На язык {dest}
Ваш текст: {originalText}
Бот перевел: {translatedText}''', reply_markup=MainButton())


@DB.message_handler(content_types=['text'])
async def ConfirmMain(message: Message):
    if message.text in ['/start', '/help', '/about', '/history']:
        await CommandStart(message)
    elif message.text == 'Перевести':
        await Questions.src.set()
        await message.answer(f'Выберите язык с которого хотите перевести:', reply_markup=GenerateMarkup())
    else:
        await message.answer('Вы ввели не верную команду. Пожалуйста повторите попытку.', reply_markup=MainButton())


@DB.message_handler(content_types=['text'], state=Questions.src)
async def ConfirmSrc(message: Message, state:FSMContext):
    if message.text in ['/start', '/help', '/about', '/history']:
        await CommandStart(message)
    elif message.text in ['Русский', 'Итальянский', 'Узбекский', 'Немецкий','Английский','Французский']:
        async with state.proxy() as data:
            data['src'] = message.text
        await Questions.next()
        await message.answer(f'Вы выбрали язык для перевода: {message.text}\nВыберите на какой язык перевести:', reply_markup=GenerateMarkup())
    else:
        await state.finish()
        await ConfirmMain(message)


@DB.message_handler(content_types=['text'], state=Questions.dest)
async def ConfirmDest(message: Message, state:FSMContext):
    if message.text in ['/start', '/help', '/about', '/history']:
        await CommandStart(message)
    elif message.text in ['Русский', 'Итальянский', 'Узбекский', 'Немецкий','Английский','Французский']:
        async with state.proxy() as data:
            data['dest'] = message.text
        await Questions.next()
        await message.answer(f'Вы выбрали язык {message.text}\nПожалуйста введите текст для перевода.', reply_markup=ReplyKeyboardRemove())
    else:
        await state.finish()
        await ConfirmMain(message)


@DB.message_handler(content_types=['text'], state=Questions.text)
async def ConfirmText(message: Message, state:FSMContext):
    if message.text in ['/start', '/help', '/about', '/history']:
        await CommandStart(message)
    else:
        async with state.proxy() as data:
            data['text'] = message.text

        src = data['src']
        dest = data['dest']
        text = data['text']
        chatId = message.chat.id
        translator = Translator()
        translatedText = translator.translate(text=text, src=GetKey(src), dest=GetKey(dest)).text
        DataBase = sqlite3.connect('DataBase.db')
        cursor = DataBase.cursor()
        cursor.execute('''
        INSERT INTO history(chatId, src, dest, originalText, translatedText) VALUES (?, ?, ?, ?, ?)
        ''', (chatId, src, dest, text, translatedText))
        DataBase.commit()
        DataBase.close()

        await state.finish()
        await message.answer(translatedText, reply_markup=MainButton())



executor.start_polling(DB)