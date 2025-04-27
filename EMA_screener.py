import talib as ta
import requests
import time
import numpy as np

# Fetch futures instruments from CoinDCX
url = "https://api.coindcx.com/exchange/v1/derivatives/futures/data/active_instruments"
response = requests.get(url)
symbols_data = response.json()


def crypto_screener(symbol,interval,hours):
    url = "https://public.coindcx.com/market_data/candlesticks"
    now = time.time()
    current_time = int(now)
    seconds_in_day = 60 * 60 * hours  # last 60 hours
    start_date = now - seconds_in_day

    query_params = {
        "pair": symbol,
        "from": start_date,
        "to": current_time,
        "resolution": interval,  # 15-minute candles
        "pcode": "f"
    }
    

    try:
        response = requests.get(url, params=query_params)
        if response.status_code == 200:
            data = response.json().get("data", [])
    
        close = np.array([float(item['close']) for item in data])
        open_ = np.array([float(item['open']) for item in data])
        low = np.array([float(item['low']) for item in data])
        high = np.array([float(item['high']) for item in data])
        volume = np.array([float(item['volume']) for item in data])

        ema_4 = ta.EMA(high, timeperiod=4)
        sma_21 = ta.SMA(close, timeperiod=21)

        i = -2  # current candle
        j = -3  # previous candle

        if (
            ema_4[i] > sma_21[i] and
            high[j] < ema_4[j] and
            close[i] > high[j]
        ):
            print(f"🟢 MATCH: {symbol}")

        else:
            print(f"{symbol}-- {close[-2]}")

    except Exception as e:
        print(f"⚠️ Error for {symbol}: {e}")
    

# Run screener for all symbols
for symbol in symbols_data:
    crypto_screener(symbol,interval="60",hours = 24)  #interval "15" or "30" or "60" or "2h" or "4h" or "1d"
                                                        # hours should be based on Interval
                                                        #for 60 or below hours will be 24
                                                        #2h = 48 and 4h = 92 and 1d = 528
                                                        #2h Interval is not working as exchange is not providing 2 hours data.

print("Screening completed") # This statment will appear once the program is completed.
