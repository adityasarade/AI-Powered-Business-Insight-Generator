# 📈 AI-Powered Stock Insights Generator

An advanced AI-driven tool for real-time stock analysis and investment insights. This tool analyzes **170+ stocks** from **NASDAQ**, **NIFTY 50**, and **S&P 500**, providing technical indicators, historical trends, and AI-generated recommendations to Buy, Wait or Hold to help you make informed financial decisions.

---

## 🚀 Features  

### 1️⃣ **Dynamic Stock Analysis**  
- Processes real-time and historical stock data using **YFinance**.  
- Computes technical indicators like RSI, MACD, and moving averages.  
- Displays interactive candlestick charts and trend patterns across multiple time frames.  
- Integrates relevant market news for deeper insights.  

### 2️⃣ **AI-Powered Investment Insights**  
- Leverages **Llama 3.3 (GroqCloud)** to analyze trends and generate actionable recommendations.  
- Provides **buy/hold/wait** suggestions based on technical and market analysis.    

### 3️⃣ **User-Friendly Interface**  
- Built with **Streamlit** for an intuitive and interactive experience.  
- Easy navigation to key financial insights and trends.  
- Generates **automated PDF reports** summarizing stock insights and technical analysis.  

---

## 🛠 Tech Stack  

| **Component**       | **Technology**        |  
|----------------------|-----------------------|  
| Frontend             | Streamlit             |  
| AI Model             | LLaMA 3.3 (GroqCloud) |  
| Financial Data       | YFinance              |  
| LLM Integration      | LangChain             |  

---

## 📂 Add this file

### **`hidden_prompt`**  
   - Contains the prompt template given to the **LLM (Llama 3.3)**.  
   - The prompt includes technical indicators and instructions for analyzing stocks and generating insights.
   - In this format:
     ```python
     def get_prompt(company_name, interval, news_response, indicators):
         prompt = """
         Write your prompt here, including relevant financial data, technical indicators, and instructions for generating insights.
         """
         return prompt
     ```

---

## 🛠 Installation  

### Steps  
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/ai-stock-insights.git
   cd ai-stock-insights
   ```
2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
## 🚀 Usage
```sh
# Run the Streamlit app
streamlit run app.py
```
Access the app at `http://localhost:8501/` in your browser.

## 📜 API Keys Setup
To use **GroqCloud LLaMA 3.3**, add your API key to an `.env` file:
```sh
GROQCLOUD_API_KEY=your_api_key_here
```
