import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

import logging
import os
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, idle
from config import settings
from handlers.start import start_handler, help_handler, lang_handler
from handlers.document import document_handler
from handlers.photo import photo_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# ─── HTTP Server بسيط يرد على Render ───────────────────────────
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running OK")

    def log_message(self, format, *args):
        pass  # إيقاف logs الـ HTTP حتى لا تزعج

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logging.info(f"Health server running on port {port}")
    server.serve_forever()

# ─── البوت ─────────────────────────────────────────────────────
async def main() -> None:
    # تشغيل HTTP server في thread منفصل
    thread = Thread(target=run_health_server, daemon=True)
    thread.start()

    app = Client(
        name="ocr_translate_bot",
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        bot_token=settings.BOT_TOKEN,
        workers=4
    )

    app.add_handler(start_handler)
    app.add_handler(help_handler)
    app.add_handler(lang_handler)
    app.add_handler(document_handler)
    app.add_handler(photo_handler)

    await app.start()
    logging.info("✅ البوت يعمل الآن...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
