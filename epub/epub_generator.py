from ebooklib import epub
import os

def create_epub(title, author, chapters, output_dir, epub_filename, cover_image, toc=None):
    book = epub.EpubBook()
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Define the TOC ensuring filenames match the added chapters
    if toc is None:
        toc = [epub.Link(f'chap_{i+1}.xhtml', chapter_title, chapter_title)
               for i, (chapter_title, _) in enumerate(chapters)]
    book.toc = tuple(toc)

    # Add chapters to the book
    for i, (chapter_title, content) in enumerate(chapters):
        chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i+1}.xhtml', lang='en')
        chapter.content = f'<h1>{chapter_title}</h1>{content}'
        book.add_item(chapter)

    # Add the cover image
    if cover_image:
        book.set_cover("cover.jpg", cover_image)

    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Define CSS style
    style = 'BODY { font-family: Times, serif; } P { margin-bottom: 1em; }'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Create the spine
    book.spine = ['nav'] + [ch for ch in book.items if isinstance(ch, epub.EpubHtml)]

    # Write to the file
    epub.write_epub(os.path.join(output_dir, epub_filename), book, {})
