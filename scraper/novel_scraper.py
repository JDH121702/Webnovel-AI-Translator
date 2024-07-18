import requests
from bs4 import BeautifulSoup
from config import HEADERS
import logging

def get_chapter_urls(novel_url, max_pages=100):
    chapters = []
    page = 1

    while page <= max_pages:
        response = requests.get(f"{novel_url}?p={page}", headers=HEADERS)
        logging.debug(f"Fetching page {page}: {response.url} - Status Code: {response.status_code}")
        if response.status_code != 200:
            logging.error(f"Failed to fetch page {page}: {response.status_code}")
            break  # Stop if the response is not successful

        soup = BeautifulSoup(response.text, 'html.parser')

        # Adjusting the selector based on the actual HTML structure
        chapter_elements = soup.select('dd.subtitle a')
        logging.debug(f"Found {len(chapter_elements)} chapter links on page {page}")
        if not chapter_elements:
            logging.debug("No more chapter links found.")
            break  # Stop if no more chapter links are found

        base_url = novel_url.rstrip('/')  # Remove trailing slash if present
        for element in chapter_elements:
            url = requests.compat.urljoin(base_url, element['href'])
            title = element.text.strip()
            chapters.append((url, title))

        # Check for the "next" button to see if there are more pages
        next_button = soup.select_one('a:-soup-contains("次へ")')  # Use :-soup-contains instead of :contains
        if not next_button:
            logging.debug("No next button found. Ending pagination.")
            break  # Stop if no next button is found

        page += 1

    logging.debug(f"Total chapters found: {len(chapters)}")
    return chapters
