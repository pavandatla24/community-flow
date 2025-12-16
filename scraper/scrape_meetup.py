import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

BASE_URLS = [
    "https://www.meetup.com/find/?location=us--il--Chicago&keywords=yoga",
    "https://www.meetup.com/find/?location=us--il--Chicago&keywords=wellness",
    "https://www.meetup.com/find/?location=us--il--Chicago&keywords=meditation",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

def scrape_meetup():
    print("Scraping Meetup...")
    results = []

    for url in BASE_URLS:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "html.parser")

        cards = soup.select("li.searchResultCard-1")

        for card in cards:
            title = card.select_one("h3").get_text(strip=True) if card.select_one("h3") else None
            desc = card.select_one("p").get_text(strip=True) if card.select_one("p") else None
            link_tag = card.select_one("a")
            link = link_tag["href"] if link_tag else None

            results.append({
                "title": title,
                "text": desc,
                "date": None,
                "link": link,
                "source": "Meetup",
                "neighborhood": "Chicago",
            })

    # Save results
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/meetup_{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(results)} items → {filename}")
    return results


if __name__ == "__main__":
    scrape_meetup()
