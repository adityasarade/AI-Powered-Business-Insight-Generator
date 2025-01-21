import streamlit as st
import pandas as pd
from yfinance_api import fetch_yfinance_data
from llmhelper import get_llm_response  # Import the LLM response function
import plotly.graph_objects as go  # type: ignore
import json
from io import StringIO
from prompt_hidden import get_prompt # imported the hidden prompt, which is used to query LLM
from generate_pdf import generate_pdf

# Load the company data
with open('companies.json', 'r') as f:
    data = json.load(f)


# Sidebar Customization
st.sidebar.markdown(
    """
    <style>
    .css-1d391kg {display: none;}

    .sidebar-box {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-decoration-line: none; 
    }

    .sidebar-link {
        display: block;
        padding: 10px 15px;
        margin-bottom: 10px;
        background-color: #606060 ;
        text-align: center;
        border-radius: 5px;
        color: #333333;
        text-decoration: none;
        font-weight: bold;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s, color 0.3s;
    }
    .sidebar-link:hover {
        background-color: #0073e6;
        color: white;
    }
    a.sidebar-link {
        text-decoration-line: none !important;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Title
st.sidebar.title("Navigation")


# List of sections for navigation
sections = ["Introduction", "Historical Data", "Technical Indicators", "Candlestick Chart", "AI Insights"]

# Add links to the sidebar
for section in sections:
    link = f'<a href="#{section.lower().replace(" ", "-")}" class="sidebar-link">{section}</a>'
    st.sidebar.markdown(link, unsafe_allow_html=True)

st.sidebar.markdown('</div>', unsafe_allow_html=True)


# main code for input
# Dropdown for company, stock exchange, and interval
exchange = st.selectbox("Select Stock Exchange", list(data.keys()))
company = st.selectbox("Select Company", list(data[exchange].keys()))
company_name = data[exchange][company]
interval = st.selectbox("Select Interval", ["Daily", "Weekly", "Monthly", "Yearly", "Max"])


# Fetch Data
if st.button("Fetch Stock Data"):
    stock_data, indicators, current_price, news_response = fetch_yfinance_data(company_name, interval)

    if stock_data is not None:
        # Prepare the report content
        report_content = StringIO()
        report_content.write(f"Stock Exchange: {exchange}\n")
        report_content.write(f"Company: {company_name}\n")
        report_content.write(f"Time Interval: {interval}\n\n")

        # Section 1: Introduction
        st.markdown("<h2 id='introduction'>Introduction</h2>", unsafe_allow_html=True)
        intro_text = f"Fetching data for **{company_name}** listed on **{exchange}**."
        st.write(intro_text)
        report_content.write("Introduction:\n")
        report_content.write(f"{company_name} is listed on {exchange}.\n\n")

        # Section 2: Historical Stock Data
        st.markdown("<h2 id='historical-data'>Historical Stock Data</h2>", unsafe_allow_html=True)
        styled_stock_data = stock_data.style.set_table_styles(
            [{"selector": "th", "props": [("text-align", "center")]}]
        ).set_properties(**{"text-align": "center"})
        st.dataframe(styled_stock_data, height=200, use_container_width=True)
        report_content.write("Historical Stock Data:\n")
        report_content.write(stock_data.to_csv(index=True))
        report_content.write("\n\n")

        # Section 3: Technical Indicators
        st.markdown("<h2 id='technical-indicators'>Technical Indicators</h2>", unsafe_allow_html=True)
        st.dataframe(indicators, height=200, use_container_width=True)
        report_content.write("Technical Indicators:\n")
        report_content.write(indicators.to_csv(index=True))
        report_content.write("\n\n")

        # Display tooltips in an expander
        st.write("### Indicator Details")
        with st.expander("See Indicator Details"):
            for col, desc in {
                "SMA": "Simple Moving Average (SMA) is the average of the closing prices for a specified period. It smooths price data to help identify trends.",
                "EMA": "Exponential Moving Average (EMA) gives more weight to recent prices, and reacts more quickly to price changes than the SMA.",
                "RSI": "The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. It ranges from 0 to 100.",
                "MACD": "The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price."
            }.items():
                st.markdown(f"**{col}**: {desc}")
                report_content.write(f"{col}: {desc}\n")
        report_content.write("\n")

        # Section 4: Candlestick Chart
        st.markdown("<h2 id='candlestick-chart'>Candlestick Chart</h2>", unsafe_allow_html=True)
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
            yaxis_title="Price (INR)" if exchange == "Nifty 50" else "Price (USD)",  # Dynamic y-axis title
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig)
        report_content.write("Candlestick Chart:\n")
        report_content.write("The candlestick chart visualizes stock price movements for the selected interval.\n\n")

        # Section 5: AI Insights
        st.markdown("<h2 id='ai-insights'>AI Insights</h2>", unsafe_allow_html=True)
        
        # get prompt from prompt_hidden python file
        prompt = get_prompt(company_name,interval,news_response,indicators)
        insights = get_llm_response(prompt)
        st.write(insights)
        report_content.write("AI Insights:\n")
        report_content.write(insights)
        report_content.write("\n")

        # Download Button
        pdf_output = generate_pdf(company_name, exchange, interval, stock_data, indicators, insights)

        st.download_button(
            label="Download PDF Report",
            data=pdf_output,
            file_name=f"{company_name}_stock_report.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Failed to fetch stock data. Check the company name or data source.")
