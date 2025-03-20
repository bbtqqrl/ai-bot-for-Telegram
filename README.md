# AI Telegram Bot

## 🤖 Description
This Telegram bot leverages artificial intelligence to analyze and process voice and text messages. It can:
- Detect the language of voice messages and transcribe them correctly.
- Generate AI-powered responses.
- Create images based on text prompts.

## ✨ Key Features
- ✏️ **Voice Message Recognition**: Automatically detects the language of voice messages and converts them to text.
- 🌐 **Multi-Language Support**: Allows users to switch bot languages and process messages in different languages.
- 🎨 **Image Generation**: Uses AI to create images from text descriptions.
- 🧠 **Interactive & Fast**: Intuitive interface with quick user interaction.

## 💪 Technologies Used
- **Python 3**
- **Aiogram 3** (asynchronous Telegram framework)
- **PostgreSQL** (for user data storage)
- **OpenAI GPT-3.5 Turbo** (for generating AI-based responses)
- **Google STT** (for voice recognition)
- **Google TTS** (for voice synthesis)
- **FLUX.1** (for image generation)

## 🛠 Installation & Setup
### 1. Clone the Repository
```bash
git clone https://github.com/username/repo.git
cd repo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file and add:
```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=your_postgresql_url
OPENAI_API_KEY=your_openai_api_key
HF_API_KEY=your_hf_api_key
```

### 4. Run the Bot
```bash
python main.py
```

## 🚀 Future Plans
- Adding support for more AI models.
- Enhancing voice message processing.
- Optimizing performance for faster response times.

## 💌 Feedback
If you have ideas or suggestions, feel free to open an issue or contact me on Telegram!

