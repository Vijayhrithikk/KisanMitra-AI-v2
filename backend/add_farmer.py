import sys
sys.path.append('.')
from database import db

users_collection = db.users

# Add farmer 7330671778 to database
farmer_data = {
    'phone': '7330671778',
    'name': 'Test Farmer',
    'farmerId': 'FARMER-1778',
    'verified': True,
    'role': 'farmer',
    'createdAt': '2024-12-16T00:00:00Z'
}

result = users_collection.replace_one(
    {'phone': '7330671778'},
    farmer_data,
    upsert=True
)

if result.upserted_id:
    print(f'✅ Farmer 7330671778 CREATED in database')
else:
    print(f'✅ Farmer 7330671778 UPDATED in database')

# Verify
user = users_collection.find_one({'phone': '7330671778'})
print(f'\n📋 Farmer details:')
print(f'  Name: {user.get("name")}')
print(f'  Phone: {user.get("phone")}')
print(f'  Farmer ID: {user.get("farmerId")}')
print(f'  Verified: {user.get("verified")}')
