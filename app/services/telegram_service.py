from app.config.settings import settings


class TelegramService:
    async def send(self, chat_id: str, message: str) -> None:
        if not settings.telegram_bot_token:
            return

        try:
            from telegram import Bot

            bot = Bot(token=settings.telegram_bot_token)
            await bot.send_message(chat_id=chat_id, text=message)
        except Exception:
            return
