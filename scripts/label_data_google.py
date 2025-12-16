import json
import os

# Get the script directory and project root
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

# Load step2 cleaned + keyword data
input_path = os.path.join(project_root, "data", "clean", "google_step2.json")
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def assign_themes(item):
    text = item["clean_text"].lower()

    themes = []

    # 1. Stress Relief + Burnout Recovery
    if any(word in text for word in ["relax", "reset", "renewal", "mental", "stress", "burnout", "healing", "yoga", "retreat"]):
        themes.append(1)

    # 2. Body Love + Self-Image
    if any(word in text for word in ["body", "self", "image", "muffins", "baths", "spa"]):
        themes.append(2)

    # 3. Movement Access + Beginner-Friendly
    if any(word in text for word in ["meditation", "movement", "beginners", "try", "experiences"]):
        themes.append(3)

    # 4. Cultural / Spiritual Connection
    if any(word in text for word in ["spiritual", "culture", "community", "mindfulness", "nature", "sanctuaries", "healing arts"]):
        themes.append(4)

    # 5. Financial Access + Mutual Aid
    if any(word in text for word in ["free", "access", "affordable", "low cost"]):
        themes.append(5)

    # 6. Community Care + Solidarity
    if any(word in text for word in ["safe spaces", "community", "together", "group", "nonprofit", "support"]):
        themes.append(6)

    # Default theme if nothing matched
    if not themes:
        themes = [1]

    return themes

# Apply theme assignment
for item in data:
    item["themes"] = assign_themes(item)

# Save step3 output
output_path = os.path.join(project_root, "data", "labeled", "google_labeled.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("STEP 3 DONE → google_labeled.json created.")
