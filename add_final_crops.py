import json

# Load existing data
path = 'backend/ml_engine/data/crop_npk_requirements.json'
with open(path, 'r') as f:
    data = json.load(f)

# Add the 3 missing fruit crops
final_crops = {
    "orange": {
        "name": "Orange (Citrus)",
        "npk_per_tree_per_year": {
            "n": 500,
            "p": 250,
            "k": 500
        },
        "trees_per_acre": 80,
        "target_yield_kg_per_tree": 80,
        "notes": "Citrus fruit. High K for fruit quality. Split applications recommended. Micronutrients important."
    },
    "pomegranate": {
        "name": "Pomegranate",
        "npk_per_acre": {
            "n": 120,
            "p": 80,
            "k": 120
        },
        "npk_per_hectare": {
            "n": 300,
            "p": 200,
            "k": 300
        },
        "target_yield_tons_per_acre": 4.0,
        "notes": "Fruit crop. Balanced NPK. Micronutrients (Zn, Fe, Mn) critical for fruit quality."
    },
    "watermelon": {
        "name": "Watermelon",
        "npk_per_acre": {
            "n": 100,
            "p": 60,
            "k": 100
        },
        "npk_per_hectare": {
            "n": 250,
            "p": 150,
            "k": 250
        },
        "target_yield_tons_per_acre": 15.0,
        "notes": "Cucurbit. High water need. High K for fruit sweetness. Drip fertigation ideal."
    }
}

# Add to data
data['crops'].update(final_crops)

# Save
with open(path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"✅ Added {len(final_crops)} final crops")
print(f"📊 Total crops now: {len(data['crops'])}")
print(f"New crops: {', '.join(final_crops.keys())}")
