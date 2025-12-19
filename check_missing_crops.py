import json

# Load both databases
crop_profiles = json.load(open('backend/ml_engine/data/crop_profiles.json'))
crop_npk = json.load(open('backend/ml_engine/data/crop_npk_requirements.json'))

# Get all crop names from profiles (these are what the frontend sends)
profile_crops = set(k.lower() for k in crop_profiles.keys())

# Get all crops in NPK database
npk_crops = set(crop_npk['crops'].keys())

# Find missing crops
missing = profile_crops - npk_crops

if missing:
    print(f"❌ Missing {len(missing)} crops in NPK database:")
    for crop in sorted(missing):
        print(f"   - {crop}")
        # Try to find similar
        similar = [c for c in npk_crops if crop[:4] in c or c[:4] in crop]
        if similar:
            print(f"     Similar: {similar}")
else:
    print("✅ All crops from crop_profiles.json have NPK data!")

print(f"\nTotal: {len(profile_crops)} in profiles, {len(npk_crops)} in NPK database")
