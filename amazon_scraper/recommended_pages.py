import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, quote
import time
import random
from fake_useragent import UserAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_amazon_page(url, max_retries=3):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            logger.warning(f"Error fetching {url}: {e}")
            if attempt == max_retries - 1:
                raise
        time.sleep(random.uniform(5, 10))


def get_book_info(item):
    link = item.select_one("a.a-link-normal")
    img = item.select_one("img.s-image")
    return {
        "link": urljoin("https://www.amazon.co.jp", link["href"]) if link else "N/A",
        "image": img["src"] if img else "N/A",
    }


def scrape_amazon_books(initial_search, max_books=100):
    all_books = []
    current_search = initial_search
    page = 1

    while len(all_books) < max_books:
        logger.info(f"Searching for '{current_search}' - Page {page}")
        url = f"https://www.amazon.co.jp/s?k={quote(current_search)}&i=stripbooks&page={page}"

        try:
            soup = get_amazon_page(url)
            search_results = soup.select("div[data-component-type='s-search-result']")

            if not search_results:
                logger.warning("No search results found. Ending search.")
                break

            for item in search_results:
                book_info = get_book_info(item)
                if book_info["link"] != "N/A" and book_info["image"] != "N/A":
                    all_books.append(book_info)
                    if len(all_books) >= max_books:
                        break

            page += 1
            if page > 5:  # Limit to 5 pages per search term
                logger.info("Reached page limit. Changing search term.")
                current_search = all_books[-1]["link"].split("/")[-1]
                page = 1

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            break

        time.sleep(random.uniform(5, 10))

    return all_books[:max_books]


def save_to_csv(data, filename="recommended_pages.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["link", "image"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)


initial_search = "デザイン経営"
scraped_data = scrape_amazon_books(initial_search)
save_to_csv(scraped_data)
logger.info(f"Data has been saved to recommended_pages.csv")
logger.info(f"Total books scraped: {len(scraped_data)}")
