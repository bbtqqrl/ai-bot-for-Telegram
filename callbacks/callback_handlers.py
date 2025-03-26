from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards import inline, builders
import os
from data.db import Database
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from main import bot
from data import bot_func
from data.bot_func import language_voices
from handlers.bot_message import VoiceRecognition, VoiceLanguageInGeneration

db = Database()
router = Router()

@router.callback_query(F.data.in_(['ua', 'eng', 'ru']))
async def handle_pagination(callback_query: CallbackQuery):
    try:
        text_language_dict = {
            'ua': 'Ви успішно вибрали мову 📚✅',
            'eng': 'You have successfully selected the language. 📚✅',
            'ru': 'Вы успешно выбрали язык 📚✅'
        }
        kb = builders.main_kb(callback_query.data)
        db.update_language(callback_query.from_user.id, callback_query.data)
        await callback_query.message.delete()
        await bot.send_message(chat_id=callback_query.from_user.id,text=text_language_dict[callback_query.data],reply_markup=kb)

    except Exception as e:
        print(e)
        await callback_query.answer("❌ Error processing request.")
        await callback_query.message.delete()

@router.callback_query(F.data.in_(['yes', 'no']))
async def handle_pagination(callback_query: CallbackQuery):
    chat_id = callback_query.from_user.id
    try:
        language = db.get_language(chat_id)
        if callback_query.data == 'no':
            text_language_dict = {
                'ua': 'Ви відмовились генерувати зображення🚫',
                'eng': 'You refused to generate the image🚫',
                'ru': 'Вы отказались генерировать изображение🚫'
            }
            await callback_query.answer(text_language_dict[language])
            await callback_query.message.delete()
        else:
            text_language_dict = {
                'ua': '<b>Генерація зображення </b>🪄🖼',
                'eng': '<b>Image Generation </b>🪄🖼',
                'ru': '<b>Генерация изображения </b>🪄🖼'
            }
            await callback_query.message.delete()
            db.update_count_generation(chat_id)
            await bot.send_message(chat_id=chat_id,text=text_language_dict[language])
            image_path = await bot_func.generate_image(db.get_image_prompt(chat_id))
            photo = FSInputFile(image_path)
            await bot.send_photo(chat_id=chat_id, photo=photo)
            await bot.send_message(chat_id=chat_id,text=f"<b>Prompt</b> : <code>{db.get_image_prompt(chat_id)}</code>")
            os.remove(image_path)
    except Exception as e:
        print(e)
        await callback_query.answer("❌ All free image generation used. Try again later")

@router.callback_query(F.data.in_(['yes_generation', 'no_generation']))
async def handle_pagination(callback_query: CallbackQuery):
    language = db.get_language(callback_query.from_user.id)
    text_changes = {
        'ua': 'Зміни застосовані успішно!',
        'eng': 'Changes applied successfully!',
        'ru': 'Изменения применены успешно!'
    }
    text_language_dict = {
        "yes_generation" :
            {"eng": f"Your prompt will be optimized using AI. 🤖\n\nYou can write your query in any way or record it by voice. 🎙️\nThe main thing is the meaning, and AI will improve the description for the best result! 🚀\n\nGood luck to you! 🍀",
            "ru": f"Ваш промт будет оптимизирован с помощью ИИ. 🤖\n\nМожете писать запрос любой записью или голосом. 🎙️\nГлавное — смысл, а ИИ улучшит описание для наилучшего результата! 🚀\n\nУдачи вам! 🍀",
            "ua": f"Ваш промт буде оптимізований за допомогою ШІ. 🤖\n\nМожете писати запит будь-як або записувати голосом. 🎙️\nГоловне — сенс, а ШІ покращить опис для найкращого результату! 🚀\n\nУдачі вам! 🍀"},
        "no_generation" :
            {"eng": f"Your prompt will not be optimized!\n\nThe AI ​​for image generation understands only English. 🤖\nDescribe everything in detail. ✍️\nUse adjectives, style, lighting, angle.\n\nGood luck! 🍀",
            "ru": f"Ваш промт не будет оптимизирован!\n\nИИ для генерации изображений понимает только английский. 🤖\nОписывайте все подробно. ✍️\nИспользуйте прилагательные, стиль, освещение, ракурс.\n\nУдачи вам! 🍀",
            "ua": f"Ваш промт не буде оптимізований!\n\nШІ для генерації зображень розуміє лише англійську. 🤖\nОписуйте все детально. ✍️\nВикористовуйте прикметники, стиль, освітлення, ракурс.\n\nУдачі вам! 🍀"}}
    db.update_ai_prompt_bool(callback_query.from_user.id, {'yes_generation' : True, 'no_generation' : False}[callback_query.data])
    await callback_query.message.edit_text(text_changes[language])
    await bot.send_message(chat_id=callback_query.from_user.id, text=text_language_dict[callback_query.data][language],reply_markup=builders.main_kb(language))



