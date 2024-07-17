import requests
from bs4 import BeautifulSoup
from config import HEADERS

def get_chapter_urls(novel_url):
    chapter_urls = []
    page = 1

    while True:
        response = requests.get(f"{novel_url}?p={page}", headers=HEADERS)
        if response.status_code == 404:
            break  # No more pages

        soup = BeautifulSoup(response.text, 'html.parser')

        # Adjusting the selector based on the actual HTML structure
        chapter_links = soup.select('dd.subtitle a')
        if not chapter_links:
            break  # No more chapters on this page

        base_url = novel_url.rstrip('/')  # Remove trailing slash if present
        new_chapter_urls = [requests.compat.urljoin(base_url, link['href']) for link in chapter_links]
        chapter_urls.extend(new_chapter_urls)
        page += 1

    return chapter_urls
