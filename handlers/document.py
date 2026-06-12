import logging
import tempfile
from pathlib import Path
from pyrogram import filters, Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from config import settings
from services.pdf_processor import pdf_to_images
from services.ocr import extract_text_from_image
from services.translator import translate_text_auto, split_long_text

logger = logging.getLogger(__name__)

# الامتدادات المسموح بها
ALLOWED_MIME = {
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/jpg",
}

async def document_cmd(client: Client, message: Message) -> None:
    try:
        doc = message.document
        if not doc:
            return

        # التحقق من نوع الملف
        if doc.mime_type not in ALLOWED_MIME:
            await message.reply_text(
                "❌ نوع الملف غير مدعوم.\n"
                "الأنواع المقبولة: PDF، JPG، PNG، WEBP"
            )
            return

        # التحقق من حجم الملف
        if doc.file_size > settings.MAX_FILE_SIZE:
            await message.reply_text("❌ حجم الملف كبير جداً. الحد الأقصى 20 ميجابايت.")
            return

        status = await message.reply_text("جاري معالجة الملف... ⏳")

        with tempfile.TemporaryDirectory() as tmpdir:
            # تنزيل الملف
            file_path = Path(tmpdir) / (doc.file_name or "file")
            await message.download(file_name=str(file_path))

            full_text = ""

            if doc.mime_type == "application/pdf":
                # معالجة PDF: تحويل كل صفحة لصورة ثم OCR
                await status.edit_text("جاري تحويل PDF إلى صور... ⏳")
                image_paths = await pdf_to_images(str(file_path), tmpdir)

                if not image_paths:
                    await status.edit_text("❌ فشل في تحويل PDF.")
                    return

                await status.edit_text(f"جاري استخراج النص من {len(image_paths)} صفحة... ⏳")
                for img_path in image_paths:
                    page_text = await extract_text_from_image(img_path)
                    if page_text:
                        full_text += page_text + "\n\n"
            else:
                # معالجة الصورة مباشرة
                await status.edit_text("جاري استخراج النص... ⏳")
                full_text = await extract_text_from_image(str(file_path))

            full_text = full_text.strip()

            if not full_text:
                await status.edit_text("❌ لم يتم العثور على نص في الملف.")
                return

            await status.edit_text("جاري الترجمة... ⏳")
            translated = await translate_text_auto(full_text, user_id=message.from_user.id)

            await status.edit_text("✅ تم استخراج النص والترجمة بنجاح.")

            # إرسال النص الأصلي
            for part in split_long_text(full_text):
                await message.reply_text(f"📄 النص المستخرج:\n\n{part}")

            # إرسال الترجمة
            for part in split_long_text(translated):
                await message.reply_text(f"🌍 الترجمة:\n\n{part}")

    except Exception as e:
        logger.exception("خطأ في معالجة المستند: %s", e)
        await message.reply_text("❌ حدث خطأ أثناء المعالجة.")

document_handler = MessageHandler(document_cmd, filters.document)
