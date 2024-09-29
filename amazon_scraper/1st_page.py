import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse, parse_qs, urlencode


def scrape_amazon(max_items=200):
    base_url = "https://www.amazon.co.jp/s"
    params = {
        "k": "デザイン経営",
        "__mk_ja_JP": "カタカナ",
        "crid": "1HRWFCZGP3Y5D",
        "sprefix": "デザイン経営,aps,172",
        "ref": "nb_sb_noss_1",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    results = []
    page = 1

    while len(results) < max_items:
        params["page"] = page
        url = f"{base_url}?{urlencode(params)}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        items = soup.select("div[data-component-type='s-search-result']")

        for item in items:
            if len(results) >= max_items:
                break

            link = item.select_one("a.a-link-normal.s-no-outline")
            img = item.select_one("img.s-image")

            if link and img:
                results.append(
                    {
                        "type": "picked",
                        "link": urljoin(base_url, link.get("href")),
                        "image": img.get("src"),
                    }
                )

        if not items:
            break

        page += 1

    return results[:max_items]


def save_to_csv(data, filename="1st_page.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["type", "link", "image"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)


scraped_data = scrape_amazon(200)
save_to_csv(scraped_data)
print(f"Data has been saved to 1st_page.csv")
print(f"Total items scraped: {len(scraped_data)}")
