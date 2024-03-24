## Installation

1. Navigate to the project directory:
    ```bash
    cd main
    ```

2. Install project dependencies from `requirements/base.txt`:
    ```bash
    pip install -r requirements/base.txt
    ```

3. Apply migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

## Usage

1. Run the development server:
    ```bash
    python manage.py runserver
    ```

2. After you're done, navigate back to the project root:
    ```bash
    cd ..
    ```

3. Navigate to the `url_scraper` directory:
    ```bash
    cd url_scraper
    ```

4. Start the URL spider to scrape URLs from a given website:
    ```bash
    scrapy crawl url_spider -a url="http://example.com"
    ```
