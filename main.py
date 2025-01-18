import streamlit as st
import yfinance as yf
from dotenv import load_dotenv
from llmhelper import llm  # Import the LLM instance from the llmhelper file
from langchain import PromptTemplate, LLMChain

# Load environment variables (though this should be done in llmhelper already)
load_dotenv()

# Streamlit app UI
st.title("AI-Powered Business Insight Generator")
st.subheader("Get business insights, stock trends, and motivational wisdom")

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
            template=("Provide a {topic} insight related to the stock market symbol {symbol}. "
                      "The response should be insightful, brief, and practical.")
        )
        
        # Create the LLMChain with the prompt and the GroqCloud LLM instance
        llm_chain = LLMChain(llm=llm, prompt=prompt_template)

        # Run the LLM chain to get the response
        llm_response = llm_chain.run({"topic": insight_topic, "symbol": stock_symbol})
        st.success(llm_response)

    except Exception as e:
        st.error(f"Failed to generate insights: {e}")

# Footer
st.markdown(
    """
    ---
    *Powered by [LangChain](https://www.langchain.com/), [GroqCloud](https://groq.com/), and [yfinance](https://pypi.org/project/yfinance/).*
    """
)
