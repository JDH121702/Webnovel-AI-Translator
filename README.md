# AI Syosetu Translator

This translator is a tool specifically designed for translating Syosetu webnovel chapters to English using OpenAI's GPT-3.5. It scrapes novel content, translates it using the OpenAI API, and generates an EPUB file for easy reading.

## Description

This project provides a complete solution for translating Syosetu webnovel chapters:
- **Scraping**: Retrieves chapter URLs and content from a specified novel on Syosetu.
- **Translation**: Uses OpenAI's GPT-3.5 to translate the scraped content.
- **EPUB Generation**: Compiles the translated content into an EPUB file.

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

2. **Enter the Novel URL**:
    - Provide the URL of the webnovel you want to translate from Syosetu.

3. **Configure Translation**:
    - Enter the title and filename for the EPUB output.
    - Choose the number of chapters to translate.

4. **Generate the EPUB**:
    - Click on the appropriate buttons in the GUI to fetch chapters, translate, and generate the EPUB file.

## Planned Updates:

1. **Headers**: Headers for each new chapter.
2. **Better Scraping so it can be used on any website**: Better scraping to be used more generally.
3. **More Lanugages**: Support for translating to more languages.

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
