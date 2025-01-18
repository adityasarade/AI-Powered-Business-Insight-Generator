from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")
def get_llm_response(prompt):
    try:
        # Ensure prompt is in correct message format
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides insights based on stock data."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Get the response from the LLM
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while generating insights."

if __name__ == "__main__":
    response=llm.invoke("What are the highest earning careers")
    print(response.content)