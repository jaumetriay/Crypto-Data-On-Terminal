import os
import random
import time
import json
import subprocess
from collections import defaultdict
import math

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

# Data storage
data_points = defaultdict(lambda: defaultdict(list))

def print_unicode_plot(data, currency, window_size=50):
    for crypto, values in data.items():
        if currency in values:
            print(f"{CRYPTO_COLORS[crypto]}{crypto} {currency} trend:")
            
            # Use only the last 'window_size' values
            recent_values = values[currency][-window_size:]
            
            # Determine the y-axis scale
            max_value = max(recent_values)
            min_value = min(recent_values)
            value_range = max_value - min_value

            # Ensure a minimum range to avoid division by zero
            if value_range == 0:
                value_range = 1

            # Create the plot
            height = 10
            width = len(recent_values)
            plot = [[' ' for _ in range(width)] for _ in range(height)]
            
            # Unicode box-drawing characters
            chars = '▁▂▃▄▅▆▇█'
            
            for i, value in enumerate(recent_values):
                # Ensure that even the minimum value gets a character
                y = max(0, min((value - min_value) / value_range * (height - 1), height - 1))
                idx = int(y)
                frac = y - idx
                
                # Always plot at least the minimum character
                plot[height - 1 - idx][i] = chars[max(0, min(int(frac * 8), 7))]
                
                # Fill in the column below the top character
                for j in range(height - idx, height):
                    plot[j][i] = chars[-1]
            
            # Print the plot
            for row in plot:
                print(''.join(row))
            
            # Print x-axis
            print('─' * width)
            
            # Print y-axis labels
            print(f"Max: {max_value:.4f}")
            print(f"Min: {min_value:.4f}")
            
            print(CRYPTO_COLORS['RESET'])
            print()  # Add a blank line between plots

iteration = 0
while EXIT == 0:
    try:
        iteration += 1
        for name, color in CRYPTO_COLORS.items():
            if name == 'RESET':
                continue  # Skip the RESET color entry
            
            out = url + name
            
            # For EUR
            result = subprocess.run(["curl", "-s", out+eur], capture_output=True, text=True)
            data = json.loads(result.stdout)
            eur_value = float(data['data']['amount'])
            data_points[name]['EUR'].append(eur_value)
            print(f"\n{color} ==> {name}-EUR: {eur_value}{CRYPTO_COLORS['RESET']}")

            # For USD
            result = subprocess.run(["curl", "-s", out+usd], capture_output=True, text=True)
            data = json.loads(result.stdout)
            usd_value = float(data['data']['amount'])
            data_points[name]['USD'].append(usd_value)
            print(f"{color} ==> {name}-USD: {usd_value}{CRYPTO_COLORS['RESET']}")

        # Print Unicode plots every 5 iterations
        if iteration % 1 == 0:
            #os.system('clear')  # Clear the terminal
            print_unicode_plot(data_points, 'EUR')
            print_unicode_plot(data_points, 'USD')

        #time.sleep(0.1)  # Random delay between 1 and 5 seconds

    except KeyboardInterrupt:
        print("\nExiting...")
        EXIT = 1
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)  # Wait for 5 seconds before trying

