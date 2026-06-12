import asyncio
import logging
from pathlib import Path
from typing import List
from pdf2image import convert_from_path

logger = logging.getLogger(__name__)

async def pdf_to_images(pdf_path: str, output_dir: str) -> List[str]:
    """
    تحويل ملف PDF إلى قائمة صور (صفحة واحدة لكل صورة).
    يعمل في thread منفصل لأن convert_from_path دالة blocking.
    """
    try:
        # تشغيل التحويل في thread منفصل
        images = await asyncio.to_thread(
            convert_from_path,
            pdf_path,
            dpi=250,          # توازن بين الجودة والسرعة
            fmt="jpeg",
        )

        paths = []
        for i, img in enumerate(images, start=1):
            img_path = str(Path(output_dir) / f"page_{i}.jpg")
            img.save(img_path, "JPEG")
            paths.append(img_path)

        return paths

    except Exception as e:
        logger.exception("خطأ في تحويل PDF إلى صور: %s", e)
        return []
