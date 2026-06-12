import logging
from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from services.translator import toggle_user_lang

logger = logging.getLogger(__name__)

async def start_cmd(client: Client, message: Message) -> None:
    try:
        await message.reply_text(
            "مرحباً بك! 👋\n"
            "أرسل ملف PDF أو صورة وسأستخرج النص وأترجمه.\n"
            "استخدم /help للتفاصيل."
        )
    except Exception as e:
        logger.exception("خطأ في /start: %s", e)

async def help_cmd(client: Client, message: Message) -> None:
    try:
        await message.reply_text(
            "📌 تعليمات الاستخدام:\n"
            "1) أرسل صورة أو ملف PDF.\n"
            "2) سأستخرج النص باستخدام OCR.\n"
            "3) سأترجم النص تلقائياً بين العربية والإنجليزية.\n\n"
            "الأوامر:\n"
            "/start - رسالة ترحيب\n"
            "/help  - تعليمات الاستخدام\n"
            "/lang  - تبديل اتجاه الترجمة (عربي↔إنجليزي)\n"
        )
    except Exception as e:
        logger.exception("خطأ في /help: %s", e)

async def lang_cmd(client: Client, message: Message) -> None:
    try:
        new_lang = toggle_user_lang(message.from_user.id)
        text = (
            "✅ تم ضبط الترجمة: عربي → إنجليزي"
            if new_lang == "ar-en"
            else "✅ تم ضبط الترجمة: إنجليزي → عربي"
        )
        await message.reply_text(text)
    except Exception as e:
        logger.exception("خطأ في /lang: %s", e)

start_handler = MessageHandler(start_cmd, filters.command("start"))
help_handler  = MessageHandler(help_cmd,  filters.command("help"))
lang_handler  = MessageHandler(lang_cmd,  filters.command("lang"))