@router.callback_query(F.data == 'generation_settings')
async def process_callback_pagination(callback_query: CallbackQuery):
    language = db.get_language(callback_query.from_user.id)
    text_language_dict = {
        "eng": f"⚙️ Optimize your prompt (query) to the image generator using AI?",
        "ru": f"⚙️ Оптимизировать ваш промт (запрос) к генератору изображений с помощью ИИ?",
        "ua": f"⚙️ Оптимізувати ваш промт (запит) до генератору зображень за допомогою ШІ?"}

    await callback_query.message.answer(text_language_dict[language], reply_markup=inline.generate_button(language, '_generation'))

@router.callback_query(F.data == 'synthesis_settings')
async def process_callback_pagination(callback_query: CallbackQuery):
    language = db.get_language(callback_query.from_user.id)
    synthesis_data = db.get_synthesis_settings(callback_query.from_user.id)
    syntesis_language = await bot_func.get_language_name_by_code(synthesis_data["language_code"])
    voice_name = synthesis_data["voice_name"]
    pitch = synthesis_data["pitch"]
    speaking_rate = synthesis_data["speaking_rate"]
    text_language_dict = {
        "eng": f"🎛 Speech synthesis settings:\n\n<b>Language:</b> {syntesis_language}\n<b>Voice:</b> {voice_name}\n<b>Pitch:</b> {pitch}\n<b>Speaking rate:</b> {speaking_rate}\n\nChoose a language for the speech synthesizer 🔊⤵️",
        "ru": f"🎛 Настройка синтеза речи:\n\n<b>Язык:</b> {syntesis_language}\n<b>Голос:</b> {voice_name}\n<b>Высота голоса:</b> {pitch}\n<b>Скорость речи:</b> {speaking_rate}\n\nВыберите язык для синтезатора речи 🔊⤵️",
        "ua": f"🎛 Налаштування синтезу мовлення:\n\n<b>Мова:</b> {syntesis_language}\n<b>Голос:</b> {voice_name}\n<b>Висота голосу:</b> {pitch}\n<b>Швидкість мовлення:</b> {speaking_rate}\n\nВиберіть мову для синтезатора мовлення 🔊⤵️"}

    await bot.send_message(chat_id=callback_query.from_user.id, text=text_language_dict[language],reply_markup=builders.create_language_keyboard(language))
    await callback_query.answer()


@router.callback_query(F.data == 'settings')
async def process_callback_pagination(callback_query: CallbackQuery):
    text_language_dict = {
        'ua': 'Налаштування боту ⚙️⤵️',
        'eng': 'Bot settings ⚙️⤵️',
        'ru': 'Настройки бота ⚙️⤵️'
    }
    await callback_query.message.answer_photo(photo=FSInputFile('photo_2025-03-15_21-36-31.jpg'), text=text_language_dict[db.get_language(callback_query.from_user.id)],reply_markup=inline.settings_button(language=db.get_language(callback_query.from_user.id)))
    await callback_query.answer()



