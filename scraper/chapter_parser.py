import requests
from bs4 import BeautifulSoup
from config import HEADERS

def get_chapter_content(chapter_url):
    response = requests.get(chapter_url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to fetch content. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Target the <div> with id "novel_honbun"
    content_div = soup.find('div', id='novel_honbun')
    
    if content_div:
        # Extract the HTML content while preserving tags
        content_html = ''.join(str(tag) for tag in content_div.find_all(['p', 'br', 'div']))
        return content_html
    else:
        print("Content div not found!")
        return None
