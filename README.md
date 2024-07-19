# Webnovel AI Translator

This translator is a comprehensive tool specifically designed for translating webnovel chapters from Syosetu or other sources to English using OpenAI's GPT-3.5. It scrapes novel content, translates it using the OpenAI API, and generates an EPUB file for easy reading. Additionally, it supports uploading existing EPUB files in different languages, translating their contents, and preserving the original writing style and formatting.

## Description

This project provides a complete solution for translating webnovel chapters:
- **Scraping**: Retrieves chapter URLs and content from a specified novel on Syosetu.
- **Translation**: Uses OpenAI's GPT-3.5 to translate the scraped content, preserving the original author's writing style and HTML formatting.
- **EPUB Generation**: Compiles the translated content into an EPUB file.
- **EPUB Upload and Translation**: Allows users to upload existing EPUB files, translates the content, and regenerates the EPUB file with preserved formatting and metadata.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/JDH121702/Syosetu-Webnovel-AI-Translator
    cd Syosetu-Webnovel-AI-Translator
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    - Create a `.env` file in the root directory of the project and add your OpenAI API key:
      ```plaintext
      OPENAI_API_KEY=your_openai_api_key
      ```

## Usage

1. **Run the Translator**:
    ```sh
    python translator_gui.py
    ```

2. **Enter the Novel URL** (For Scraping and Translation):
    - Provide the URL of the webnovel you want to translate from Syosetu.

3. **Upload an EPUB File** (For EPUB Translation):
    - Click the "Browse..." button next to "Upload EPUB" to select an EPUB file from your local machine.

4. **Configure Translation**:
    - Enter the title, author, and filename for the EPUB output.
    - Choose the output directory and optional cover image.
    - If scraping, configure the number of chapters to translate.
    - If uploading an EPUB, the chapters and metadata will be loaded automatically.

5. **Generate the EPUB**:
    - Click on the appropriate buttons in the GUI to fetch chapters, translate, and generate the EPUB file.

## Features

- **Preserves Original Writing Style**: Translations aim to maintain the author's unique writing style.
- **HTML Tag Preservation**: Ensures that HTML formatting is preserved in the translated content.
- **Metadata Handling**: Automatically reads and includes metadata such as title, author, and cover image from uploaded EPUB files.

## Planned Updates:

1. **Enhanced Chapter Headers**: Improved formatting for chapter headers.
2. **Universal Scraping**: Extend scraping capabilities to work with more websites.
3. **Multi-Language Support**: Support for translating to more languages.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes and commit them**:
    ```sh
    git commit -m 'Add some feature'
    ```
4. **Push to the branch**:
    ```sh
    git push origin feature/your-feature-name
    ```
5. **Create a new Pull Request**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
