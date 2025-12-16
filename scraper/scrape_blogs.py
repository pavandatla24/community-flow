import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

BLOG_SOURCES = [
    "https://chicagomindfulcollective.com/blog/",
    "https://www.yogasix.com/blog",
    "https://www.mindful.org/category/news/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_blogs():
    print("Scraping Chicago wellness blogs...")
    results = []

    for url in BLOG_SOURCES:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        # Catch all paragraphs (blogs are long)
        paragraphs = soup.find_all("p")

        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) < 40:  # skip small junk
                continue

            results.append({
                "title": None,
                "text": text,
                "date": None,
                "link": url,
                "source": "Blog",
                "neighborhood": "Chicago"
            })

    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/blogs_{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(results)} items → {filename}")
    return results


if __name__ == "__main__":
    scrape_blogs()
