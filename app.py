import os
from flask import Flask, jsonify
import requests
import threading
import time
import datetime

app = Flask(__name__)

# Get environment variables - CORRECT NAMES
ALCHEMY_KEY = os.environ.get('ALCHEMY_API_KEY')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = os.environ.get('TELEGRAM_CHAT_ID')

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
        self.start_time = datetime.datetime.now()
        print("✅ Bot created successfully")
    
    def send_telegram(self, text):
        if not self.telegram_token or not self.telegram_chat:
            print("❌ Telegram credentials missing")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            payload = {
                'chat_id': self.telegram_chat,
                'text': text,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("✅ Telegram message sent")
                self.message_count += 1
                return True
            else:
                print(f"❌ Telegram error: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Telegram exception: {e}")
            return False
    
    def run(self):
        print("🔄 Bot main loop started")
        
        self.send_telegram("🚀 <b>Bot Started on Railway!</b>")
        
        counter = 1
        while True:
            try:
                time.sleep(300)
                
                heartbeat = f"""
⏰ <b>Bot Heartbeat #{counter}</b>
🕐 Time: {datetime.datetime.now().strftime('%H:%M:%S')}
📊 Messages sent: {self.message_count}
<i>Bot is running normally</i>
"""
                self.send_telegram(heartbeat)
                counter += 1
                
            except Exception as e:
                print(f"❌ Loop error: {e}")
                time.sleep(60)

bot = Bot()
thread = threading.Thread(target=bot.run, daemon=True)
thread.start()

@app.route('/')
def home():
    return jsonify({
        'status': 'ok',
        'bot': 'running',
        'messages': bot.message_count,
        'time': str(datetime.datetime.now())
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/debug')
def debug():
    return jsonify({
        'alchemy': '✅' if ALCHEMY_KEY else '❌',
        'telegram_token': '✅' if TELEGRAM_TOKEN else '❌',
        'telegram_chat': '✅' if TELEGRAM_CHAT else '❌',
        'messages': bot.message_count
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port)
