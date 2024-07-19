import ebooklib
from ebooklib import epub

def read_epub(file_path):
    book = epub.read_epub(file_path)
    
    # Extract metadata
    title = book.get_metadata('DC', 'title')[0][0]
    author = book.get_metadata('DC', 'creator')[0][0]
    cover_image = None

    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        if 'cover' in item.get_name().lower():
            cover_image = item.content
            break
    
    # Extract chapters and their content
    chapters = []
    toc = []
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            chapters.append((item.title, item.content.decode('utf-8')))
            toc.append(epub.Link(item.file_name, item.title, item.title))
    
    return {
        'title': title,
        'author': author,
        'cover_image': cover_image,
        'chapters': chapters,
        'toc': toc
    }
