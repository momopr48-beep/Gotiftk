import os
import telebot
import google.generativeai as genai

# توكن البوت ومفتاح چيميني جاهزة ومضبوطة
TELEGRAM_BOT_TOKEN = "8996016776:AAETM1FLdxBuhF_djytNahSu7xJPu4ZhnmM"
GEMINI_API_KEY = "AQ.Ab8RN6IQFfkxmTkyZUZy6xEkxJGtkJY9esnQTmeEbDF9qxAbcw"

# إعداد مكتبة چيميني
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"صار خطأ يا غالي: {str(e)}")

print("البوت يشتغل الآن...")
bot.polling()
