import yfinance as yf
import pandas as pd

def fetch_yfinance_data(company_name, interval):
    try:
        stock = yf.Ticker(company_name)
        current_price = stock.history(period="1d")
        if interval == "Daily":
            data = stock.history(period="1mo", interval="1d")
        elif interval == "Weekly":
            data = stock.history(period="6mo", interval="1wk")
        elif interval == "Monthly":
            data = stock.history(period="1y", interval="1mo")
        elif interval == "Yearly":
            data = stock.history(period="10y", interval="1mo")

        # Calculate technical indicators manually

        # Simple Moving Average (SMA)
        data['SMA'] = data['Close'].rolling(window=14).mean()

        # Exponential Moving Average (EMA)
        data['EMA'] = data['Close'].ewm(span=14, adjust=False).mean()

        # Relative Strength Index (RSI)
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # Moving Average Convergence Divergence (MACD)
        ema12 = data['Close'].ewm(span=12, adjust=False).mean()
        ema26 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = ema12 - ema26
        data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

        # Bollinger Bands
        data['Bollinger_Mid'] = data['Close'].rolling(window=20).mean()
        data['Bollinger_High'] = data['Bollinger_Mid'] + 2 * data['Close'].rolling(window=20).std()
        data['Bollinger_Low'] = data['Bollinger_Mid'] - 2 * data['Close'].rolling(window=20).std()

        # Select and return technical indicators
        data=data.sort_values(by='Date',ascending=False)
        indicators = data[["SMA", "EMA", "RSI", "MACD", "MACD_Signal", "Bollinger_High", "Bollinger_Low"]]
        return data, indicators, current_price

    except Exception as e:
        print(e)
        return None, None