import asyncio
import logging
from pyrogram import Client, idle
from config import settings
from handlers.start import start_handler, help_handler, lang_handler
from handlers.document import document_handler
from handlers.photo import photo_handler

# إعداد تسجيل الأخطاء والمعلومات
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

async def main() -> None:
    app = Client(
        name="ocr_translate_bot",
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        bot_token=settings.BOT_TOKEN,
        workers=4
    )

    # تسجيل الهاندلرز
    app.add_handler(start_handler)
    app.add_handler(help_handler)
    app.add_handler(lang_handler)
    app.add_handler(document_handler)
    app.add_handler(photo_handler)

    await app.start()
    logging.info("✅ البوت يعمل الآن على Render...")

    # idle() هو الصحيح على Render وليس asyncio.Event
    await idle()

    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
