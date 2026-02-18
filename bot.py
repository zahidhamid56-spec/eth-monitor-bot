import os
import time
import requests
from web3 import Web3

# Get environment variables
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not ALCHEMY_API_KEY or not TELEGRAM_TOKEN or not CHAT_ID:
    print("Missing environment variables!")
    exit()

# Connect to Ethereum using Alchemy
alchemy_url = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

if w3.is_connected():
    print("Connected to Ethereum")
else:
    print("Failed to connect to Ethereum")
    exit()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

0xCF37716b70688c687F615AEf0699611a8b681615
last_balance = None

while True:
    try:
        balance = w3.eth.get_balance(wallet_address)
        eth_balance = w3.from_wei(balance, 'ether')

        if eth_balance != last_balance:
            message = f"Wallet balance updated: {eth_balance} ETH"
            print(message)
            send_telegram_message(message)
            last_balance = eth_balance

        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(30)
