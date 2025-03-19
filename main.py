import asyncio
from aiogram import Bot, Dispatcher
import os
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("BOT_API_KEY")
bot = Bot(API_KEY, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
async def main():
    from handlers import bot_message, user_commands
    from callbacks import callback_handlers
    dp.include_routers(
        user_commands.router,
        bot_message.router,
        callback_handlers.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
