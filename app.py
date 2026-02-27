import os
from flask import Flask, jsonify
import requests
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Get environment variables - FIXED NAMES
ALCHEMY_KEY = os.environ.get('ALCHEMY_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.environ.get('TELEGRAM_CHAT_ID') # Fixed this line!

print("=" * 60)
print("🤖 BOT STARTING UP")
print("=" * 60)
print(f"ALCHEMY_KEY: {'✅ FOUND' if ALCHEMY_KEY else '❌ MISSING'}")
print(f"TELEGRAM_TOKEN: {'✅ FOUND' if TELEGRAM_TOKEN else '❌ MISSING'}")
print(f"TELEGRAM_CHAT: {'✅ FOUND' if TELEGRAM_CHAT else '❌ MISSING'}")
print("=" * 60)

class Bot:
    def __init__(self):
        self.alchemy = ALCHEMY_KEY
        self.telegram_token = TELEGRAM_TOKEN
        self.telegram_chat = TELEGRAM_CHAT
        self.message_count = 0
        self.start_time = datetime.now()
        print("✅ Bot created")
    
    def send_telegram(self, text):
        if not self.telegram_token or not self.telegram_chat:
            print("❌ Telegram credentials missing")
            return
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            requests.post(url, json={
                'chat_id': self.telegram_chat,
                'text': text,
                'parse_mode': 'HTML'
            })
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
    return jsonify({
        'status': 'ok',
        'bot': 'running',
        'time': str(datetime.now())
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/debug')
def debug():
    return jsonify({
        'alchemy': '✅' if ALCHEMY_KEY else '❌',
        'telegram_token': '✅' if TELEGRAM_TOKEN else '❌',
        'telegram_chat': '✅' if TELEGRAM_CHAT else '❌'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Starting on port {port}")
    app.run(host='0.0.0.0', port=port)

