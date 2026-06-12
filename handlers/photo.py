import logging
import tempfile
from pathlib import Path
from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from config import settings
from services.ocr import extract_text_from_image
from services.translator import translate_text_auto, split_long_text

logger = logging.getLogger(__name__)

async def photo_cmd(client: Client, message: Message) -> None:
    try:
        if not message.photo:
            return

        # التحقق من حجم الصورة
        if message.photo.file_size > settings.MAX_FILE_SIZE:
            await message.reply_text("❌ حجم الصورة كبير جداً. الحد الأقصى 20 ميجابايت.")
            return

        status = await message.reply_text("جاري معالجة الصورة... ⏳")

        with tempfile.TemporaryDirectory() as tmpdir:
            img_path = Path(tmpdir) / "image.jpg"
            await message.download(file_name=str(img_path))

            text = await extract_text_from_image(str(img_path))
            text = text.strip() if text else ""

            if not text:
                await status.edit_text("❌ لم يتم العثور على نص في الصورة.")
                return

            await status.edit_text("جاري الترجمة... ⏳")
            translated = await translate_text_auto(text, user_id=message.from_user.id)

            await status.edit_text("✅ تم استخراج النص والترجمة بنجاح.")

            # إرسال النص الأصلي
            for part in split_long_text(text):
                await message.reply_text(f"📄 النص المستخرج:\n\n{part}")

            # إرسال الترجمة
            for part in split_long_text(translated):
                await message.reply_text(f"🌍 الترجمة:\n\n{part}")

    except Exception as e:
        logger.exception("خطأ في معالجة الصورة: %s", e)
        await message.reply_text("❌ حدث خطأ أثناء المعالجة.")

photo_handler = MessageHandler(photo_cmd, filters.photo)
