import streamlit as st
import pandas as pd
from yfinance_api import fetch_yfinance_data
from llmhelper import get_llm_response  # Import the LLM response function
import plotly.graph_objects as go


# Streamlit App
st.title("AI-Powered Stock Insights")

# Dropdown for company and data source
company_name = st.text_input("Enter Company Name:")
interval = st.selectbox("Select Interval", ["Daily", "Weekly", "Monthly", "Yearly"])

st.markdown("""
        <style>
            .title {
                color: green;
                font-size: 30px;
                font-weight: bold;
            }
            .metric-value {
                font-size: 20px;
                color: #333;
                font-weight: bold;
            }
            .custom-table {
                border-collapse: collapse;
                width: 100%;
            }
            .custom-table th, .custom-table td {
                padding: 10px;
                text-align: left;
                border: 1px solid #ddd;
            }
            .custom-table th {
                background-color: #f2f2f2;
            }
        </style>
    """, unsafe_allow_html=True)
# Fetch Data
if st.button("Fetch Stock Data"):
    stock_data, indicators, current_price = fetch_yfinance_data(company_name, interval)

    if stock_data is not None:
            
        st.write(f"<div class='title'>Stock Data for {company_name}</div>", unsafe_allow_html=True)
        
        # Displaying current prices
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div class='metric-value'>Open: ${current_price['Open'].iloc[-1]:.2f}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-value'>Close: ${current_price['Close'].iloc[-1]:.2f}</div>", unsafe_allow_html=True)
        
        st.write("### Historical Stock Data")
        st.dataframe(stock_data, height=200)
        st.write("### Technical Indicators")
        st.dataframe(indicators, height=200)
        
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

        fig.update_layout(title=f"Candlestick Chart for {company_name}",
                          xaxis_title="Date",
                          yaxis_title="Price (USD)",
                          xaxis_rangeslider_visible=False)

        st.plotly_chart(fig)


        # Generate insights using LLM
        prompt = f"""
        Analyze the stock performance of {company_name} over the {interval} period.
        Use the following technical indicators: {indicators}.
        Provide actionable insights and a summary for an investor.
        and give the answer whether one should buy this stock or not ?
        analyse it based on data and do not show disclaimer of "This analysis is based on technical indicators and should not be considered as investment advice."
        Be specific to answer and do not generalize the opinion and explain the reccomendation in simple language.
        Also mention until when to wait ,if you think one should not buy that stock now.
        And do not just write paragraphs, make points and they must be readable and understandable
        """
        insights = get_llm_response(prompt)
        st.write("### AI Insights")
        st.write(insights)
    else:
        st.error("Failed to fetch stock data. Check the company name or data source.")
