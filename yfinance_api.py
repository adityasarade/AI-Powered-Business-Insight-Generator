import yfinance as yf # type: ignore
import pandas as pd
from llmhelper import get_llm_response
import json

def format_large_number(number):
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.2f} Billion"
    elif number >= 1_000_000:
        return f"{number / 1_000_000:.2f} Million"
    else:
        return str(number)

def fetch_company_details(stock):
    """Fetch basic company information from yfinance."""
    try:
        info = stock.info

        # Extract relevant details
        company_details = {
            'longName': info.get('longName', 'N/A'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'marketCap': format_large_number(info.get('marketCap', 'N/A')),
            'peRatio': info.get('trailingPE', 'N/A'),
        }
        return company_details
    except Exception as e:
        print(f"Error fetching company details : {e}")
        return {
            'longName': 'N/A',
            'sector': 'N/A',
            'industry': 'N/A',
            'marketCap': 'N/A',
            'peRatio': 'N/A',
        }

def extract_news(company_name):

    stock = yf.Ticker(company_name)
    news = stock.news
    company_news=[]
    for item in news:
        title = item['content'].get('title', 'No title available')
        summary = item['content'].get('summary', 'No summary available')
        pub_date = item['content'].get('pubDate', 'Unknown date')
        
        company_news.append({
            'title': title,
            'summary': summary,
            'pubDate': pub_date
        })

    sorted_news = sorted(company_news, key=lambda x: x['pubDate'], reverse=True)
    
    # save in memory
    news_data = json.dumps(sorted_news, indent=4)
    return news_data

def get_news_sorted(news_data):

    news_data_loaded = json.loads(news_data)
    
    prompt = f"""
    Summarize the following news and provide important insights. 
    Focus on key events, trends, and any conclusions that can be drawn, 
    No Preamble:
    {news_data_loaded} 
    """
    response = get_llm_response(prompt)
    return response

def get_stock_data(interval,stock):
    if interval == "Daily":
        data = stock.history(period="1mo", interval="1d")
    elif interval == "Weekly":
        data = stock.history(period="6mo", interval="1wk")
    elif interval == "Monthly":
        data = stock.history(period="1y", interval="1mo")
    elif interval == "Yearly":
        data = stock.history(period="10y", interval="3mo")
    elif interval == "Max":
        data = stock.history(period="max", interval="3mo")
    return data

def calculate_technical_indicators(data):
    
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
    return data

def fetch_yfinance_data(company_name, interval):
    try:

        stock = yf.Ticker(company_name)
        current_price = stock.history(period="1d")

        # get stock history data
        data = get_stock_data(interval,stock)
        
        # Calculate technical indicators manually
        data = calculate_technical_indicators(data)

        # Sort and Select and return technical indicators
        data=data.sort_values(by='Date',ascending=False)
        indicators = data[["SMA", "EMA", "RSI", "MACD", "MACD_Signal", "Bollinger_High", "Bollinger_Low"]]
        data = data.drop(columns=["SMA", "EMA", "RSI", "MACD", "MACD_Signal", "Bollinger_High", "Bollinger_Low","Bollinger_Mid"])

        # Get news articles sorted aby LLM into json file
        news_data = extract_news(company_name)
        news_response = get_news_sorted(news_data)
        company_details = fetch_company_details(stock)
        return data, indicators, current_price, news_response, company_details

    except Exception as e:
        print(e)
        return None, None, None, None
    