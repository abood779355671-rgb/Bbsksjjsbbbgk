#!/bin/bash
# سكريبت تثبيت ونشر بوت OCR Translate على Ubuntu VPS

set -e

echo "=== 1. تحديث النظام وتثبيت المتطلبات ==="
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3-pip poppler-utils git

echo "=== 2. نسخ المشروع (عدّل الرابط حسب رفعك على GitHub) ==="
# git clone https://github.com/YOUR_USER/ocr_translate_bot.git
# cd ocr_translate_bot

echo "=== 3. إنشاء البيئة الافتراضية وتثبيت المكتبات ==="
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 4. إعداد ملف .env ==="
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✏️  عدّل ملف .env وأضف بياناتك:"
    echo "   nano .env"
fi

echo "=== 5. تثبيت خدمة systemd ==="
sudo cp ocr-bot.service /etc/systemd/system/ocr-bot.service
sudo systemctl daemon-reload
sudo systemctl enable ocr-bot
sudo systemctl start ocr-bot

echo ""
echo "✅ تم النشر بنجاح!"
echo "📋 عرض الـ logs: journalctl -u ocr-bot -f"
echo "🔄 إعادة التشغيل: sudo systemctl restart ocr-bot"
echo "⛔ إيقاف البوت:  sudo systemctl stop ocr-bot"
