import unittest
from scraper.novel_scraper import get_chapter_urls
from scraper.chapter_parser import get_chapter_content

class TestScraper(unittest.TestCase):
    def test_get_chapter_urls(self):
        # Mock or real test URL
        urls = get_chapter_urls("https://ncode.syosetu.com/n2163n/")
        self.assertGreater(len(urls), 0)

    def test_get_chapter_content(self):
        # Mock or real chapter URL
        content = get_chapter_content("https://ncode.syosetu.com/n2163n/1/")
        self.assertTrue(len(content) > 0)

if __name__ == '__main__':
    unittest.main()
