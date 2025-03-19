from aiogram import Router
import aiofiles, aiohttp, os
from aiogram import F, Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data import bot_func
from pydub import AudioSegment
from data.db import Database
from keyboards import builders, inline
from main import bot
from data.bot_func import language_voices

router = Router()
db = Database()

class ImageGenState(StatesGroup):
    waiting_for_prompt = State() 

class SpeechSynthState(StatesGroup):
    waiting_for_synthesis_text = State() 

class VoiceRecognition(StatesGroup):
    waiting_for_language = State()

class VoiceLanguageInGeneration(StatesGroup):
    waiting_for_language_in_generation = State()

@router.message(F.text.in_(["Синтезатор мовлення🗣", "Speech synthesizer🗣", "Синтезатор речи🗣"]))
async def market_status(message: Message,  state: FSMContext):
    synthesis_data = db.get_synthesis_settings(message.chat.id)
    language = db.get_language(message.chat.id)
    syntesis_language = await bot_func.get_language_name_by_code(synthesis_data["language_code"])
    voice_name = synthesis_data["voice_name"]
    pitch = synthesis_data["pitch"]
    speaking_rate = synthesis_data["speaking_rate"]
    text_language_dict = {
        "eng": f"🔊 This function allows you to synthesize speech in different languages, with various voices and pitch levels!\n\n<b>Synthesis settings can be changed in Profile.</b>\n\n🎛 Your current settings:\n<b>Language:</b> {syntesis_language}\n<b>Voice:</b> {voice_name}\n<b>Pitch:</b> {pitch}\n<b>Speaking rate:</b> {speaking_rate}\n\n✍️ Simply type the text you want to convert to speech in the chat!",
        "ru": f"🔊 Эта функция позволяет синтезировать речь на разных языках, с различными голосами и высотой тона!\n\n<b>Настройки синтеза можно изменить в Профиле.</b>\n\n🎛 Ваши текущие настройки:\n<b>Язык:</b> {syntesis_language}\n<b>Голос:</b> {voice_name}\n<b>Высота голоса:</b> {pitch}\n<b>Скорость речи:</b> {speaking_rate}\n\n✍️ Просто напишите в чат текст, который хотите преобразовать в речь!",
        "ua": f"🔊 Ця функція дозволяє синтезувати мовлення різними мовами, голосами та з регульованою висотою!\n\n<b>Налаштування синтезу можна змінити у Профілі.</b>\n\n🎛 Ваші поточні налаштування:\n<b>Мова:</b> {syntesis_language}\n<b>Голос:</b> {voice_name}\n<b>Висота голосу:</b> {pitch}\n<b>Швидкість мовлення:</b> {speaking_rate}\n\n✍️ Напишіть у чат текст, який хочете перетворити на мовлення!"}

    await message.answer(text_language_dict[language])
    await state.set_state(SpeechSynthState.waiting_for_synthesis_text)


@router.message(F.text.in_(["Генерація зображень🖼", "Image generation🖼", "Генерация изображений🖼"]))
async def send_and_delete_image(message: Message, state: FSMContext):
    language_dict = {
    "ua": "Введіть текстовий опис для генерації зображення ✍️⤵️\n\nВаш запит буде автоматично оптимізовано за допомогою штучного інтелекту, щоб отримане зображення було якомога точнішим і якіснішим.\n\nЗа бажанням ви можете змінити цей параметр у налаштуваннях профілю.",
    
    "eng": "Enter a text description for image generation ✍️⤵️\n\nYour prompt will be automatically optimized using artificial intelligence to ensure the generated image is as accurate and high-quality as possible.\n\nIf you prefer, you can change this setting in your profile settings.",
    
    "ru": "Введите текстовое описание для генерации изображения ✍️⤵️\n\nВаш запрос будет автоматически оптимизирован с помощью искусственного интеллекта, чтобы созданное изображение было как можно точнее и качественнее.\n\nПри желании вы можете изменить этот параметр в настройках профиля."}

    language_dict_false = {
    "ua": "Введіть текстовий опис для генерації зображення ✍️⤵️\n\nВаш запит не буде оптимізовано за допомогою штучного інтелекту.\n\nЗа бажанням ви можете змінити цей параметр у налаштуваннях профілю.",
    
    "eng": "Enter a text description for image generation ✍️⤵️\n\nYour prompt will be not optimized using ai\n\nIf you prefer, you can change this setting in your profile settings.",
    
    "ru": "Введите текстовое описание для генерации изображения ✍️⤵️\n\nВаш запрос не будет оптимизирован с помощью искусственного интеллекта\n\nПри желании вы можете изменить этот параметр в настройках профиля."}

    language = db.get_language(message.chat.id)
    prompt_bool = db.get_ai_prompt_bool(message.chat.id)
    if not prompt_bool:
        language_dict = language_dict_false
    await message.answer_photo(FSInputFile('photo_2025-03-16_18-37-24.jpg'), language_dict[language])
    await state.set_state(ImageGenState.waiting_for_prompt)

