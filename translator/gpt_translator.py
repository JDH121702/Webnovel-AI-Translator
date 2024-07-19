import os
from openai import OpenAI

# Print the API key to verify it's being accessed correctly
print(f"API Key in gpt_translator.py: {os.getenv('OPENAI_API_KEY')}")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def translate_text(text):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a translator that converts text to English. Preserve the HTML tags and the original author's writing style as much as possible."},
            {"role": "user", "content": f"Translate the following text to English, preserving HTML tags and the original author's writing style:\n\n{text}"}
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content.strip()

def translate_chapters(chapters):
    translated_chapters = []
    for title, content in chapters:
        translated_content = translate_text(content)
        translated_chapters.append((title, translated_content))
    return translated_chapters
