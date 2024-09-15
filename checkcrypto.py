import os
import random
import time
import json
import subprocess

# ANSI color codes and cryptocurrencies
CRYPTO_COLORS = {
    'BTC': '\033[38;5;208m',  # Orange
    'ETH': '\033[34m',        # Blue
    'LTC': '\033[33m',        # Yellow
    'BCH': '\033[38;5;130m',  # Brown
    'RESET': '\033[0m'        # Reset to default color
}

# API URL components
url = "https://api.coinbase.com/v2/prices/"
eur = "-EUR/buy"
usd = "-USD/buy"

EXIT = 0

while EXIT == 0:
    try:
        for name, color in CRYPTO_COLORS.items():
            if name == 'RESET':
                continue  # Skip the RESET color entry
            
            out = url + name
            
            # For EUR
            result = subprocess.run(["curl", "-s", out+eur], capture_output=True, text=True)
            data = json.loads(result.stdout)
            print(f"\n{color} ==> {name}-EUR: {data['data']['amount']}{CRYPTO_COLORS['RESET']}")

            # For USD
            result = subprocess.run(["curl", "-s", out+usd], capture_output=True, text=True)
            data = json.loads(result.stdout)
            print(f"{color} ==> {name}-USD: {data['data']['amount']}{CRYPTO_COLORS['RESET']}")
		
            time.sleep(0.1)
            if random.randint(0,10) > 9:
                print("\n")
                os.system("fortune")
                print("\n")


    except KeyboardInterrupt:
        EXIT = 1
