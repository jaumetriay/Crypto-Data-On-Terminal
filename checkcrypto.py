import os
import random
import time


#outputs a list of data related to the cryptos listed  below
#to kill process ctrl + c 
cryptoList = ['BTC','ETH','LTC','BCH']

#gets the api info
url="https://api.coinbase.com/v2/prices/"
eur="-EUR/buy"
usd="-USD/buy"
out = ""
EXIT=0

while EXIT == 0:
	try:
		for name in cryptoList:
			out = url + name
			os.system("curl " + out+eur)
			print("\b")
			os.system("curl " + out+usd)
			print("\n")

			time.sleep(1)
			if random.randint(0,10) > 7:
				os.system("fortune") #displays a pseudorandom sentence, just for the comedic effect, ha ha. 
				print("\n")

		
	except KeyboardInterrupt:
		EXIT=1
