import talib as ta
import requests,time
import numpy as np

url = "https://api.coindcx.com/exchange/v1/derivatives/futures/data/active_instruments"

response = requests.get(url)
symbol = response.json()

def crypto_screener(symbol):

  url = "https://public.coindcx.com/market_data/candlesticks"
  now = time.time()
  current_time = int(now)
  seconds_in_day = 60 * 60 * 48
  start_date = now - (seconds_in_day)

  query_params = {
      "pair": symbol,
      "from": start_date,
      "to": current_time,
      "resolution": "15",  # '1' OR '5' OR '60' OR '1D'
      "pcode": "f"
  }
  response = requests.get(url, params=query_params)
  data = response.json()
  data = data["data"]
  close= np.array([item['close'] for item in data])
  open = np.array([item['open'] for item in data])
  low = np.array([item['low'] for item in data])
  volume = np.array([item['volume'] for item in data])

  try:
      sma50 = ta.SMA(close, timeperiod=50)
      rsi =ta.RSI(close, timeperiod=14)

      # Check conditions
      if (close[-2] > sma50[-2] and
          low[-2] < sma50[-2] and
          close[-2] > open[-2] and  # Green candle
          rsi[-2] >= 57 and
          volume[-2] > volume[-3]):
        print(f"{symbol} meets all buy conditions!")
  except:
     pass
            
for i in symbol:
    crypto_screener(i)