@router.callback_query(F.data == 'language_settings')
async def delete_user_data(callback_query: CallbackQuery):
    text_language_dict = {
        'ua': 'Виберіть нову мову 📚',
        'eng': 'Choose new language 📚',
        'ru': 'Выберите новый язык 📚'
    }
    language = db.get_language(callback_query.from_user.id)
    kb = inline.language_button()
    await callback_query.message.answer(text_language_dict[language], reply_markup=kb)
    await callback_query.answer()


@router.callback_query(F.data == 'voice_language_settings')
async def process_callback_pagination(callback_query: CallbackQuery, state: FSMContext):
    text_language_dict = {
        "eng": "🎙️ Select the audio language for accurate transcription.",
        "ru": "🎙️ Выберите язык аудио для точного распознавания.",
        "ua": "🎙️ Оберіть мову аудіо для якісного розпізнавання.",}
    language = db.get_language(callback_query.from_user.id)
    await callback_query.message.answer(text_language_dict[language], reply_markup=builders.create_language_keyboard(language, prefix='recognition'))
    await callback_query.answer()
    await state.set_state(VoiceRecognition.waiting_for_language)



@router.callback_query(lambda c: c.data.startswith('page_synthesis|'))
async def process_callback_pagination(callback_query: CallbackQuery):
    page = int(callback_query.data.split('|')[1])
    text_language_dict = {
        "eng": f"🎛 Speech synthesis settings:\n\n<b>Language:</b> Not selected\n<b>Voice:</b> Not selected\n<b>Pitch:</b> Not selected\n<b>Speaking rate:</b> Not selected\n\nChoose a language for the speech synthesizer 🔊⤵️",
        "ru": f"🎛 Настройка синтеза речи:\n\n<b>Язык:</b> Не выбрано\n<b>Голос:</b> Не выбрано\n<b>Высота голоса:</b> Не выбрано\n<b>Скорость речи:</b> Не выбрано\n\nВыберите язык для синтезатора речи 🔊⤵️",
        "ua": f"🎛 Налаштування синтезу мовлення:\n\n<b>Мова:</b> Не вибраний\n<b>Голос:</b> Не вибраний\n<b>Висота голосу:</b> Не вибраний\n<b>Швидкість мовлення:</b> Не вибрано\n\nВиберіть мову для синтезатора мовлення 🔊⤵️"}

    await callback_query.message.edit_text(text=text_language_dict[db.get_language(callback_query.from_user.id)],reply_markup=builders.create_language_keyboard(language=db.get_language(callback_query.from_user.id), page=page, prefix = 'synthesis'))

@router.callback_query(lambda c: c.data.startswith('page_recognition|'))
async def process_callback_pagination(callback_query: CallbackQuery):
    page = int(callback_query.data.split('|')[1])
    text_language_dict = {
        "eng": "🎙️ Select the audio language for accurate transcription.",
        "ru": "🎙️ Выберите язык аудио для точного распознавания.",
        "ua": "🎙️ Оберіть мову аудіо для якісного розпізнавання.",}
    await callback_query.message.edit_text(text=text_language_dict[db.get_language(callback_query.from_user.id)],reply_markup=builders.create_language_keyboard(language=db.get_language(callback_query.from_user.id), page=page, prefix='recognition'))

@router.callback_query(lambda c: c.data.startswith('lang_synthesis|'))
async def process_callback_language(callback_query: CallbackQuery):
    selected_language = callback_query.data.split('|')[1]
    text_language_dict = {
        "eng": f"🎛 Speech synthesis settings:\n\n<b>Language:</b> {selected_language}\n<b>Voice:</b> Not selected\n<b>Pitch:</b> Not selected\n<b>Speaking rate:</b> Not selected\n\nChoose a voice for the speech synthesizer 🔊⤵️",
        "ru": f"🎛 Настройка синтеза речи:\n\n<b>Язык:</b> {selected_language}\n<b>Голос:</b> Не выбрано\n<b>Высота голоса:</b> Не выбрано\n<b>Скорость речи:</b> Не выбрано\n\nВыберите голос для синтезатора речи 🔊⤵️",
        "ua": f"🎛 Налаштування синтезу мовлення:\n\n<b>Мова:</b> {selected_language}\n<b>Голос:</b> Не вибраний\n<b>Висота голосу:</b> Не вибраний\n<b>Швидкість мовлення:</b> Не вибрано\n\nВиберіть голос для синтезатора мовлення 🔊⤵️"}
    await callback_query.message.edit_text(text=text_language_dict[db.get_language(callback_query.from_user.id)],reply_markup=builders.create_voice_keyboard(language_voices.get(selected_language)['voices']))

