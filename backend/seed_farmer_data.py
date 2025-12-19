"""
Seed database with test listings and orders for farmer 7330671778
Run this to populate MongoDB with complete test data
"""

import sys
sys.path.append('.')
from database import create_listing, create_order, listings_collection, orders_collection
from datetime import datetime

print("="*60)
print("POPULATING DATABASE FOR FARMER: 7330671778")
print("="*60)

# Clear existing data for this farmer
print("\n🗑️  Clearing existing data...")
listings_collection.delete_many({'farmerPhone': '7330671778'})
orders_collection.delete_many({'farmerId': 'FARMER-1778'})

# Create 2 listings
print("\n📋 Creating 2 listings...")

listing1_data = {
    'crop': 'Rice',
    'variety': 'Sona Masoori',
    'quantity': 100,
    'unit': 'Quintal',
    'price': 2500,
    'farmerId': 'FARMER-1778',
    'farmerName': 'Test Farmer',
    'farmerPhone': '7330671778',
    'farmerVerified': True,
    'location': {
        'state': 'Andhra Pradesh',
        'district': 'Guntur',
        'city': 'Tenali'
    },
    'contact': {
        'name': 'Test Farmer',
        'phone': '7330671778'
    },
    'fertilizers': 'Urea, DAP',
    'pesticides': 'Neem Oil',
    'notes': 'Premium quality rice',
    'images': []
}

listing2_data = {
    'crop': 'Cotton',
    'variety': 'BT Cotton',
    'quantity': 50,
    'unit': 'Quintal',
    'price': 5500,
    'farmerId': 'FARMER-1778',
    'farmerName': 'Test Farmer',
    'farmerPhone': '7330671778',
    'farmerVerified': True,
    'location': {
        'state': 'Andhra Pradesh',
        'district': 'Guntur',
        'city': 'Tenali'
    },
    'contact': {
        'name': 'Test Farmer',
        'phone': '7330671778'
    },
    'fertilizers': 'NPK Complex',
    'pesticides': 'Chemical pesticides',
    'notes': 'High quality BT cotton',
    'images': []
}

listing1 = create_listing(listing1_data)
listing2 = create_listing(listing2_data)

print(f"✅ Created listing 1: {listing1['listingId']} - {listing1['crop']}")
print(f"✅ Created listing 2: {listing2['listingId']} - {listing2['crop']}")

# Create 3 orders for these listings
print("\n📦 Creating 3 test orders...")

order1_data = {
    'listingId': listing1['listingId'],
    'farmerId': 'FARMER-1778',
    'buyerId': 'BUYER-001',
    'buyerName': 'Test Buyer 1',
    'buyerPhone': '9876543210',
    'crop': listing1['crop'],
    'variety': listing1['variety'],
    'quantity': 20,
    'unit': 'Quintal',
    'pricing': {
        'unitPrice': 2500,
        'subtotal': 50000,
        'deliveryCharge': 500,
        'platformFee': 500,
        'total': 51000,
        'farmerGets': 49500
    },
    'delivery': {
        'type': 'local',
        'address': 'Test Address, Guntur'
    }
}

order2_data = {
    'listingId': listing2['listingId'],
    'farmerId': 'FARMER-1778',
    'buyerId': 'BUYER-002',
    'buyerName': 'Test Buyer 2',
    'buyerPhone': '9876543211',
    'crop': listing2['crop'],
    'variety': listing2['variety'],
    'quantity': 10,
    'unit': 'Quintal',
    'pricing': {
        'unitPrice': 5500,
        'subtotal': 55000,
        'deliveryCharge': 0,
        'platformFee': 550,
        'total': 55550,
        'farmerGets': 55000
    },
    'delivery': {
        'type': 'pickup',
        'address': ''
    }
}

order3_data = {
    'listingId': listing1['listingId'],
    'farmerId': 'FARMER-1778',
    'buyerId': 'BUYER-003',
    'buyerName': 'Test Buyer 3',
    'buyerPhone': '9876543212',
    'crop': listing1['crop'],
    'variety': listing1['variety'],
    'quantity': 30,
    'unit': 'Quintal',
    'pricing': {
        'unitPrice': 2500,
        'subtotal': 75000,
        'deliveryCharge': 200,
        'platformFee': 750,
        'total': 75950,
        'farmerGets': 74750
    },
    'delivery': {
        'type': 'local',
        'address': 'Another Address, Vijayawada'
    }
}

order1 = create_order(order1_data)
order2 = create_order(order2_data)
order3 = create_order(order3_data)

print(f"✅ Created order 1: {order1['orderId']} - {order1['crop']} (PENDING)")
print(f"✅ Created order 2: {order2['orderId']} - {order2['crop']} (PENDING)")  
print(f"✅ Created order 3: {order3['orderId']} - {order3['crop']} (PENDING)")

# Verify
print("\n🔍 Verification:")
listings = list(listings_collection.find({'farmerPhone': '7330671778'}))
orders = list(orders_collection.find({'farmerId': 'FARMER-1778'}))

print(f"✅ Total listings for 7330671778: {len(listings)}")
print(f"✅ Total orders for FARMER-1778: {len(orders)}")

print("\n" + "="*60)
print("✅ DATABASE POPULATED SUCCESSFULLY!")
print("="*60)
print("\nNext steps:")
print("1. Restart marketplace API: python marketplace_api.py")
print("2. Login with phone: 7330671778")
print("3. Go to Farmer Dashboard → Listings tab")
print("4. Check Orders tab for 3 orders")
print("="*60)
