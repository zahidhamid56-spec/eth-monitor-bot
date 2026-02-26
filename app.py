import os
from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Get environment variables
ALCHEMY_KEY = os.environ.get('ALCHEMY_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.environ.get('TELEGRAM_CHAT_ID')

print("=" * 50)
print("🚀 BOT STARTING")
print("=" * 50)
print(f"ALCHEMY: {'✅' if ALCHEMY_KEY else '❌'}")
print(f"TELEGRAM TOKEN: {'✅' if TELEGRAM_TOKEN else '❌'}")
print(f"TELEGRAM CHAT: {'✅' if TELEGRAM_CHAT else '❌'}")
print("=" * 50)

class Bot:
    def __init__(self):
        self.alchemy = ALCHEMY_KEY
        self.telegram_token = TELEGRAM_TOKEN
        self.telegram_chat = TELEGRAM_CHAT
        print("✅ Bot created")
    
    def send_telegram(self, text):
        if not self.telegram_token or not self.telegram_chat:
            print("❌ No telegram")
            return
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            requests.post(url, json={'chat_id': self.telegram_chat, 'text': text})
            print("✅ Telegram sent")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        print("🔄 Bot running")
        self.send_telegram("🚀 Bot started on Railway!")
        while True:
            time.sleep(60)

bot = Bot()
thread = threading.Thread(target=bot.run, daemon=True)
thread.start()

@app.route('/')
def home():
    return jsonify({'status': 'ok'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
