import os
import telebot
from google import genai

# قراءة التوكن والمفتاح من متغيرات البيئة بأمان
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# تهيئة عميل چيميني الجديد
client = genai.Client(api_key=GEMINI_API_KEY)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # استخدام النموذج الحديث gemini-2.5-flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"صار خطأ يا غالي: {str(e)}")

print("البوت يعمل الآن بالمكتبة الجديدة...")
bot.polling()
