import asyncio
import logging
from typing import List
from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator

logger = logging.getLogger(__name__)

# تخزين إعدادات الترجمة لكل مستخدم في الذاكرة
_user_lang_settings: dict = {}

# الحد الأقصى لـ GoogleTranslator في كل طلب
_GOOGLE_CHUNK = 4500

def get_user_lang(user_id: int) -> str:
    return _user_lang_settings.get(user_id, "ar-en")

def toggle_user_lang(user_id: int) -> str:
    current = _user_lang_settings.get(user_id, "ar-en")
    new_val = "en-ar" if current == "ar-en" else "ar-en"
    _user_lang_settings[user_id] = new_val
    return new_val

def split_long_text(text: str, max_length: int = 4096) -> List[str]:
    """
    تقسيم النص الطويل إلى أجزاء لا تتجاوز max_length
    """
    parts = []
    while len(text) > max_length:
        parts.append(text[:max_length])
        text = text[max_length:]
    if text:
        parts.append(text)
    return parts

def _detect_lang(text: str) -> str:
    """
    اكتشاف لغة النص — يرجع 'ar' أو 'en' أو 'unknown'
    """
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def _translate_chunk(chunk: str, source: str, target: str) -> str:
    """
    ترجمة جزء واحد من النص (blocking — يُستدعى من thread)
    """
    return GoogleTranslator(source=source, target=target).translate(chunk)

async def translate_text_auto(text: str, user_id: int) -> str:
    """
    ترجمة النص كاملاً مع تقسيمه إذا تجاوز حد GoogleTranslator
    """
    try:
        detected = _detect_lang(text)

        if detected == "ar":
            source, target = "ar", "en"
        elif detected == "en":
            source, target = "en", "ar"
        else:
            # استخدام إعداد المستخدم عند عدم التعرف على اللغة
            pref = get_user_lang(user_id)
            source, target = ("ar", "en") if pref == "ar-en" else ("en", "ar")

        # تقسيم النص إلى أجزاء لا تتجاوز حد GoogleTranslator
        chunks = split_long_text(text, max_length=_GOOGLE_CHUNK)
        translated_parts = []

        for chunk in chunks:
            part = await asyncio.to_thread(_translate_chunk, chunk, source, target)
            translated_parts.append(part)

        return "\n".join(translated_parts)

    except Exception as e:
        logger.exception("خطأ في الترجمة: %s", e)
        return "❌ حدث خطأ أثناء الترجمة."
