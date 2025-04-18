import requests
from fake_useragent import UserAgent
import time
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup

# === CONFIG ===
BOT_TOKEN = '8015910781:AAFO6EIR9BS3GnYqIaU8-2I8Jc79DhGLKPg'
CHAT_ID = '1735180463'
URL = 'https://tixel.com/hr/music-tickets/2025/07/09/love-international-2025/'

# === TELEGRAM ALERT ===
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"❌ Telegram send failed: {e}")


# === MAIN MONITOR LOOP ===
ua = UserAgent()
prev_hash = None

while True:
    try:
        headers = {
            'User-Agent': ua.random
        }

        response = requests.get(URL, headers=headers)

        if response.status_code == 200:
            content = response.text
            # Inside your loop, after fetching content:
            soup = BeautifulSoup(response.text, "html.parser")

            # Option A: Just the visible text (ignores scripts, meta, etc.)
            visible_text = soup.get_text(separator=' ', strip=True)

            # Option B: OR you can narrow down to specific divs if needed
            # e.g., visible_text = soup.select_one("main").get_text()

            current_hash = hashlib.md5(visible_text.encode('utf-8')).hexdigest()

            # current_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Status: 200 | Hash: {current_hash}")

            if prev_hash and current_hash != prev_hash:
                print("🔔 Change detected! Sending alert.")
                send_telegram_alert(f"🚨 Website content changed on Tixel!\n🔗 {URL}")
            elif not prev_hash:
                print("✅ First fetch. Hash stored.")

            prev_hash = current_hash

        else:
            print(f"⚠️ [{response.status_code}] Non-OK response.")
            send_telegram_alert(f"⚠️ [{response.status_code}] Unable to reach site: {URL}")

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        send_telegram_alert(f"⚠️ Exception during check: {e}")

    time.sleep(15)  # 1-minute interval
