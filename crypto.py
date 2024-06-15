import talib as ta
import requests,time
import numpy as np

# Telegram bot token and chat ID
bot_token = '6876777402:AAFv0NLr9-3dmXpaaokMeFzE8bAA4vVUoCk'  # Replace with your bot token
chat_id = "1432191600"  # Replace with your chat ID

# Function to send message
def send_telegram_message(message):
    try:
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        params = {
            'chat_id': chat_id,
            'parse_mode': 'HTML',
            'text': message
        }
        response = requests.get(send_text, params=params)
        response.raise_for_status()  # Raise an error for bad response status (4xx or 5xx)
        # print("Message sent successfully:", response.json())
        return True
    except requests.exceptions.RequestException as e:
        # print("Error sending message:", e)
        # print("Response content:", response.content.decode("utf-8"))  # Print the response content for debugging
        return False



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
  high = np.array([item['high'] for item in data])

  try:
      sma50 = ta.SMA(close, timeperiod=50)
      rsi =ta.RSI(close, timeperiod=14)

      # Check conditions
      if (close[-2] > sma50[-2] and
          low[-2] < sma50[-2] and
          close[-2] > open[-2] and  # Green candle
          rsi[-2] >= 57 and
          volume[-2] > volume[-3]):
        print(f"{symbol} meets all buy conditions! RSI is {rsi[-2]}")
        message = f"{symbol} meets all buy conditions! RSI is {rsi[-2]}"
        send_telegram_message(message)
        
      elif (close[-2] < sma50[-2] and
          high[-2] < sma50[-2] and
          close[-2] < open[-2] and  # red candle
          rsi[-2] <= 43 and
          volume[-2] > volume[-3]):
        print(f"{symbol} meets all sell conditions! RSI is {rsi[-2]}")
        message = f"{symbol} meets all sell conditions! RSI is {rsi[-2]}"
        send_telegram_message(message)
        
      
  except:
     pass
  
while True:           
    for i in symbol:
        crypto_screener(i)
    time.sleep(800)
    