@router.callback_query(lambda c: c.data.startswith('voice|'))
async def process_callback_pagination(callback_query: CallbackQuery):
    callback_data = callback_query.data.split('|')
    language_code, voice_name = callback_data[1][:5], callback_data[1]
    selected_language = await bot_func.get_language_name_by_code(language_code)
    text_language_dict = {
        "eng": f"🎛 Speech synthesis settings:\n\n<b>Language:</b> {selected_language}\n<b>Voice:</b> {voice_name}\n<b>Pitch:</b> Not selected\n<b>Speaking rate:</b> Not selected\n\nChoose a voice for the speech synthesizer 🔊⤵️",
        "ru": f"🎛 Настройка синтеза речи:\n\n<b>Язык:</b> {selected_language}\n<b>Голос:</b> {voice_name}\n<b>Высота голоса:</b> Не выбрано\n<b>Скорость речи:</b> Не выбрано\n\nВыберите голос для синтезатора речи 🔊⤵️",
        "ua": f"🎛 Налаштування синтезу мовлення:\n\n<b>Мова:</b> {selected_language}\n<b>Голос:</b> {voice_name}\n<b>Висота голосу:</b> Не вибраний\n<b>Швидкість мовлення:</b> Не вибрано\n\nВиберіть голос для синтезатора мовлення 🔊⤵️"}
    await callback_query.message.edit_text(text=text_language_dict[db.get_language(callback_query.from_user.id)],reply_markup=inline.synthesis_pitch_button(db.get_language(callback_query.from_user.id), language_code, voice_name))

@router.callback_query(lambda c: c.data.startswith('pitch|'))
async def process_callback_pagination(callback_query: CallbackQuery):
    _, language_code, voice_name, pitch = callback_query.data.split('|')
    selected_language = await bot_func.get_language_name_by_code(language_code)
    text_language_dict = {
        "eng": f"🎛 Speech synthesis settings:\n\n<b>Language:</b> {selected_language}\n<b>Voice:</b> {voice_name}\n<b>Pitch:</b> {pitch}\n<b>Speaking rate:</b> Not selected\n\nChoose speaking rate for the speech synthesizer 🔊⤵️",
        "ru": f"🎛 Настройка синтеза речи:\n\n<b>Язык:</b> {selected_language}\n<b>Голос:</b> {voice_name}\n<b>Высота голоса:</b> {pitch}\n<b>Скорость речи:</b> Не выбрано\n\nВыберите скорость речи для синтезатора речи 🔊⤵️",
        "ua": f"🎛 Налаштування синтезу мовлення:\n\n<b>Мова:</b> {selected_language}\n<b>Голос:</b> {voice_name}\n<b>Висота голосу:</b> {pitch}\n<b>Швидкість мовлення:</b> Не вибрано\n\nВиберіть швидкість мовлення для синтезатора мовлення 🔊⤵️"}

    await callback_query.message.edit_text(text=text_language_dict[db.get_language(callback_query.from_user.id)],reply_markup=inline.synthesis_rate_button(db.get_language(callback_query.from_user.id), language_code, voice_name, pitch))