@router.message(F.text.in_(["Можливості бота🤖", "Bot capabilities🤖", "Возможности бота🤖"]))
async def market_status(message: Message, state: FSMContext):
    await state.clear()
    text_language_dict = {
        'ua': "<b>🔹 Можливості бота:</b>\n\n🧠 <b>Велика LLM-модель з пам’яттю</b> – бот аналізує контекст розмови та дає осмислені відповіді.\n\n🎙 <b>Голосові повідомлення</b> – можеш надсилати голосові замість тексту, ШІ їх розпізнає та передасть в LLM.\n\n🖼 <b>Генерація зображень</b> – бот створить унікальні картинки на основі твого опису.\n\n🔊 <b>Синтезатор голосу</b> – бот може відповідати голосом та вручну синтезувати голос, а ти можеш змінювати його налаштування в профілі.\n\n⚙️ <b>Налаштування:</b> можна змінити мову бота, мову голосових повідомлень для аналізу та параметри синтезатора голосу.\n\n📖 <b>Детальніше:</b> <a href='https://github.com/your_repo'>GitHub README</a>",
        'eng': "<b>🔹 Bot Features:</b>\n\n🧠 <b>Powerful LLM model with memory</b> – the bot understands context and gives meaningful responses.\n\n🎙 <b>Voice messages</b> – send voice instead of text, AI will recognize it and process it in the LLM.\n\n🖼 <b>Image generation</b> – create unique images based on your description.\n\n🔊 <b>Voice synthesizer</b> – the bot can respond with voice and manually synthesize voice, and you can customize its settings in your profile.\n\n⚙️ <b>Settings:</b> change the bot's language, set the language for voice message analysis, and adjust voice synthesizer parameters.\n\n📖 <b>More details:</b> <a href='https://github.com/your_repo'>GitHub README</a>",
        'ru': "<b>🔹 Возможности бота:</b>\n\n🧠 <b>Мощная LLM-модель с памятью</b> – бот анализирует контекст беседы и дает осмысленные ответы.\n\n🎙 <b>Голосовые сообщения</b> – отправляй голос вместо текста, ИИ распознает его и передаст в LLM.\n\n🖼 <b>Генерация изображений</b> – бот создаст уникальные картинки по твоему описанию.\n\n🔊 <b>Синтезатор голоса</b> – бот может отвечать голосом и вручную синтезировать голос, а ты можешь настроить параметры синтезатора в профиле.\n\n⚙️ <b>Настройки:</b> можно изменить язык бота, язык голосовых сообщений для анализа и параметры синтезатора голоса.\n\n📖 <b>Подробнее:</b> <a href='https://github.com/your_repo'>GitHub README</a>"}
    await message.answer_photo(FSInputFile('photo_2025-03-15_19-35-44.jpg'), text_language_dict[db.get_language(message.chat.id)])

@router.message(F.text.in_(["Новий чат💬", "New chat💬", "Новый чат💬"]))
async def market_status(message: Message, state: FSMContext):
    await state.clear()
    text_language_dict = {
        'ua': 'Привіт , чим я можу вам допомогти?',
        'eng': 'Hello, how can I help you?',
        'ru': 'Привет, чем я могу вам помочь?'
    }
    db.delete_history(message.chat.id)
    await message.answer(text_language_dict[db.get_language(message.chat.id)])

@router.message(F.text.in_(["Profile📋", "Профіль📋", "Профиль📋"]))
async def market_status(message: Message, state: FSMContext):
    await state.clear()
    data = db.get_user_data(message.chat.id)
    language = db.get_language(message.chat.id)
    language_name = await bot_func.get_language_name_by_code(db.get_voice_language(message.chat.id))
    text_language_dict = {
        'ua': f'<b>Ваш профіль </b>📋⤵️\n\n🆔 : <code>{message.chat.id}</code>\n📍 Юзернейм : {message.from_user.first_name}\n\n📝 <b>Відправлено повідомлень</b> : {data[0]}\n🔉 <b>Відправлено аудіо</b> : {data[1]}\n🎨 <b>Згенеровано зображень</b> : {data[2]}\n\n🌐 <b>Мова боту</b> : {language}\n🗣 <b>Мова ваших голосових повідомлень </b> : {language_name}',
        'eng': f'<b>Your Profile </b>📋⤵️\n\n🆔 : <code>{message.chat.id}</code>\n📍 Username : {message.from_user.first_name}\n\n📝 <b>Messages sent</b> : {data[0]}\n🔉 <b>Voice messages sent</b> : {data[1]}\n🎨 <b>Images generated</b> : {data[2]}\n\n🌐 <b>Bot language</b>: {language}\n🗣 <b>Your voice message language</b>: {language_name}',
        'ru': f'<b>Ваш профиль </b>📋⤵️\n\n🆔 : <code>{message.chat.id}</code>\n📍 Юзернейм : {message.from_user.first_name}\n\n📝 <b>Отправлено сообщений</b> : {data[0]}\n🔉 <b>Отправлено аудиосообщений</b> : {data[1]}\n🎨 <b>Сгенерировано изображений</b> : {data[2]}\n\n🌐 <b>Язык бота</b>: {language}\n🗣 <b>Язык ваших голосовых сообщений</b>: {language_name}'}

    await message.answer(text_language_dict[language], reply_markup=inline.profile_settings_button(language))


