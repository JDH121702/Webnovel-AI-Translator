import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dotenv import load_dotenv
from tqdm import tqdm
from ebooklib import epub  # Ensure this import is present
import logging

# Load environment variables from .env file
load_dotenv()

from scraper.novel_scraper import get_chapter_urls
from scraper.chapter_parser import get_chapter_content
from translator.gpt_translator import translate_text
from utils.helpers import clean_text

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Webnovel Translator")
        self.geometry("800x600")  # Increased default window size
        self.configure(bg="#f8f9fa")

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#f8f9fa", font=("Helvetica", 12))
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TEntry", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f8f9fa")
        self.style.configure("TProgressbar", thickness=20)

        self.chapter_urls = []
        self.chapter_titles = []
        self.selected_chapters = []
        self.cover_image_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding="20 20 20 20", style="TFrame")
        frame.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        # Novel URL
        ttk.Label(frame, text="Novel URL:", anchor="e").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.novel_url_entry = ttk.Entry(frame, width=50)
        self.novel_url_entry.grid(row=0, column=1, padx=10, pady=10)

        # EPUB Title
        ttk.Label(frame, text="EPUB Title:", anchor="e").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.epub_title_entry = ttk.Entry(frame, width=50)
        self.epub_title_entry.grid(row=1, column=1, padx=10, pady=10)

        # Author
        ttk.Label(frame, text="Author:", anchor="e").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.author_entry = ttk.Entry(frame, width=50)
        self.author_entry.grid(row=2, column=1, padx=10, pady=10)

        # EPUB Filename
        ttk.Label(frame, text="EPUB Filename:", anchor="e").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.epub_filename_entry = ttk.Entry(frame, width=50)
        self.epub_filename_entry.grid(row=3, column=1, padx=10, pady=10)

        # Output Directory
        ttk.Label(frame, text="Output Directory:", anchor="e").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.output_dir_button = ttk.Button(frame, text="Browse...", command=self.browse_output_dir)
        self.output_dir_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.output_dir = tk.StringVar()
        self.output_dir_label = ttk.Label(frame, textvariable=self.output_dir, anchor="w")
        self.output_dir_label.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        # Cover Image
        ttk.Label(frame, text="Cover Image:", anchor="e").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.cover_image_button = ttk.Button(frame, text="Browse...", command=self.browse_cover_image)
        self.cover_image_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.cover_image_label = ttk.Label(frame, textvariable=self.cover_image_path, anchor="w")
        self.cover_image_label.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        # Grab Chapters Button
        self.grab_chapters_button = ttk.Button(frame, text="Grab Chapters", command=self.grab_chapters)
        self.grab_chapters_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Chapters Count Label
        self.chapters_count_label = ttk.Label(frame, text="", font=("Helvetica", 10))
        self.chapters_count_label.grid(row=7, column=0, columnspan=2, pady=10)

        # Chapter Selection Frame
        self.chapter_selection_frame = ttk.Frame(self, padding="10 10 10 10", style="TFrame")
        self.chapter_selection_frame.grid(row=1, column=0, sticky="nsew")
        self.chapter_selection_frame.columnconfigure(0, weight=1)
        self.chapter_selection_frame.rowconfigure(0, weight=1)

        self.chapter_listbox = tk.Listbox(self.chapter_selection_frame, selectmode=tk.MULTIPLE, width=50, height=20)
        self.chapter_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        chapter_listbox_scrollbar = ttk.Scrollbar(self.chapter_selection_frame, orient=tk.VERTICAL, command=self.chapter_listbox.yview)
        chapter_listbox_scrollbar.grid(row=0, column=1, sticky="ns")
        self.chapter_listbox.config(yscrollcommand=chapter_listbox_scrollbar.set)

        # Select/Deselect All Buttons
        self.select_all_button = ttk.Button(self.chapter_selection_frame, text="Select All", command=self.select_all_chapters)
        self.select_all_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.deselect_all_button = ttk.Button(self.chapter_selection_frame, text="Deselect All", command=self.deselect_all_chapters)
        self.deselect_all_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Translate Button
        self.translate_button = ttk.Button(self, text="Translate", command=self.start_translation, state=tk.DISABLED)
        self.translate_button.grid(row=2, column=0, columnspan=2, pady=10)

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def browse_output_dir(self):
        dir_selected = filedialog.askdirectory()
        if dir_selected:
            self.output_dir.set(dir_selected)

    def browse_cover_image(self):
        file_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_selected:
            self.cover_image_path.set(file_selected)

    def grab_chapters(self):
        novel_url = self.novel_url_entry.get()

        if not novel_url:
            messagebox.showerror("Error", "Please enter the novel URL.")
            return

        try:
            chapters = get_chapter_urls(novel_url)
            self.chapter_urls = [url for url, _ in chapters]
            self.chapter_titles = [title for _, title in chapters]
            self.update_chapter_listbox()
            chapters_count = len(self.chapter_urls)
            self.chapters_count_label.config(text=f"Chapters Grabbed: {chapters_count}")

            if chapters_count > 0:
                self.translate_button.config(state=tk.NORMAL)
            else:
                self.translate_button.config(state=tk.DISABLED)
        except Exception as e:
            logging.error("Error while grabbing chapters: %s", e)
            messagebox.showerror("Error", f"An error occurred while grabbing chapters: {e}")

    def update_chapter_listbox(self):
        self.chapter_listbox.delete(0, tk.END)
        for title in self.chapter_titles:
            self.chapter_listbox.insert(tk.END, title)
        for i in range(len(self.chapter_titles)):
            self.chapter_listbox.select_set(i)

    def select_all_chapters(self):
        self.chapter_listbox.select_set(0, tk.END)

    def deselect_all_chapters(self):
        self.chapter_listbox.select_clear(0, tk.END)

    def start_translation(self):
        epub_title = self.epub_title_entry.get()
        author = self.author_entry.get()
        epub_filename = self.epub_filename_entry.get() + ".epub"
        output_dir = self.output_dir.get()
        cover_image = self.cover_image_path.get()

        if not epub_title or not author or not epub_filename or not output_dir:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        selected_indices = self.chapter_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one chapter to translate.")
            return

        selected_chapters = [(self.chapter_titles[i], self.chapter_urls[i]) for i in selected_indices]

        self.translate_button.config(state=tk.DISABLED)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
        self.progress.grid(row=3, column=0, columnspan=2, padx=10, pady=20)
        self.progress.config(value=0)
        self.update()

        chapters = []

        for i, (title, url) in enumerate(tqdm(selected_chapters, desc="Translating Chapters", unit="chapter")):
            try:
                content = get_chapter_content(url)
                if content:
                    cleaned_content = clean_text(content)
                    translated_content = translate_text(cleaned_content)
                    if translated_content:
                        chapters.append((title, translated_content))
                self.progress.config(value=(i+1) * (100 // len(selected_chapters)))
                self.update()
            except Exception as e:
                logging.error("Error while translating chapter: %s", e)
                messagebox.showerror("Error", f"An error occurred while translating a chapter: {e}")

        if chapters:
            try:
                create_epub(epub_title, author, chapters, output_dir, epub_filename, cover_image)
                messagebox.showinfo("Success", "EPUB file created successfully!")
            except Exception as e:
                logging.error("Error while creating EPUB: %s", e)
                messagebox.showerror("Error", f"An error occurred while creating the EPUB file: {e}")
        else:
            messagebox.showerror("Error", "No chapters were processed successfully.")

        self.translate_button.config(state=tk.NORMAL)

def create_epub(title, author, chapters, output_dir, epub_filename, cover_image):
    book = epub.EpubBook()
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # Define the TOC
    toc = []

    for i, (chapter_title, content) in enumerate(chapters):
        chapter = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i+1}.xhtml', lang='en')
        chapter.content = f'<h1>{chapter_title}</h1>{content}'
        book.add_item(chapter)
        toc.append(epub.Link(chapter.file_name, chapter.title, chapter_title))

    # Add the cover image
    if cover_image:
        with open(cover_image, 'rb') as img_file:
            book.set_cover("cover.jpg", img_file.read())

    # Define Table of Contents
    book.toc = tuple(toc)

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

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
