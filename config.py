import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# تحميل المتغيرات من ملف .env
load_dotenv()

@dataclass
class Settings:
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str
    MAX_FILE_SIZE: int = field(default=20 * 1024 * 1024)  # 20 ميجابايت

def _get_env_int(key: str) -> int:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"المتغير {key} غير موجود في .env")
    return int(value)

def _get_env_str(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise ValueError(f"المتغير {key} غير موجود في .env")
    return value

settings = Settings(
    API_ID=_get_env_int("API_ID"),
    API_HASH=_get_env_str("API_HASH"),
    BOT_TOKEN=_get_env_str("BOT_TOKEN"),
)
