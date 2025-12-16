import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

RSS_URL = "https://news.google.com/rss/search?q=chicago+wellness+mindfulness+healing&hl=en-US&gl=US&ceid=US:en"

def scrape_google_rss():
    print("Scraping Google News RSS...")

    response = requests.get(RSS_URL)
    root = ET.fromstring(response.text)

    items = root.findall(".//item")
    results = []

    for item in items:
        title = item.find("title").text if item.find("title") is not None else None
        link = item.find("link").text if item.find("link") is not None else None
        description = item.find("description").text if item.find("description") is not None else None
        pubdate = item.find("pubDate").text if item.find("pubDate") is not None else None

        results.append({
            "title": title,
            "text": description,
            "date": pubdate,
            "link": link,
            "source": "Google News RSS",
            "neighborhood": "Chicago"
        })

    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/google_rss_{datetime.now().strftime('%Y-%m-%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(results)} items → {filename}")


if __name__ == "__main__":
    scrape_google_rss()
