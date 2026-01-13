import requests

BOT_TOKEN = "8273425790:AAHT7xQde08Lnlac23XT6raI9-2yfNLfNbM"
CHAT_ID = 1993340499


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": f"⏰ AI Assistant Reminder:\n{message}"
    }
    r = requests.post(url, data=payload)
    print("Telegram response:", r.status_code, r.text)