@router.callback_query(lambda c: c.data.startswith('rate|'))
async def process_callback_pagination(callback_query: CallbackQuery):
    _, language_code, voice_name, pitch, speaking_rate = callback_query.data.split('|')
    selected_language = await bot_func.get_language_name_by_code(language_code)
    db.update_synthesis_settings(callback_query.from_user.id, language_code, voice_name, pitch, speaking_rate)
    text_language_dict = {
        "eng": f"🎛 Speech synthesis settings:\n\n<b>Language:</b> {selected_language}\n<b>Voice:</b> {voice_name}\n<b>Pitch:</b> {pitch}\n<b>Speaking rate:</b> {speaking_rate}\n\nChanges applied successfully! 🔊",
        "ru": f"🎛 Настройка синтеза речи:\n\n<b>Язык:</b> {selected_language}\n<b>Голос:</b> {voice_name}\n<b>Высота голоса:</b> {pitch}\n<b>Скорость речи:</b> {speaking_rate}\n\nИзменения применены успешно! 🔊",
        "ua": f"🎛 Налаштування синтезу мовлення:\n\n<b>Мова:</b> {selected_language}\n<b>Голос:</b> {voice_name}\n<b>Висота голосу:</b> {pitch}\n<b>Швидкість мовлення:</b> {speaking_rate}\n\nЗміни застосовані успішно! 🔊"}

    await callback_query.message.edit_text(text=text_language_dict[db.get_language(callback_query.from_user.id)])




@router.callback_query(VoiceLanguageInGeneration.waiting_for_language_in_generation)
async def set_voice_language(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    new_language = language_voices[callback_query.data.split('|')[1]]["language_code"]
    language = db.get_language(user_id)
    text_language_dict = {
        "eng": f"Your audio language has been successfully saved!\n\n You can change it in your Profile settings 📋",
        "ru": f"Ваш язык аудио успешно сохранен!\n\n Изменить его можно в настройках Профиля 📋",
        "ua": f"Ваша мова аудіо успішно збережена!\n\n Змінити її можна в налаштуваннях Профілю 📋"}
    await callback_query.message.edit_text(text=text_language_dict[language])
    if not db.get_voice_language(user_id): 
        data = await state.get_data()
        file_path = data.get("voice_path")
        prompt = await bot_func.audio_transcription(file_path, new_language)
        os.remove(file_path)
        if file_path:
            if db.get_ai_prompt_bool(user_id):
                prompt = await bot_func.prompt_ai_response(prompt)
            language_dict = {
                'ua': ['Ось ваш промт ⤵️', 'Генерувати зображення?'],
                'eng': ['Here is your prompt ⤵️', 'Generate image?'],
                'ru': ['Вот ваш промт ⤵️', 'Генерировать изображение?']}
            response = f"{language_dict[language][0]}\n\n<code>{prompt}</code>\n\n{language_dict[language][1]}"
            await bot.send_message(user_id, response, reply_markup=inline.generate_button(language))
            db.update_image_prompt(user_id, prompt)
    
    db.update_voice_language(user_id, new_language)
    await state.clear()


@router.callback_query(VoiceRecognition.waiting_for_language)
async def set_voice_language(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    new_language = language_voices[callback_query.data.split('|')[1]]["language_code"]
    language = db.get_language(user_id)
    text_language_dict = {
        "eng": f"Your audio language has been successfully saved!\n\n You can change it in your Profile settings 📋",
        "ru": f"Ваш язык аудио успешно сохранен!\n\n Изменить его можно в настройках Профиля 📋",
        "ua": f"Ваша мова аудіо успішно збережена!\n\n Змінити її можна в налаштуваннях Профілю 📋"}
    await callback_query.message.edit_text(text=text_language_dict[language])
    if not db.get_voice_language(user_id): 
        data = await state.get_data()
        file_path = data.get("voice_path")
        if file_path:
            text_from_voice = await bot_func.audio_transcription(file_path, new_language) 
            data = db.get_history(user_id)
            data.append({"role": "user", "content": text_from_voice})
            ai_response = await bot_func.ai_response(data)
            await bot.send_message(chat_id=user_id, text= ai_response, reply_markup=builders.main_kb(language))

            db.update_history(user_id, {"role": "user", "content": text_from_voice}, {"role": "assistant", "content": ai_response})
            os.remove(file_path)
    
    db.update_voice_language(user_id, new_language)
    await state.clear()



