import asyncio
import logging
import easyocr

logger = logging.getLogger(__name__)

# تهيئة قارئ OCR مرة واحدة عند بدء التشغيل (عملية ثقيلة)
_reader = easyocr.Reader(["ar", "en"], gpu=False)

async def extract_text_from_image(image_path: str) -> str:
    """
    استخراج النص من صورة باستخدام EasyOCR.
    يعمل في thread منفصل لأن easyocr دالة blocking.
    """
    try:
        # تشغيل OCR في thread منفصل حتى لا يعطل event loop
        results = await asyncio.to_thread(
            _reader.readtext, image_path, detail=0, paragraph=True
        )
        text = "\n".join(results).strip()
        return text
    except Exception as e:
        logger.exception("خطأ في OCR: %s", e)
        return ""