@router.message(F.text.in_(["About me!😊", "Про мене!😊", "Обо мне!😊"]))
async def market_status(message: Message, state: FSMContext):
    await state.clear()
    text_language_dict = {
        'ua': (
            f"<b>Про мене!</b>\n\n"
            f"Привіт! Я <b>Максим Горельчик</b>, 18-річний Python-розробник, який захоплюється створенням розумних і ефективних рішень. Я <b>люблю</b> вирішувати складні завдання, оптимізувати процеси та постійно вдосконалювати свої навички.\n\n"
            f"Я <b>відкритий</b> до нових ідей та можливостей, будь то цікавий проєкт, співпраця чи фріланс. Якщо у вас є щось цікаве—<b>зв’яжіться зі мною!</b> 🚀\n\n"
            f"Цей бот побудований на async <code><b>Python</b></code> і <code><b>Aiogram</b></code>, інтегрує <code><b>PostgreSQL</b></code> та отримує ринкові дані в реальному часі за допомогою різних <code><b>API</b></code>. Це лише один із багатьох проєктів у моєму портфоліо.\n\n"
            f"🔗 <a href='https://github.com/bbtqqrl'><b>GitHub</b></a>\n"
            f"🔗 <a href='https://www.linkedin.com/in/bbtqqrl/'><b>LinkedIn</b></a>"
        ),
        'eng': (
            f"<b>About Me!</b>\n\n"
            f"Hi! I’m <b>Maksym Horelchyk</b>, an 18-year-old Python developer passionate about creating smart and efficient solutions. I <b>enjoy</b> tackling complex problems, optimizing processes, and continuously improving my skills.\n\n"
            f"I’m <b>always open</b> to new ideas and opportunities, whether it’s an interesting project, collaboration, or freelance work. If you have something exciting in mind—<b>let’s connect!</b> 🚀\n\n"
            f"This bot is built with async <code><b>Python</b></code> and <code><b>Aiogram</b></code>, integrates <code><b>PostgreSQL</b></code>, and fetches real-time market data using various <code><b>APIs</b></code>. It’s just one of many projects in my growing portfolio.\n\n"
            f"🔗 <a href='https://github.com/bbtqqrl'><b>GitHub</b></a>\n"
            f"🔗 <a href='https://www.linkedin.com/in/bbtqqrl/'><b>LinkedIn</b></a>"
        ),
        'ru': (
            f"<b>Обо мне!</b>\n\n"
            f"Привет! Я <b>Максим Горельчик</b>, 18-летний Python-разработчик, увлечённый созданием умных и эффективных решений. Я <b>люблю</b> решать сложные задачи, оптимизировать процессы и постоянно совершенствовать свои навыки.\n\n"
            f"Я <b>открыт</b> для новых идей и возможностей, будь то интересный проект, сотрудничество или фриланс. Если у вас есть что-то интересное—<b>свяжитесь со мной!</b> 🚀\n\n"
            f"Этот бот построен на async <code><b>Python</b></code> и <code><b>Aiogram</b></code>, интегрирует <code><b>PostgreSQL</b></code> и получает рыночные данные в реальном времени с помощью различных <code><b>API</b></code>. Это всего лишь один из многих проектов в моем портфолио.\n\n"
            f"🔗 <a href='https://github.com/bbtqqrl'><b>GitHub</b></a>\n"
            f"🔗 <a href='https://www.linkedin.com/in/bbtqqrl/'><b>LinkedIn</b></a>"
        )
    }

    await message.answer(text_language_dict[db.get_language(message.chat.id)])

