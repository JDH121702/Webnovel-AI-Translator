import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dotenv import load_dotenv
from tqdm import tqdm
from ebooklib import epub  # Ensure this import is present
import logging
import ttkbootstrap as tb

# Load environment variables from .env file
load_dotenv()

from scraper.novel_scraper import get_chapter_urls
from scraper.chapter_parser import get_chapter_content
from translator.gpt_translator import translate_text, translate_chapters
from utils.helpers import clean_text
from epub.epub_reader import read_epub
from epub.epub_generator import create_epub

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TranslatorApp(tb.Window):
    def __init__(self):
        # Use a more professional theme for a modern look
        super().__init__(themename="cosmo")

        self.title("Webnovel Translator")
        self.geometry("900x880")  # Increased default window size by 10%

        # Apply a corporate style font across the application
        self.option_add("*Font", "Segoe UI 11")

        # Configure general style settings
        self.style = tb.Style()
        self.style.configure("TFrame", background="#FFFFFF")
        self.style.configure("TLabel", background="#FFFFFF", font=("Segoe UI", 11))
        self.style.configure("TButton", font=("Segoe UI", 11))
        self.style.configure("TProgressbar", thickness=20)

        self.configure(bg="#FFFFFF")

        self.chapter_urls = []
        self.chapter_titles = []
        self.selected_chapters = []
        self.cover_image_path = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")
        self.progress = None

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About", "Webnovel Translator - powered by GPT"
            ),
        )
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def create_widgets(self):
        notebook = tb.Notebook(self, bootstyle="secondary")
        notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        details_frame = ttk.Frame(notebook, padding="20 20 20 20", style="TFrame")
        chapters_frame = ttk.Frame(notebook, padding="10 10 10 10", style="TFrame")
        notebook.add(details_frame, text="Details")
        notebook.add(chapters_frame, text="Chapters")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        details_frame.columnconfigure(0, weight=1)
        details_frame.columnconfigure(1, weight=1)
        details_frame.columnconfigure(2, weight=1)

        # Novel URL
        ttk.Label(details_frame, text="Novel URL:", anchor="e").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.novel_url_entry = ttk.Entry(details_frame, width=50)
        self.novel_url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # EPUB Title
        ttk.Label(details_frame, text="EPUB Title:", anchor="e").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.epub_title_entry = ttk.Entry(details_frame, width=50)
        self.epub_title_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Author
        ttk.Label(details_frame, text="Author:", anchor="e").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.author_entry = ttk.Entry(details_frame, width=50)
        self.author_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # EPUB Filename
        ttk.Label(details_frame, text="EPUB Filename:", anchor="e").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.epub_filename_entry = ttk.Entry(details_frame, width=50)
        self.epub_filename_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Output Directory
        ttk.Label(details_frame, text="Output Directory:", anchor="e").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.output_dir_button = ttk.Button(details_frame, text="Browse...", command=self.browse_output_dir)
        self.output_dir_button.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        self.output_dir = tk.StringVar()
        self.output_dir_label = ttk.Label(details_frame, textvariable=self.output_dir, anchor="w")
        self.output_dir_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        # Cover Image
        ttk.Label(details_frame, text="Cover Image:", anchor="e").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.cover_image_button = ttk.Button(details_frame, text="Browse...", command=self.browse_cover_image)
        self.cover_image_button.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        self.cover_image_label = ttk.Label(details_frame, textvariable=self.cover_image_path, anchor="w")
        self.cover_image_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        # EPUB Upload
        ttk.Label(details_frame, text="Upload EPUB:", anchor="e").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.epub_upload_button = ttk.Button(details_frame, text="Browse...", command=self.upload_epub)
        self.epub_upload_button.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        self.epub_upload_label = ttk.Label(details_frame, text="", anchor="w")
        self.epub_upload_label.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        # Chapters Count Label
        self.chapters_count_label = ttk.Label(details_frame, text="", font=("Roboto", 10))
        self.chapters_count_label.grid(row=7, column=0, columnspan=3, pady=20)

        # Chapter Selection Frame
        self.chapter_selection_frame = ttk.Frame(chapters_frame, padding="10 10 10 10", style="TFrame")
        self.chapter_selection_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.chapter_selection_frame.columnconfigure(0, weight=1)
        self.chapter_selection_frame.rowconfigure(0, weight=1)

        self.chapter_listbox = tk.Listbox(
            self.chapter_selection_frame,
            selectmode=tk.MULTIPLE,
            width=50,
            height=20,
            bg="#FFFFFF",
            fg="#000000",
            font=("Segoe UI", 11)
        )
        self.chapter_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        chapter_listbox_scrollbar = ttk.Scrollbar(self.chapter_selection_frame, orient=tk.VERTICAL, command=self.chapter_listbox.yview)
        chapter_listbox_scrollbar.grid(row=0, column=1, sticky="ns")
        self.chapter_listbox.config(yscrollcommand=chapter_listbox_scrollbar.set)

        # Select/Deselect All Buttons and Grab Chapters Button
        self.select_all_button = ttk.Button(self.chapter_selection_frame, text="Select All", command=self.select_all_chapters)
        self.select_all_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.grab_chapters_button = ttk.Button(self.chapter_selection_frame, text="Grab Chapters", command=self.grab_chapters)
        self.grab_chapters_button.grid(row=1, column=0, padx=5, pady=5)

        self.deselect_all_button = ttk.Button(self.chapter_selection_frame, text="Deselect All", command=self.deselect_all_chapters)
        self.deselect_all_button.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Translate Button
        self.translate_button = ttk.Button(self, text="Translate", command=self.start_translation, state=tk.DISABLED)
        self.translate_button.grid(row=2, column=0, columnspan=3, pady=20)

        self.status_bar = ttk.Label(self, textvariable=self.status_var, anchor="w", style="TLabel")
        self.status_bar.grid(row=3, column=0, sticky="ew", padx=10, pady=(0,10))

        for child in details_frame.winfo_children():
            child.grid_configure(padx=10, pady=10)

    def browse_output_dir(self):
        dir_selected = filedialog.askdirectory()
        if dir_selected:
            self.output_dir.set(dir_selected)

    def browse_cover_image(self):
        file_selected = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_selected:
            self.cover_image_path.set(file_selected)

    def upload_epub(self):
        file_selected = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])
        if file_selected:
            self.epub_upload_label.config(text=os.path.basename(file_selected))
            epub_data = read_epub(file_selected)
            self.epub_title_entry.delete(0, tk.END)
            self.epub_title_entry.insert(0, epub_data['title'])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, epub_data['author'])
            self.cover_image_path.set(file_selected)

            self.selected_chapters = epub_data['chapters']
            self.chapter_titles = [title for title, _ in epub_data['chapters']]
            self.update_chapter_listbox()

            if self.selected_chapters:
                self.translate_button.config(state=tk.NORMAL)

    def grab_chapters(self):
        novel_url = self.novel_url_entry.get()

        if not novel_url:
            messagebox.showerror("Error", "Please enter the novel URL.")
            return

        try:
            self.status_var.set("Fetching chapters...")
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
            self.status_var.set(f"{chapters_count} chapters ready")
        except Exception as e:
            logging.error("Error while grabbing chapters: %s", e)
            messagebox.showerror("Error", f"An error occurred while grabbing chapters: {e}")
            self.status_var.set("Error while grabbing chapters")

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
        if not selected_indices and not self.selected_chapters:
            messagebox.showerror("Error", "Please select at least one chapter to translate.")
            return

        if self.selected_chapters:
            selected_chapters = self.selected_chapters
        else:
            selected_chapters = [(self.chapter_titles[i], self.chapter_urls[i]) for i in selected_indices]

        self.translate_button.config(state=tk.DISABLED)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate", style="TProgressbar")
        self.progress.grid(row=1, column=0, columnspan=3, padx=10, pady=20)
        self.progress.config(value=0)
        self.status_var.set("Translating chapters...")
        self.update()

        chapters = []

        for i, (title, url_or_content) in enumerate(tqdm(selected_chapters, desc="Translating Chapters", unit="chapter")):
            try:
                if url_or_content.startswith('http'):
                    content = get_chapter_content(url_or_content)
                else:
                    content = url_or_content
                if content:
                    cleaned_content = clean_text(content)
                    translated_content = translate_text(cleaned_content)
                    if translated_content:
                        chapters.append((title, translated_content))
                progress_value = (i + 1) / len(selected_chapters) * 100
                self.progress.config(value=progress_value)
                self.update()
            except Exception as e:
                logging.error("Error while translating chapter: %s", e)
                messagebox.showerror("Error", f"An error occurred while translating a chapter: {e}")

        if chapters:
            try:
                toc = [epub.Link(f'chap_{i+1}.xhtml', chapter_title, chapter_title) for i, (chapter_title, _) in enumerate(chapters)]
                create_epub(epub_title, author, chapters, output_dir, epub_filename, cover_image, toc)
                messagebox.showinfo("Success", "EPUB file created successfully!")
            except Exception as e:
                logging.error("Error while creating EPUB: %s", e)
                messagebox.showerror("Error", f"An error occurred while creating the EPUB file: {e}")
        else:
            messagebox.showerror("Error", "No chapters were processed successfully.")

        self.translate_button.config(state=tk.NORMAL)
        self.status_var.set("Translation complete")
        if self.progress:
            self.progress.destroy()

if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()
