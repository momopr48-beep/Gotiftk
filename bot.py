import os
import telebot
from google import genai

# جلب المفاتيح بأمان تام من متغيرات البيئة في المنصة
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# إعداد عميل چيميني الحديث ونموذج الفلاش
client = genai.Client(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "عذراً، لم أستطع توليد رد.")
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")

print("البوت يعمل الآن بكفاءة وأمان تام...")
bot.polling(none_stop=True)
