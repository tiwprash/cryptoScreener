import requests # Install requests module first.
import requests
import talib as ta
import numpy as np
import pandas as pd

url = "https://api.coindcx.com/exchange/v1/derivatives/futures/data/active_instruments"

response = requests.get(url)
symbol = response.json()

import time
now = time.time()
current_time = int(now)
seconds_in_day = 60 * 60 * 48
start_date = now - (seconds_in_day)

def candelstick(symbol,interval):
    try:
        url = "https://public.coindcx.com/market_data/candlesticks"
        query_params = {
            "pair": symbol,
            "from": start_date,
            "to": current_time,
            "resolution": interval,  # '1' OR '5' OR '60' OR '1D'
            "pcode": "f"
        }
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            # print(data)
            data = data['data']
        else:
            print(f"Error: {response.status_code}, {response.text}")

        close = np.array([item['close'] for item in data],dtype=np.double)
        volume = np.array([item['volume'] for item in data],dtype=np.double)
        high = np.array([item['high'] for item in data],dtype=np.double)

        # Calculate the 5 EMA and 50 SMA
        ema = ta.EMA(close, timeperiod=5)
        sma = ta.SMA(close, timeperiod=50)

        # Function to calculate the highest value of the last 5 values
        highest_number = close[-5:]
        latest_high = max(highest_number)
    except:
        pass

    # Strategy conditions
    try:
        if (ema[-2] < sma[-2]) and (latest_high> sma[-2]) and (close[-2] < ema[-2]):
            print(f"Sell {symbol}")
    except:
        pass


for i in symbol:
    candelstick(i,15)
