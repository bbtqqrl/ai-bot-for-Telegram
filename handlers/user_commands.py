import asyncio
from aiogram import Router
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from data.db import Database
from keyboards import builders, inline

router = Router()
db = Database()

@router.message(CommandStart())
async def command(message: Message):
    text_language_dict = {
        'ua': "<b>Привіт! 👋</b>\n\nЯ твій AI-асистент. Можу відповідати на запитання, генерувати зображення та працювати з голосовими повідомленнями. 📢🖼\n\nДокладніше – у розділі 'Можливості бота'.\n\n<b>Приємного користування!👨‍💻</b>",
        'eng': "<b>Hello! 👋</b>\n\nI’m your AI assistant. I can answer questions, generate images, and process voice messages. 📢🖼\n\nMore details in 'Bot Capabilities'.\n\n<b>Enjoy your use!👨‍💻</b>",
        'ru': "<b>Привет! 👋</b>\n\nЯ твой AI-ассистент. Отвечаю на вопросы, создаю изображения и работаю с голосовыми сообщениями. 📢🖼\n\nПодробнее в разделе 'Возможности бота'.\n\n<b>Приятного использования!👨‍💻</b>"}

    language = db.get_language(message.chat.id)
    if not language:
        db.insert_user(message.chat.id)
        await message.answer_photo(FSInputFile('photo_2025-03-15_20-09-41.jpg'), "<b>Hello! 👋</b>\n\nI’m your AI assistant. I can answer questions, generate images, and process voice messages. 📢🖼\n\nMore details in 'Bot Capabilities'.\n\n<b>Select a language:</b>", reply_markup=inline.language_button())
    else:
        await message.answer_photo(FSInputFile('photo_2025-03-15_20-09-41.jpg'), text_language_dict[language], reply_markup=builders.main_kb(language))


