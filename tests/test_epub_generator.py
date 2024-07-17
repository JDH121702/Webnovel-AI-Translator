import unittest
import os
from epub.epub_generator import create_epub

class TestEPUBGenerator(unittest.TestCase):
    def test_create_epub(self):
        chapters = [
            ("Chapter 1", "This is the content of chapter 1."),
            ("Chapter 2", "This is the content of chapter 2.")
        ]
        create_epub("Test Novel", chapters)
        self.assertTrue(os.path.exists("Test Novel.epub"))
        os.remove("Test Novel.epub")

if __name__ == '__main__':
    unittest.main()
