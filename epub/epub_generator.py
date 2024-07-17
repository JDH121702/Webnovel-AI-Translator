from ebooklib import epub
import os

def create_epub(novel_title, chapters, output_dir, epub_filename):
    book = epub.EpubBook()
    book.set_title(novel_title)
    book.set_language('en')
    
    for i, (title, content) in enumerate(chapters):
        chapter = epub.EpubHtml(title=title, file_name=f'chap_{i+1}.xhtml', lang='en')
        # Ensure the content is HTML and preserving paragraph breaks
        chapter.content = f'<h1>{title}</h1><div>{content}</div>'
        book.add_item(chapter)
    
    # Define Table of Contents
    book.toc = (epub.Link(ch.file_name, ch.title, ch.title) for ch in book.items if isinstance(ch, epub.EpubHtml))
    # Add default NCX and Nav files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = '''
    body { font-family: Times, serif; }
    p { margin: 0 0 1em 0; line-height: 1.5em; }
    br { line-height: 1.5em; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Create the spine
    book.spine = ['nav'] + [ch for ch in book.items if isinstance(ch, epub.EpubHtml)]
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Write to the file
    output_path = os.path.join(output_dir, epub_filename)
    epub.write_epub(output_path, book, {})
    print(f'EPUB file created at: {output_path}')
