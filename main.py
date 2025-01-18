import streamlit as st
import yfinance as yf
from dotenv import load_dotenv
from llmhelper import llm  # Import the LLM instance from the llmhelper file
from langchain import PromptTemplate, LLMChain
import plotly.graph_objects as go
import random
import io


# Load environment variables (though this should be done in llmhelper already)
load_dotenv()

# Streamlit app UI
st.title("AI-Powered Business Insight Generator")

# Input section
st.sidebar.header("User Input")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", value="AAPL")
insight_topic = st.sidebar.selectbox(
    "Select Insight Topic",
    ["Motivation", "Stock Advice", "Business Strategy"]
)
generate_button = st.sidebar.button("Generate Insights")

# Fetch stock data
if generate_button:
    st.write(f"## Insights for {stock_symbol}")
    try:
        # Get stock market data using yfinance
        stock_data = yf.Ticker(stock_symbol)
        stock_price = stock_data.history(period="1d")['Close'][-1]
        st.write(f"### Current Price: ${stock_price:.2f}")

        # Placeholder for Alpha Vantage integration (will integrate later)
        st.info("Market stats will be fetched from Alpha Vantage in the next steps.")
    except Exception as e:
        st.error(f"Failed to fetch stock data: {e}")

    # Generate insights using the imported LLM and LangChain
    st.write(f"### Insights on: {insight_topic}")
    try:
        # Construct the prompt template
        prompt_template = PromptTemplate(
            input_variables=["topic", "symbol"],
            template=("Explain in layman's terms the {topic} insights for the stock market symbol {symbol}. "
                      "Keep the response concise and easy to understand for non-experts.")
        )
        
        # Create the LLMChain with the prompt and the GroqCloud LLM instance
        llm_chain = LLMChain(llm=llm, prompt=prompt_template)

        # Run the LLM chain to get the response
        llm_response = llm_chain.run({"topic": insight_topic, "symbol": stock_symbol})
        st.success(llm_response)

    except Exception as e:
        st.error(f"Failed to generate insights: {e}")


def create_price_chart(stock_data, stock_symbol):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close'],
        name='OHLC'
    ))
    fig.update_layout(
        title=f'{stock_symbol} Price Movement',
        template='plotly_white',
        xaxis_rangeslider_visible=False,
        height=500
    )
    return fig

# Inside the stock data fetching block
stock_data = yf.Ticker(stock_symbol)
stock_hist = stock_data.history(period="6mo")
st.plotly_chart(create_price_chart(stock_hist, stock_symbol), use_container_width=True)


QUOTES = {
    "Motivation": [
        "Success usually comes to those who are too busy to be looking for it. - Henry David Thoreau",
        "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    ],
    "Stock Advice": [
        "The stock market is filled with individuals who know the price of everything but the value of nothing. - Philip Fisher",
        "Risk comes from not knowing what you're doing. - Warren Buffett",
    ],
    "Business Strategy": [
        "In the middle of difficulty lies opportunity. - Albert Einstein",
        "The secret of business is to know something that nobody else knows. - Aristotle Onassis",
    ]
}

def display_quote(category):
    st.session_state["quote"] = random.choice(QUOTES.get(category, ["No quotes available."]))

# Initialize quote
if "quote" not in st.session_state:
    st.session_state["quote"] = random.choice(QUOTES.get(insight_topic, ["No quotes available."]))

# Display and cycle quotes
st.markdown(f"### Quote: {st.session_state['quote']}")
if st.button("Next Quote"):
    display_quote(insight_topic)



def generate_insights_report(stock_symbol, insights, quote):
    report = f"Insights for {stock_symbol}\n\n{insights}\n\nQuote: {quote}"
    return report

if generate_button:
    report = generate_insights_report(stock_symbol, llm_response, st.session_state["quote"])
    st.download_button("Download Insights", data=io.StringIO(report), file_name=f"{stock_symbol}_insights.txt")


# Footer
st.markdown(
    """
    ---
    *Powered by [LangChain](https://www.langchain.com/), [GroqCloud](https://groq.com/), and [yfinance](https://pypi.org/project/yfinance/).*
    """
)


