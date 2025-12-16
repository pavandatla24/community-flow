import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Get the project root directory (parent of nlp/)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

INPUT_FILE = os.path.join(project_root, "data", "labeled", "google_labeled.json")
OUTPUT_FILE = os.path.join(project_root, "data", "cleaned", "google_topics.json")

def load_data():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def build_topic_model():
    print("Loading cleaned + labeled data...")
    items = load_data()

    texts = [item["clean_text"] for item in items]

    print("Vectorizing text (TF-IDF)...")
    vectorizer = TfidfVectorizer(stop_words="english", min_df=2)
    X = vectorizer.fit_transform(texts)

    print("Clustering into 6 topics (KMeans)...")
    kmeans = KMeans(n_clusters=6, random_state=42, n_init="auto")
    clusters = kmeans.fit_predict(X)

    print("Adding topic_id to each item...")
    for item, cluster_id in zip(items, clusters):
        item["topic_id"] = int(cluster_id)

    save_data(items)
    print(f"Step 4 completed → Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    build_topic_model()
