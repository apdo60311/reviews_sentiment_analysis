# Sentiment Anlyser Web Application

This project is a web application for text analysis and generation. It uses Flask for the web framework and integrates various NLP tools for sentiment analysis and text generation.

## Project Structure

```
📦reviews_sentiment_analysis
 ┣ 📂analyser
 ┃ ┣ 📂ml
 ┃ ┃ ┣ 📂.ipynb_checkpoints
 ┃ ┃ ┃ ┗ 📜ml-book-checkpoint.ipynb
 ┃ ┃ ┣ 📜ml-book.ipynb
 ┃ ┃ ┣ 📜reviews_labeled.csv
 ┃ ┃ ┗ 📜TimeSeries.ipynb
 ┃ ┣ 📂web
 ┃ ┃ ┣ 📂static
 ┃ ┃ ┣ 📂templates
 ┃ ┃ ┃ ┣ 📜generate.html
 ┃ ┃ ┃ ┣ 📜index.html
 ┃ ┃ ┃ ┗ 📜scrapper.html
 ┃ ┃ ┣ 📂utils
 ┃ ┃ ┃ ┣ 📜gen_similar.py
 ┃ ┃ ┃ ┣ 📜scrap_analyser.py
 ┃ ┃ ┃ ┗ 📜seintmeint.py
 ┃ ┃ ┗ 📜app.py
 ┃ ┣ 📜collect_data.py
 ┃ ┣ 📜data-reviews.json
 ┃ ┣ 📜data.json
 ┃ ┣ 📜requirements.txt
 ┃ ┗ 📜reviews.json
 ┣ 📂data
 ┃ ┗ 📜reviews.csv
 ┣ 📂web-scrapper
 ┃ ┗ 📜web-scraper.rar
 ┣ 📜.gitignore
 ┗ 📜README.md
```

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/apdo60311/reviews_sentiment_analysis
    cd analyser
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    # Or use visual studio code to create venv
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```sh
    python web/app.py
    ```

2. Open your web browser and go to `http://localhost:5000`.

## Features

### Seintment Analysis

- **Sentiment Analysis**: Enter a comment to analyze its sentiment using the [seintmeint.analyze_sentiment]() function from [utils/seintmeint.py]().

### Generate Similar

- **Text Generation**: Enter a prompt to generate similar text using the [TextGenerator]() class from [utils/gen_similar.py]().

## Contributing

Contributions are welcome! Here are some ways you can contribute:

1. Report bugs and issues
2. Fix bugs and implement new features
3. Write documentation and improve existing docs
4. Suggest new features and improvements

### Steps to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request
