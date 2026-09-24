import time
import requests

GEMINI_API_KEY = "AQ.Ab8RN6IXrq9-JK_ldpmPP_3j30bL2j-AKQCY0_UdPqJfLuSR_w"
TELEGRAM_TOKEN = "8996016776:AAETM1FLdxBuhF_djytNahSu7xJPu4ZhnmM"

BOT_USERNAME = None

def get_bot_info():
    global BOT_USERNAME
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
        res = requests.get(url).json()
        if res.get("ok"):
            BOT_USERNAME = res["result"].get("username")
    except:
        pass

def ask_ai(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    
    full_prompt = f"أنت مساعد ذكي ولطيف، وتتحدث حصرياً باللهجة العراقية الطبيعية. أجب على السؤال الآتي بأسلوب عراقي ودود وبدون تكلف: {prompt}"
    
    data = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=15)
            res_json = response.json()
            
            if "candidates" in res_json:
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
            elif "error" in res_json:
                err_msg = res_json['error'].get('message', '')
                if "high demand" in err_msg.lower():
                    time.sleep(2)
                    continue
                else:
                    return f"خطأ من قِبل جوجل: {err_msg}"
            else:
                return "صار عندي خلل بالرد، بس سامعك سولفلي!"
        except Exception as e:
            time.sleep(1)
            
    return "والله يا غالي السيرفر عليه ضغط قوي هسة، اتركني ثواني وارجع راسلني!"

get_bot_info()
offset = 0

while True:
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates?offset={offset}&timeout=10"
        res = requests.get(url).json()
        for update in res.get("result", []):
            offset = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                msg = update["message"]
                chat = msg["chat"]
                chat_type = chat.get("type", "private")
                text = msg["text"]
                chat_id = chat["id"]
                
                should_reply = False
                
                if chat_type == "private":
                    should_reply = True
                elif chat_type in ["group", "supergroup"]:
                    if "reply_to_message" in msg:
                        replied_from = msg["reply_to_message"].get("from", {})
                        if replied_from.get("is_bot") and replied_from.get("username") == BOT_USERNAME:
                            should_reply = True
                    if BOT_USERNAME and f"@{BOT_USERNAME.lower()}" in text.lower():
                        should_reply = True
                
                if should_reply:
                    reply_text = ask_ai(text)
                    send_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
                    requests.post(send_url, json={"chat_id": chat_id, "text": reply_text, "reply_to_message_id": msg["message_id"]})
                    
    except Exception as e:
        time.sleep(1)
