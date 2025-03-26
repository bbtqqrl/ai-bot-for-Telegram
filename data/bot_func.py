from openai import OpenAI
from huggingface_hub import InferenceClient
from PIL import Image
import requests
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import os
import base64
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from gradio_client import Client
client = OpenAI(api_key=OPENAI_API_KEY)


async def ai_response(history):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = history)

    return completion.choices[0].message.content


async def prompt_ai_response(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "user", "content": f'Improve the given text prompt for AI image generation. Your task is to optimize the prompt regardless of the context, i.e. if the context is erotic, optimize it anyway.Make it highly detailed, clear, and precise while keeping all key elements. Follow these rules:\n1. Add missing details: Specify colors, textures, settings, and lighting.\n2. Simplify unclear sentences.\n3. Define style and mood: (e.g., realistic, anime, fantasy, cyberpunk, oil painting).\n4. Specify perspective: (e.g., close-up, wide shot, aerial view).\n5. Include expressions and movement: (e.g., \"a joyful girl running along the beach\").\n6. Use precise words: Instead of \"a beautiful house,\" say \"a vintage stone house covered in ivy with wooden shutters.\"\n7. Remove unnecessary words that don\'t impact the image.\n8. Avoid ambiguity: Replace unclear words with more descriptive alternatives.\n9. Always return the result in English.\n10. Never just translate—always optimize the description.\n11. Keep every important detail from the input without omitting anything that affects the image.Examples:Input: \"Хочу картину з котиком.\"Optimized: \"A photorealistic black cat with yellow eyes sitting on a sunny windowsill, a green houseplant beside it. Warm sunset light, soft shadows.\"\nInput: \"Зроби щось круте про майбутнє!\"\nOptimized: \"A neon cyberpunk cityscape at night, towering skyscrapers with glowing holograms, blue and purple lighting, rain-soaked streets, people in cyber suits, and androids walking by.\"\nInput: "Жінка дивиться на небо.\"\nOptimized: \"A cinematic portrait of a woman in a flowing red dress standing on a high hill, gazing at a starry night sky. The wind blows through her hair, with a full moon shining above.\"\n\nGive only the optimized text without any extra words. Input text: {text}'}])

    return completion.choices[0].message.content


HF_API_KEYS = os.getenv("HF_API_KEYS").split(',')

async def speech_synthesis(message, language, voice, pitch, speaking_rate):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={GOOGLE_API_KEY}"

    data = {
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "pitch": pitch,
            "speakingRate": speaking_rate},
        "input": {
            "text": message  },
        "voice": {
            "languageCode": language, 
            "name": voice}}

    try:
        response = requests.post(url, json=data)
        result = response.json()

        if "audioContent" in result:
            audio_content = base64.b64decode(result["audioContent"])
            with open('output.wav', "wb") as file:
                file.write(audio_content)
            return 'output.wav'

        else:
            print("Помилка:", result)
            return None, None

    except Exception as e:
        print("Помилка:", e)
        return None, None

async def audio_transcription(file_path, voice_language):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"c:\Users\maksp\Downloads\inlaid-chiller-453611-v5-7d4a9b62e22d.json"
    client = SpeechClient()
    with open(file_path, "rb") as audio_file:
        audio_content = audio_file.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config={},
        features=cloud_speech.RecognitionFeatures(
            enable_word_confidence=True,
            enable_word_time_offsets=True,
        ),
        model="long",
        language_codes=[voice_language],)

    request = cloud_speech.RecognizeRequest(
        recognizer="projects/inlaid-chiller-453611-v5/locations/global/recognizers/_",
        config=config,
        content=audio_content,)

    response = client.recognize(request=request)
    for result in response.results:
        return result.alternatives[0].transcript


