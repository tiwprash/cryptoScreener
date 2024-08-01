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

def statergy1(symbol, interval):
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
            data = data['data']
        else:
            print(f"Error: {response.status_code} {symbol}, {response.text}")
            return

        close = np.array([item['close'] for item in data], dtype=np.double)
        low = np.array([item['low'] for item in data], dtype=np.double)

        # Calculate 5 EMA and 50 SMA
        ema_5 = ta.EMA(close, timeperiod=5)
        sma_50 = ta.SMA(close, timeperiod=50)

        if len(ema_5) < 2 or len(sma_50) < 2:
            print(f"Not enough data to calculate EMA and SMA for {symbol}")
            return

        # Check the sell condition
        if (low[-3] > ema_5[-2]) and (ema_5[-2] < sma_50[-2]) and (close[-2] < low[-3]):
            print(f"{symbol} sell condition met")

    except Exception as e:
        print(f"Error processing {symbol}: {e}")

# Other functions and main script logic remain the same

for i in symbol:
    statergy1(i,15)

for i in symbol:
    statergy1(i,30)

for i in symbol:
    statergy1(i,60)

