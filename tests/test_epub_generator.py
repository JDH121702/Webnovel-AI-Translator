import unittest
import os
import tempfile
from ebooklib import epub
from epub.epub_generator import create_epub

class TestEPUBGenerator(unittest.TestCase):
    def test_create_epub(self):
        chapters = [
            ("Chapter 1", "This is the content of chapter 1."),
            ("Chapter 2", "This is the content of chapter 2.")
        ]
        toc = [epub.Link(f'chap_{i+1}.xhtml', title, title)
               for i, (title, _) in enumerate(chapters)]
        with tempfile.TemporaryDirectory() as tmpdir:
            create_epub(
                "Test Novel",
                "Author",
                chapters,
                tmpdir,
                "Test_Novel.epub",
                None,
                toc,
            )
            self.assertTrue(
                os.path.exists(os.path.join(tmpdir, "Test_Novel.epub"))
            )

if __name__ == '__main__':
    unittest.main()
