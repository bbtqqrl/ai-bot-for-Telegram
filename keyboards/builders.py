from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from data.bot_func import language_voices
def main_kb(language):
    items_language_dict = {
        'ua':['Новий чат💬', 'Генерація зображень🖼', 'Синтезатор мовлення🗣', 'Профіль📋', 'Можливості бота🤖', 'Про мене!😊'],
        'eng':['New chat💬', 'Image generation🖼', 'Speech synthesizer🗣', 'Profile📋', 'Bot capabilities🤖', 'About me!😊'],
        'ru':['Новый чат💬', 'Генерация изображений🖼', 'Синтезатор речи🗣', 'Профиль📋', 'Возможности бота🤖', 'Обо мне!😊']
    }
    items = items_language_dict[language]
    builder = ReplyKeyboardBuilder()
    [builder.add(KeyboardButton(text = item)) for item in items]
    builder.adjust(3, 3)
    return builder.as_markup(resize_keyboard=True)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def create_language_keyboard(language, page: int = 0, prefix = 'synthesis'):
    text_language_dict = {
        'eng': ['⬅️ Back', 'Next ➡️'],
        'ua': ['⬅️ Назад', 'Далі ➡️'],
        'ru': ['⬅️ Назад', 'Дальше ➡️']
    }

    languages = list(language_voices.keys())
    start = page * 10
    end = start + 10
    languages_page = languages[start:end]

    keyboard = InlineKeyboardBuilder()

    # Додаємо кнопки мов (по 2 в ряд)
    buttons = [InlineKeyboardButton(text=lang, callback_data=f"lang_{prefix}|{lang}") for lang in languages_page]
    keyboard.add(*buttons)
    keyboard.adjust(2)  # Розміщуємо по 2 кнопки в ряд

    # Додаємо кнопки навігації
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text=text_language_dict[language][0], callback_data=f"page_{prefix}|{page-1}"))
    if page < 4:
        nav_buttons.append(InlineKeyboardButton(text=text_language_dict[language][1], callback_data=f"page_{prefix}|{page+1}"))

    if nav_buttons:
        keyboard.row(*nav_buttons)  # Додаємо кнопки в один ряд

    return keyboard.as_markup()


def create_voice_keyboard(voices):
    languages = list(language_voices.keys())
    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=voice, callback_data=f"voice|{voice}") for voice in voices]
    keyboard.add(*buttons)
    keyboard.adjust(1) 

    return keyboard.as_markup()