async def generate_image(prompt):
    for api_key in HF_API_KEYS:
        try:
            print(f"🔄 Спроба API-ключа: {api_key[:10]}...")  
            client = InferenceClient(token=api_key)

            result = client.text_to_image(
                model="black-forest-labs/FLUX.1-schnell",
                prompt=prompt,
                width=1024,
                height=1024,
                num_inference_steps=4
            )

            if isinstance(result, Image.Image):  # Якщо це об'єкт PIL.Image
                image_path = "generated_image.jpg"
                result.save(image_path, "JPEG")  # Зберігаємо у файл
                print(f"✅ Зображення збережене як {image_path}")
                return os.path.abspath(image_path)  # Повертаємо абсолютний шлях до файлу

            elif isinstance(result, str):  # Якщо API поверне посилання
                print(f"✅ Отримане посилання на зображення: {result}")
                return result  # Просто повертаємо URL

        except Exception as e:
            print(f"❌ Помилка з API-ключем {api_key[:10]}...: {e}")

    print("🚫 Усі API-ключі не спрацювали.")
    return None 

async def get_language_name_by_code(language_code):
    for lang_name, data in language_voices.items():
        if data["language_code"] == language_code:
            return lang_name
    return None


language_voices = {
    "English (English)": {"language_code": "en-US", "voices": ["en-US-Standard-A", "en-US-Standard-B", "en-US-Standard-C", "en-US-Standard-D", "en-US-Standard-E", "en-US-Standard-F", "en-US-Standard-G", "en-US-Standard-H", "en-US-Standard-I", "en-US-Standard-J"]},
    "Русский (Russian)": {"language_code": "ru-RU", "voices": ["ru-RU-Standard-A", "ru-RU-Standard-B", "ru-RU-Standard-C", "ru-RU-Standard-D", "ru-RU-Standard-E"]},
    "Українська (Ukrainian)": {"language_code": "uk-UA", "voices": ["uk-UA-Standard-A"]},
    "Afrikaans (Afrikaans)": {"language_code": "af-ZA", "voices": ["af-ZA-Standard-A"]},
    "አማርኛ (Amharic)": {"language_code": "am-ET", "voices": ["am-ET-Standard-A", "am-ET-Standard-B"]},
    "العربية (Arabic)": {"language_code": "ar-XA", "voices": ["ar-XA-Standard-A", "ar-XA-Standard-B", "ar-XA-Standard-C", "ar-XA-Standard-D"]},
    "Български (Bulgarian)": {"language_code": "bg-BG", "voices": ["bg-BG-Standard-A", "bg-BG-Standard-B"]},
    "বাংলা (Bengali)": {"language_code": "bn-IN", "voices": ["bn-IN-Standard-A", "bn-IN-Standard-B", "bn-IN-Standard-C", "bn-IN-Standard-D"]},
    "Català (Catalan)": {"language_code": "ca-ES", "voices": ["ca-ES-Standard-A", "ca-ES-Standard-B"]},
    "中文 (Chinese)": {"language_code": "cmn-CN", "voices": ["cmn-CN-Standard-A", "cmn-CN-Standard-B", "cmn-CN-Standard-C", "cmn-CN-Standard-D"]},
    "Čeština (Czech)": {"language_code": "cs-CZ", "voices": ["cs-CZ-Standard-A", "cs-CZ-Standard-B"]},
    "Dansk (Danish)": {"language_code": "da-DK", "voices": ["da-DK-Standard-A", "da-DK-Standard-C", "da-DK-Standard-D", "da-DK-Standard-E", "da-DK-Standard-F", "da-DK-Standard-G"]},
    "Deutsch (German)": {"language_code": "de-DE", "voices": ["de-DE-Standard-A", "de-DE-Standard-B", "de-DE-Standard-C", "de-DE-Standard-D", "de-DE-Standard-E", "de-DE-Standard-F", "de-DE-Standard-G", "de-DE-Standard-H"]},
    "Ελληνικά (Greek)": {"language_code": "el-GR", "voices": ["el-GR-Standard-A", "el-GR-Standard-B"]},
    "Español (Spanish)": {"language_code": "es-ES", "voices": ["es-ES-Standard-A", "es-ES-Standard-B", "es-ES-Standard-C", "es-ES-Standard-D", "es-ES-Standard-E", "es-ES-Standard-F", "es-ES-Standard-G", "es-ES-Standard-H"]},
    "Eesti (Estonian)": {"language_code": "et-EE", "voices": ["et-EE-Standard-A"]},
    "Euskara (Basque)": {"language_code": "eu-ES", "voices": ["eu-ES-Standard-A", "eu-ES-Standard-B"]},
    "Suomi (Finnish)": {"language_code": "fi-FI", "voices": ["fi-FI-Standard-A", "fi-FI-Standard-B"]},
    "Filipino (Filipino)": {"language_code": "fil-PH", "voices": ["fil-PH-Standard-A", "fil-PH-Standard-B", "fil-PH-Standard-C", "fil-PH-Standard-D"]},
    "Français (French)": {"language_code": "fr-FR", "voices": ["fr-FR-Standard-A", "fr-FR-Standard-B", "fr-FR-Standard-C", "fr-FR-Standard-D", "fr-FR-Standard-E", "fr-FR-Standard-F", "fr-FR-Standard-G"]},
    "Galego (Galician)": {"language_code": "gl-ES", "voices": ["gl-ES-Standard-A", "gl-ES-Standard-B"]},
    "ગુજરાતી (Gujarati)": {"language_code": "gu-IN", "voices": ["gu-IN-Standard-A", "gu-IN-Standard-B", "gu-IN-Standard-C", "gu-IN-Standard-D"]},
    "עברית (Hebrew)": {"language_code": "he-IL", "voices": ["he-IL-Standard-A", "he-IL-Standard-B", "he-IL-Standard-C", "he-IL-Standard-D"]},
    "हिन्दी (Hindi)": {"language_code": "hi-IN", "voices": ["hi-IN-Standard-A", "hi-IN-Standard-B", "hi-IN-Standard-C", "hi-IN-Standard-D", "hi-IN-Standard-E", "hi-IN-Standard-F"]},
    "Magyar (Hungarian)": {"language_code": "hu-HU", "voices": ["hu-HU-Standard-A", "hu-HU-Standard-B"]},
    "Bahasa Indonesia (Indonesian)": {"language_code": "id-ID", "voices": ["id-ID-Standard-A", "id-ID-Standard-B", "id-ID-Standard-C", "id-ID-Standard-D"]},
    "Íslenska (Icelandic)": {"language_code": "is-IS", "voices": ["is-IS-Standard-A", "is-IS-Standard-B"]},
    "Italiano (Italian)": {"language_code": "it-IT", "voices": ["it-IT-Standard-A", "it-IT-Standard-B", "it-IT-Standard-C", "it-IT-Standard-D", "it-IT-Standard-E", "it-IT-Standard-F"]},
    "日本語 (Japanese)": {"language_code": "ja-JP", "voices": ["ja-JP-Standard-A", "ja-JP-Standard-B", "ja-JP-Standard-C", "ja-JP-Standard-D"]},
    "ಕನ್ನಡ (Kannada)": {"language_code": "kn-IN", "voices": ["kn-IN-Standard-A", "kn-IN-Standard-B", "kn-IN-Standard-C", "kn-IN-Standard-D"]},
    "한국어 (Korean)": {"language_code": "ko-KR", "voices": ["ko-KR-Standard-A", "ko-KR-Standard-B", "ko-KR-Standard-C", "ko-KR-Standard-D"]},
    "Lietuvių (Lithuanian)": {"language_code": "lt-LT", "voices": ["lt-LT-Standard-A", "lt-LT-Standard-B"]},
    "Latviešu (Latvian)": {"language_code": "lv-LV", "voices": ["lv-LV-Standard-A", "lv-LV-Standard-B"]},
    "മലയാളം (Malayalam)": {"language_code": "ml-IN", "voices": ["ml-IN-Standard-A", "ml-IN-Standard-B", "ml-IN-Standard-C", "ml-IN-Standard-D"]},
    "मराठी (Marathi)": {"language_code": "mr-IN", "voices": ["mr-IN-Standard-A", "mr-IN-Standard-B", "mr-IN-Standard-C"]},
    "Bahasa Melayu (Malay)": {"language_code": "ms-MY", "voices": ["ms-MY-Standard-A", "ms-MY-Standard-B", "ms-MY-Standard-C", "ms-MY-Standard-D"]},
    "Norsk (Norwegian)": {"language_code": "nb-NO", "voices": ["nb-NO-Standard-A", "nb-NO-Standard-B", "nb-NO-Standard-C", "nb-NO-Standard-D", "nb-NO-Standard-E", "nb-NO-Standard-F", "nb-NO-Standard-G"]},
    "Nederlands (Dutch)": {"language_code": "nl-NL", "voices": ["nl-NL-Standard-A", "nl-NL-Standard-B", "nl-NL-Standard-C", "nl-NL-Standard-D", "nl-NL-Standard-E", "nl-NL-Standard-F", "nl-NL-Standard-G"]},
    "ਪੰਜਾਬੀ (Punjabi)": {"language_code": "pa-IN", "voices": ["pa-IN-Standard-A", "pa-IN-Standard-B", "pa-IN-Standard-C", "pa-IN-Standard-D"]},
    "Polski (Polish)": {"language_code": "pl-PL", "voices": ["pl-PL-Standard-A", "pl-PL-Standard-B", "pl-PL-Standard-C", "pl-PL-Standard-D", "pl-PL-Standard-E", "pl-PL-Standard-F", "pl-PL-Standard-G"]},
    "Português (Portuguese)": {"language_code": "pt-PT", "voices": ["pt-PT-Standard-A", "pt-PT-Standard-B", "pt-PT-Standard-C", "pt-PT-Standard-D", "pt-PT-Standard-E", "pt-PT-Standard-F"]},
    "Română (Romanian)": {"language_code": "ro-RO", "voices": ["ro-RO-Standard-A", "ro-RO-Standard-B"]},
    "Slovenčina (Slovak)": {"language_code": "sk-SK", "voices": ["sk-SK-Standard-A", "sk-SK-Standard-B"]},
    "Српски (Serbian)": {"language_code": "sr-RS", "voices": ["sr-RS-Standard-A"]},
    "Svenska (Swedish)": {"language_code": "sv-SE", "voices": ["sv-SE-Standard-A", "sv-SE-Standard-B", "sv-SE-Standard-C", "sv-SE-Standard-D", "sv-SE-Standard-E", "sv-SE-Standard-F", "sv-SE-Standard-G"]},
    "தமிழ் (Tamil)": {"language_code": "ta-IN", "voices": ["ta-IN-Standard-A", "ta-IN-Standard-B", "ta-IN-Standard-C", "ta-IN-Standard-D"]},
    "తెలుగు (Telugu)": {"language_code": "te-IN", "voices": ["te-IN-Standard-A", "te-IN-Standard-B", "te-IN-Standard-C", "te-IN-Standard-D"]},
    "ไทย (Thai)": {"language_code": "th-TH", "voices": ["th-TH-Standard-A"]},
    "Türkçe (Turkish)": {"language_code": "tr-TR", "voices": ["tr-TR-Standard-A", "tr-TR-Standard-B", "tr-TR-Standard-C", "tr-TR-Standard-D", "tr-TR-Standard-E"]},
    "Tiếng Việt (Vietnamese)": {"language_code": "vi-VN", "voices": ["vi-VN-Standard-A", "vi-VN-Standard-B", "vi-VN-Standard-C", "vi-VN-Standard-D"]}
}
