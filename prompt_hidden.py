
def get_prompt(company_name,interval,news_response,indicators):
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
    return prompt