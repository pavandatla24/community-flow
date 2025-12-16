import json
import re
import html
import os

def clean_html(raw_text):
    # Remove HTML tags
    no_tags = re.sub(r"<.*?>", "", raw_text)

    # Convert HTML entities like &nbsp; to normal characters
    cleaned = html.unescape(no_tags)

    # Remove extra whitespace
    return cleaned.strip()

# Load file
input_file = "data/raw/google_rss_2025-12-04.json"
output_file = "data/clean/google_clean.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned = []
for item in data:
    item["text"] = clean_html(item["text"])
    cleaned.append(item)

os.makedirs("data/clean", exist_ok=True)

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

print(f"Saved cleaned dataset → {output_file}")
