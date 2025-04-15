import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_data_with_gpt(text):
    prompt = f"""Extract the following fields from this document. Return the output as valid JSON.
    
    Required Fields:
    - type (either "Invoice" or "Purchase Order")
    - document_number
    - vendor
    - date
    - items: a list of {{"item": string, "quantity": number, "unit_price": float, "total_price": float}}
    - grand_total

    Document Text:
    {text[:3000]}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
