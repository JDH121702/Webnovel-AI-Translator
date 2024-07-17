import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables from .env file
load_dotenv()

from scraper.novel_scraper import get_chapter_urls
from scraper.chapter_parser import get_chapter_content
from translator.gpt_translator import translate_text
from epub.epub_generator import create_epub
from utils.helpers import clean_text

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

        # EPUB Filename
        ttk.Label(frame, text="EPUB Filename:", anchor="e").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.epub_filename_entry = ttk.Entry(frame, width=50)
        self.epub_filename_entry.grid(row=2, column=1, padx=10, pady=10)

        # Output Directory
        ttk.Label(frame, text="Output Directory:", anchor="e").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.output_dir_button = ttk.Button(frame, text="Browse...", command=self.browse_output_dir)
        self.output_dir_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        self.output_dir = tk.StringVar()
        self.output_dir_label = ttk.Label(frame, textvariable=self.output_dir, anchor="w")
        self.output_dir_label.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        # Grab Chapters Button
        self.grab_chapters_button = ttk.Button(frame, text="Grab Chapters", command=self.grab_chapters)
        self.grab_chapters_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Chapters Count Label
        self.chapters_count_label = ttk.Label(frame, text="", font=("Helvetica", 10))
        self.chapters_count_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Number of Chapters to Translate
        ttk.Label(frame, text="Number of Chapters to Translate:", anchor="e").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.num_chapters_entry = ttk.Entry(frame, width=10)
        self.num_chapters_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Progress Bar
        self.progress = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
        self.progress.grid(row=7, column=0, columnspan=2, padx=10, pady=20)

        # Translate Button
        self.translate_button = ttk.Button(frame, text="Translate", command=self.start_translation, state=tk.DISABLED)
        self.translate_button.grid(row=8, column=0, columnspan=2, pady=10)

        for child in frame.winfo_children():
            child.grid_configure(padx=10, pady=5)

    def browse_output_dir(self):
        dir_selected = filedialog.askdirectory()
        if dir_selected:
            self.output_dir.set(dir_selected)

    def grab_chapters(self):
        novel_url = self.novel_url_entry.get()

        if not novel_url:
            messagebox.showerror("Error", "Please enter the novel URL.")
            return

        self.chapter_urls = get_chapter_urls(novel_url)
        chapters_count = len(self.chapter_urls)
        self.chapters_count_label.config(text=f"Chapters Grabbed: {chapters_count}")

        if chapters_count > 0:
            self.translate_button.config(state=tk.NORMAL)
        else:
            self.translate_button.config(state=tk.DISABLED)

    def start_translation(self):
        epub_title = self.epub_title_entry.get()
        epub_filename = self.epub_filename_entry.get() + ".epub"
        output_dir = self.output_dir.get()
        num_chapters = self.num_chapters_entry.get()

        if not epub_title or not epub_filename or not output_dir:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if not num_chapters.isdigit() or int(num_chapters) <= 0:
            messagebox.showerror("Error", "Please enter a valid number of chapters to translate.")
            return

        num_chapters = min(int(num_chapters), len(self.chapter_urls))

        self.translate_button.config(state=tk.DISABLED)
        self.progress.config(value=0)
        self.update()

        chapters = []

        for i, url in enumerate(tqdm(self.chapter_urls[:num_chapters], desc="Translating Chapters", unit="chapter")):
            content = get_chapter_content(url)
            if content:
                cleaned_content = clean_text(content)
                translated_content = translate_text(cleaned_content)
                if translated_content:
                    chapters.append((url.split('/')[-1], translated_content))
            self.progress.config(value=(i+1) * (100 // num_chapters))
            self.update()

        if chapters:
            create_epub(epub_title, chapters, output_dir, epub_filename)
            messagebox.showinfo("Success", "EPUB file created successfully!")
        else:
            messagebox.showerror("Error", "No chapters were processed successfully.")

        self.translate_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
