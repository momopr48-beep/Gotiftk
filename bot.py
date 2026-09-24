import telebot
from google import genai

TELEGRAM_BOT_TOKEN = "8996016776:AAETM1FLdxBuhF_djytNahSu7xJPu4ZhnmM"
GEMINI_API_KEY = "AQ.Ab8RN6IXrq9-JK_ldpmPP_3j30bL2j-AKQCY0_UdPqJfLuSR_w"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"عذراً، حدث خطأ: {e}")

print("Bot is running...")
bot.infinity_polling()
