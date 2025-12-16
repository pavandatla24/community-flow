import json
import re
import string
from collections import Counter

# ----------------------------
# Helper Functions
# ----------------------------

def clean_entities(text):
    text = text.replace("&nbsp;", " ")
    text = text.replace("\u00a0", " ")
    return text.strip()

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    words = text.split()
    return words

# Basic stopwords list (small but effective)
STOPWORDS = {
    "the", "and", "a", "an", "to", "in", "for", "of", "on", "with", 
    "at", "by", "from", "is", "are", "that", "this"
}

def extract_keywords(text, top_n=5):
    words = tokenize(text)
    words = [w for w in words if w not in STOPWORDS]
    freq = Counter(words)
    keywords = [word for word, _ in freq.most_common(top_n)]
    return keywords

# ----------------------------
# Load Data
# ----------------------------
input_file = "data/clean/google_clean.json"
output_file = "data/clean/google_step2.json"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# ----------------------------
# Process Each Article
# ----------------------------
for item in data:
    text = item["text"]

    # Clean HTML entities
    cleaned_text = clean_entities(text)

    # Add new fields
    item["clean_text"] = cleaned_text
    item["keywords"] = extract_keywords(cleaned_text)

# ----------------------------
# Save Output
# ----------------------------
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Step 2 complete → Saved:", output_file)
