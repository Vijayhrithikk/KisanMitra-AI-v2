import json
import os

# Load existing data
path = 'backend/ml_engine/data/crop_npk_requirements.json'
with open(path, 'r') as f:
    data = json.load(f)

# Add missing crops
new_crops = {
    "millets": {
        "name": "Millets (Pearl/Finger)",
        "npk_per_acre": {"n": 40, "p": 40, "k": 20},
        "npk_per_hectare": {"n": 100, "p": 100, "k": 50},
        "target_yield_tons_per_acre": 1.0,
        "notes": "Climate-resilient nutri-cereals. Low input requirements."
    },
    "tobacco": {
        "name": "Tobacco",
        "npk_per_acre": {"n": 60, "p": 40, "k": 120},
        "npk_per_hectare": {"n": 150, "p": 100, "k": 300},
        "target_yield_tons_per_acre": 1.0,
        "notes": "High potassium for leaf quality. Avoid chloride fertilizers."
    },
    "turmeric": {
        "name": "Turmeric",
        "npk_per_acre": {"n": 60, "p": 50, "k": 120},
        "npk_per_hectare": {"n": 150, "p": 125, "k": 300},
        "target_yield_tons_per_acre": 4.0,
        "notes": "Long-duration spice crop. High potassium. FYM essential."
    },
    "pulses": {
        "name": "Pulses (Red Gram/Arhar)",
        "npk_per_acre": {"n": 20, "p": 60, "k": 30},
        "npk_per_hectare": {"n": 50, "p": 150, "k": 75},
        "target_yield_tons_per_acre": 0.8,
        "notes": "Legume. N-fixing. High P need. Rhizobium treatment."
    },
    "oil seeds": {
        "name": "Oil Seeds (Mustard/Sunflower)",
        "npk_per_acre": {"n": 60, "p": 40, "k": 30},
        "npk_per_hectare": {"n": 150, "p": 100, "k": 75},
        "target_yield_tons_per_acre": 1.2,
        "notes": "Sulphur critical for oil content."
    },
    "barley": {
        "name": "Barley",
        "npk_per_acre": {"n": 60, "p": 40, "k": 30},
        "npk_per_hectare": {"n": 150, "p": 100, "k": 75},
        "target_yield_tons_per_acre": 2.0,
        "notes": "Drought and salinity tolerant. Moderate needs."
    },
    "bengal gram": {
        "name": "Bengal Gram (Chickpea)",
        "npk_per_acre": {"n": 20, "p": 60, "k": 30},
        "npk_per_hectare": {"n": 50, "p": 150, "k": 75},
        "target_yield_tons_per_acre": 1.0,
        "notes": "Major pulse. Legume with N-fixation. High P."
    },
    "cabbage": {
        "name": "Cabbage",
        "npk_per_acre": {"n": 150, "p": 75, "k": 75},
        "npk_per_hectare": {"n": 375, "p": 187, "k": 187},
        "target_yield_tons_per_acre": 12.0,
        "notes": "Heavy feeder. Boron needed."
    },
    "cauliflower": {
        "name": "Cauliflower",
        "npk_per_acre": {"n": 120, "p": 60, "k": 60},
        "npk_per_hectare": {"n": 300, "p": 150, "k": 150},
        "target_yield_tons_per_acre": 10.0,
        "notes": "Boron and molybdenum important."
    },
    "brinjal": {
        "name": "Brinjal (Eggplant)",
        "npk_per_acre": {"n": 100, "p": 50, "k": 50},
        "npk_per_hectare": {"n": 250, "p": 125, "k": 125},
        "target_yield_tons_per_acre": 8.0,
        "notes": "Long-duration vegetable. Regular feeding."
    },
    "okra": {
        "name": "Okra (Bhindi)",
        "npk_per_acre": {"n": 80, "p": 40, "k": 40},
        "npk_per_hectare": {"n": 200, "p": 100, "k": 100},
        "target_yield_tons_per_acre": 4.0,
        "notes": "Warm season crop. Drought tolerant."
    },
    "carrot": {
        "name": "Carrot",
        "npk_per_acre": {"n": 50, "p": 50, "k": 75},
        "npk_per_hectare": {"n": 125, "p": 125, "k": 187},
        "target_yield_tons_per_acre": 8.0,
        "notes": "High K for root development. Avoid fresh manure."
    },
    "guava": {
        "name": "Guava",
        "npk_per_tree_per_year": {"n": 400, "p": 200, "k": 400},
        "trees_per_acre": 100,
        "target_yield_kg_per_tree": 50,
        "notes": "Hardy fruit tree. Apply in 3-4 split doses."
    },
    "paddy": {
        "name": "Paddy (alias for Rice)",
        "npk_per_acre": {"n": 120, "p": 60, "k": 40},
        "npk_per_hectare": {"n": 300, "p": 150, "k": 100},
        "target_yield_tons_per_acre": 3.0,
        "notes": "Same as rice. High nitrogen requirement."
    },
    "ground nuts": {
        "name": "Ground Nuts (alias)",
        "npk_per_acre": {"n": 25, "p": 60, "k": 40},
        "npk_per_hectare": {"n": 62.5, "p": 150, "k": 100},
        "target_yield_tons_per_acre": 1.2,
        "notes": "Legume. Gypsum critical. Low N needed."
    }
}

# Add to data
data['crops'].update(new_crops)

# Save
with open(path, 'w') as f:
    json.dump(data, f, indent=4)

print(f"✅ Added {len(new_crops)} crops. Total now: {len(data['crops'])}")
print(f"New crops: {', '.join(new_crops.keys())}")
