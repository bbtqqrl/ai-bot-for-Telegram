from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def language_button():
    buttons = [
        [InlineKeyboardButton(text='English', callback_data='eng')],
        [InlineKeyboardButton(text='Українська', callback_data='ua')],
        [InlineKeyboardButton(text='Русский', callback_data='ru')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def generate_button(language, prefix = ''):
    buttons = {
        'ua': [InlineKeyboardButton(text='Так✅', callback_data=f'yes{prefix}'),InlineKeyboardButton(text=f'Ні❌', callback_data=f'no{prefix}')],
        'eng': [InlineKeyboardButton(text='Yes✅', callback_data=f'yes{prefix}'),InlineKeyboardButton(text=f'No❌', callback_data=f'no{prefix}')],
        'ru': [InlineKeyboardButton(text='Да✅', callback_data=f'yes{prefix}'),InlineKeyboardButton(text=f'Нет❌', callback_data=f'no{prefix}')]
        
        }
    return InlineKeyboardMarkup(inline_keyboard=[buttons[language]])


def settings_button(language):
    buttons = {
        'ua': [[InlineKeyboardButton(text='Налаштування синтезу 🔊', callback_data='synthesis_settings')], [InlineKeyboardButton(text='Мова вашого голосу 🌐', callback_data='voice_language_settings')], [InlineKeyboardButton(text='Налаштування генерації 🖼', callback_data='generation_settings')], [InlineKeyboardButton(text='Змінити мову бота 🤖', callback_data='language_settings')]],
        'ru': [[InlineKeyboardButton(text='Настройки синтеза 🔊', callback_data='synthesis_settings')],  [InlineKeyboardButton(text='Язык вашего голоса 🌐', callback_data='voice_language_settings')], [InlineKeyboardButton(text='Настройка генерации 🖼', callback_data='generation_settings')],  [InlineKeyboardButton(text='Изменить язык бота 🤖', callback_data='language_settings')]],  
        'eng': [[InlineKeyboardButton(text='Synthesis Settings 🔊', callback_data='synthesis_settings')],  [InlineKeyboardButton(text='Your Voice Language 🌐', callback_data='voice_language_settings')], [InlineKeyboardButton(text='Generation settings 🖼', callback_data='generation_settings')],  [InlineKeyboardButton(text='Change Bot Language 🤖', callback_data='language_settings')]]}
    return InlineKeyboardMarkup(inline_keyboard=buttons[language])

def profile_settings_button(language):
    buttons = {
        'ua': [InlineKeyboardButton(text='Налаштування ⚙️', callback_data='settings')],
        'eng': [InlineKeyboardButton(text='Settings ⚙️', callback_data='settings')],
        'ru': [InlineKeyboardButton(text='Настройки ⚙️', callback_data='settings')]
        
        }
    return InlineKeyboardMarkup(inline_keyboard=[buttons[language]])


def synthesis_pitch_button(language, language_code, voice_name):
    buttons = {
        'ua': [[InlineKeyboardButton(text='🔺 Дуже високий', callback_data=f"pitch|{language_code}|{voice_name}|10")],
               [InlineKeyboardButton(text='🔺 Високий', callback_data=f"pitch|{language_code}|{voice_name}|5")], 
               [InlineKeyboardButton(text='♦️ Середній', callback_data=f"pitch|{language_code}|{voice_name}|0")],
               [InlineKeyboardButton(text='🔻 Низький', callback_data=f"pitch|{language_code}|{voice_name}|-5")],
               [InlineKeyboardButton(text='🔻 Дуже низький', callback_data=f"pitch|{language_code}|{voice_name}|-10")]
               ],
        'eng': [[InlineKeyboardButton(text='🔺 Very high', callback_data=f"pitch|{language_code}|{voice_name}|10")],
               [InlineKeyboardButton(text='🔺 High', callback_data=f"pitch|{language_code}|{voice_name}|5")], 
               [InlineKeyboardButton(text='♦️ Medium', callback_data=f"pitch|{language_code}|{voice_name}|0")],
               [InlineKeyboardButton(text='🔻 Low', callback_data=f"pitch|{language_code}|{voice_name}|-5")],
               [InlineKeyboardButton(text='🔻 Very low', callback_data=f"pitch|{language_code}|{voice_name}|-10")]
               ],
        'ru': [[InlineKeyboardButton(text='🔺 Очень высокий', callback_data=f"pitch|{language_code}|{voice_name}|10")],
               [InlineKeyboardButton(text='🔺 Высокий', callback_data=f"pitch|{language_code}|{voice_name}|5")], 
               [InlineKeyboardButton(text='♦️ Средний', callback_data=f"pitch|{language_code}|{voice_name}|0")],
               [InlineKeyboardButton(text='🔻 Низкий', callback_data=f"pitch|{language_code}|{voice_name}|-5")],
               [InlineKeyboardButton(text='🔻 Очень низкий', callback_data=f"pitch|{language_code}|{voice_name}|-10")]]}
    return InlineKeyboardMarkup(inline_keyboard=buttons[language])

def synthesis_rate_button(language, language_code, voice_name, pitch):
    buttons = {
        'ua': [[InlineKeyboardButton(text='🔺 Дуже швидка', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1.40")],
               [InlineKeyboardButton(text='🔺 Швидшко', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1.20")], 
               [InlineKeyboardButton(text='♦️ Середня', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1")],
               [InlineKeyboardButton(text='🔻 Повільно', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|0.85")],
               [InlineKeyboardButton(text='🔻 Дуже повільно', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|0.70")]
               ],
        'eng': [[InlineKeyboardButton(text='🔺 Very quickly', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1.40")],
               [InlineKeyboardButton(text='🔺 Quickly', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1.20")], 
               [InlineKeyboardButton(text='♦️ Medium', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1")],
               [InlineKeyboardButton(text='🔻 Slowly', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|0.85")],
               [InlineKeyboardButton(text='🔻 Very slowly', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|0.70")]
               ],
        'ru': [[InlineKeyboardButton(text='🔺 Очень быстро', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1.40")],
               [InlineKeyboardButton(text='🔺 Быстро', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1.20")], 
               [InlineKeyboardButton(text='♦️ Среднее', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|1")],
               [InlineKeyboardButton(text='🔻 Медленно', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|0.85")],
               [InlineKeyboardButton(text='🔻 Очень низкий', callback_data=f"rate|{language_code}|{voice_name}|{pitch}|0.70")]]}
    return InlineKeyboardMarkup(inline_keyboard=buttons[language])
