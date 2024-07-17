import os
from openai import OpenAI

# Print the API key to verify it's being accessed correctly
print(f"API Key in gpt_translator.py: {os.getenv('OPENAI_API_KEY')}")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_text(text):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a translator that converts text to English. Preserve the HTML tags in the translation."},
            {"role": "user", "content": f"Translate the following text to English, preserving HTML tags:\n\n{text}"}
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content.strip()
