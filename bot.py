import telebot
import google.generativeai as genai

TELEGRAM_BOT_TOKEN = "8996016776:AAETM1FLdxBuhF_djytNahSu7xJPu4ZhnmM"
GEMINI_API_KEY = "AQ.Ab8RN6IXrq9-JK_ldpmPP_3j30bL2j-AKQCY0_UdPqJfLuSR_w"

# إعداد مفتاح جوجل
genai.configure(api_key=GEMINI_API_KEY)

# استخدام النموذج المعتمد
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"عذراً، حدث خطأ: {e}")

print("Bot is running...")
bot.infinity_polling()
