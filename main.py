import streamlit as st
import pandas as pd
from yfinance_api import fetch_yfinance_data
from llmhelper import get_llm_response  # Import the LLM response function
import plotly.graph_objects as go  # type: ignore
import json

with open('companies.json', 'r') as f:
    data = json.load(f)

# Streamlit App
st.title("AI-Powered Stock Insights")

# Dropdown for company and stock exchange and interval
exchange = st.selectbox("Select Stock Exchange", list(data.keys()))
company = st.selectbox("Select Company", list(data[exchange].keys()))
company_name = data[exchange][company]
interval = st.selectbox("Select Interval", ["Daily", "Weekly", "Monthly", "Yearly", "Max"])

# Fetch Data
if st.button("Fetch Stock Data"):
    stock_data, indicators, current_price, news_response = fetch_yfinance_data(company_name, interval)

    if stock_data is not None:
        # Plot Candle Chart using Plotly
        fig = go.Figure(data=[go.Candlestick(
            x=stock_data.index,
            open=stock_data['Open'],
            high=stock_data['High'],
            low=stock_data['Low'],
            close=stock_data['Close'],
            increasing_line_color='green',
            decreasing_line_color='red'
        )])

        fig.update_layout(
            title=f"Candlestick Chart for {company_name}",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig)
        # Display Historical Stock Data
        st.write("### Historical Stock Data")
        styled_stock_data = stock_data.style.set_table_styles(
            [{"selector": "th", "props": [("text-align", "center")]}]
        ).set_properties(**{"text-align": "center"})
        st.dataframe(styled_stock_data, height=200, use_container_width=True)

        # Display Technical Indicators
        st.write("### Technical Indicators")
        st.dataframe(indicators, height=200, use_container_width=True)

        # Display tooltips in an expander
        st.write("### Indicator Details")
        with st.expander("See Indicator Details"):
            for col, desc in {
                "SMA": "Simple Moving Average (SMA) is the average of the closing prices for a specified period. It smooths price data to help identify trends.",
                "EMA": "Exponential Moving Average (EMA) gives more weight to recent prices, and reacts more quickly to price changes than the SMA.",
                "RSI": "The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100.",
                "MACD": "The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price."
                # Add more indicators and descriptions as needed
            }.items():
                st.markdown(f"**{col}**: {desc}")


        # Generate insights using LLM
        prompt = f"""
        Analyze the stock performance of {company_name} over the {interval} period.
        Check the current news of the company and based on it give insights: {news_response}.
        Also give a company overview first and then start the following:
        Use the following technical indicators: {indicators}.
        Provide actionable insights and a summary for an investor.
        Answer whether one should buy this stock or not.
        Analyze it based on data and do not show disclaimers like "This analysis is based on technical indicators and should not be considered as investment advice."
        Be specific in your answer and do not generalize the opinion. Explain the recommendation in simple language.
        Also mention until when to wait, if you think one should not buy that stock now.
        Use points for readability and clarity.
        """
        insights = get_llm_response(prompt)
        st.write("### AI Insights")
        st.write(insights)
    else:
        st.error("Failed to fetch stock data. Check the company name or data source.")
