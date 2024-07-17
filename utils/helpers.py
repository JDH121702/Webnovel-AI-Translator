import re

def clean_text(text):
    # Ensure HTML tags for paragraphs and line breaks are preserved
    text = re.sub(r'\s+', ' ', text).strip()
    # Replace double newlines with paragraph tags and single newlines with <br/>
    text = text.replace('\n\n', '</p><p>').replace('\n', '<br/>')
    # Ensure the text is wrapped in <p> tags
    return f'<p>{text}</p>'