@router.message(SpeechSynthState.waiting_for_synthesis_text)
async def process_prompt(message: Message, state: FSMContext):
    settings_dict = db.get_synthesis_settings(message.chat.id)
    language, voice, pitch, speaking_rate = settings_dict["language_code"], settings_dict["voice_name"], settings_dict["pitch"], settings_dict["speaking_rate"]
    language_dict = {
        'ua': 'Завантаження аудіо 📌...',
        'eng': 'Loading audio 📌...',
        'ru': 'Загрузка аудио 📌...'}
    await message.answer(language_dict[db.get_language(message.chat.id)])
    await state.clear()
    wav_path = await bot_func.speech_synthesis(message.text, language, voice, pitch, speaking_rate)
    if wav_path:
        try:
            await message.answer_document(FSInputFile(wav_path))
        except Exception as e:
            print(e)
        finally:
            os.remove(wav_path)
    else:
        await message.answer("Something get wrong...")


@router.message(ImageGenState.waiting_for_prompt)
async def process_prompt(message: Message, state: FSMContext):
    await state.clear()
    language = db.get_language(message.chat.id)
    language_dict = {
        'ua': ['Ось ваш промт ⤵️', 'Генерувати зображення?'],
        'eng': ['Here is your prompt ⤵️', 'Generate image?'],
        'ru': ['Вот ваш промт ⤵️', 'Генерировать изображение?']}
    if message.text:
        prompt = message.text
    elif message.voice:
        db.update_count_voice_message(message.chat.id)
        file = await bot.get_file(message.voice.file_id)
        file_path = f"{file.file_id}.ogg"
        await bot.download_file(file.file_path, file_path)
        voice_language = db.get_voice_language(message.chat.id)
        if voice_language:
            promt = await bot_func.audio_transcription(file_path, voice_language) # Не зрозуміло якк мова , треба використати if elif db.get_VOICE LANGUAGE != none і тд
            os.remove(file_path)
        else:
            promt = None
            await state.update_data(voice_path=file_path)
            text_language_dict = {
                "eng": "🎙️ Select the audio language for accurate transcription.",
                "ru": "🎙️ Выберите язык аудио для точного распознавания.",
                "ua": "🎙️ Оберіть мову аудіо для якісного розпізнавання.",}
            await message.answer(text_language_dict[language], reply_markup=builders.create_language_keyboard(language, prefix='recognition'))
            await state.set_state(VoiceLanguageInGeneration.waiting_for_language_in_generation)
    if promt:
        if db.get_ai_prompt_bool(message.chat.id):
            prompt = await bot_func.prompt_ai_response(promt)
        response = f"{language_dict[language][0]}\n\n<code>{prompt}</code>\n\n{language_dict[language][1]}"
        await message.answer(response, reply_markup=inline.generate_button(language))
        db.update_image_prompt(message.chat.id, prompt)


@router.message(F.voice)
async def handle_voice(message: Message, state: FSMContext):
    db.update_count_voice_message(message.chat.id)
    language = db.get_language(message.chat.id)
    file = await bot.get_file(message.voice.file_id)
    file_path = f"{file.file_id}.ogg"
    await bot.download_file(file.file_path, file_path)
    voice_language = db.get_voice_language(message.chat.id)
    if voice_language:
        text_from_voice = await bot_func.audio_transcription(file_path, voice_language) # Не зрозуміло якк мова , треба використати if elif db.get_VOICE LANGUAGE != none і тд
        data = db.get_history(message.chat.id)
        data.append({"role": "user", "content": text_from_voice})
        ai_response = await bot_func.ai_response(data)
        await message.answer(ai_response, reply_markup=builders.main_kb(language))
        db.update_history(message.chat.id, {"role": "user", "content": text_from_voice}, {"role": "assistant", "content": ai_response})
        os.remove(file_path)
    else:
        await state.update_data(voice_path=file_path)
        text_language_dict = {
            "eng": "🎙️ Select the audio language for accurate transcription.",
            "ru": "🎙️ Выберите язык аудио для точного распознавания.",
            "ua": "🎙️ Оберіть мову аудіо для якісного розпізнавання.",}

        await message.answer(text_language_dict[language], reply_markup=builders.create_language_keyboard(language, prefix='recognition'))
        await state.set_state(VoiceRecognition.waiting_for_language)


@router.message(F.text)
async def handle_crypto_request(message: Message):
    db.update_count_message(message.chat.id)
    data = db.get_history(message.chat.id)
    data.append({"role": "user", "content": message.text})
    ai_response = await bot_func.ai_response(data)
    kb = builders.main_kb(db.get_language(message.chat.id))
    await message.answer(ai_response, reply_markup=kb)
    db.update_history(message.chat.id, {"role": "user", "content": message.text}, {"role": "assistant", "content": ai_response})


