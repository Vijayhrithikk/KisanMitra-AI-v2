import sys
sys.path.append('.')
from database import listings_collection, orders_collection

print("="*50)
print("CHECKING DATABASE FOR PHONE: 7330671778")
print("="*50)

# Check listings
listings = list(listings_collection.find({}))
print(f"\n📋 Total listings in database: {len(listings)}")

if listings:
    print("\n📋 First 5 listings:")
    for i, listing in enumerate(listings[:5], 1):
        print(f"\n  Listing {i}:")
        print(f"    Crop: {listing.get('crop')}")
        print(f"    farmerId: {listing.get('farmerId')}")
        print(f"    farmerPhone: {listing.get('farmerPhone')}")
        print(f"    listingId: {listing.get('listingId')}")

# Check for specific phone
phone_listings = list(listings_collection.find({'farmerPhone': '7330671778'}))
print(f"\n📞 Listings for phone 7330671778: {len(phone_listings)}")
for listing in phone_listings:
    print(f"  - {listing.get('crop')} ({listing.get('listingId')})")

# Check orders
orders = list(orders_collection.find({}))
print(f"\n📦 Total orders in database: {len(orders)}")

if orders:
    print("\n📦 First 3 orders:")
    for i, order in enumerate(orders[:3], 1):
        print(f"\n  Order {i}:")
        print(f"    orderId: {order.get('orderId')}")
        print(f"    farmerId: {order.get('farmerId')}")
        print(f"    buyerId: {order.get('buyerId')}")
        print(f"    crop: {order.get('crop')}")
        print(f"    status: {order.get('status')}")

print("\n" + "="*50)
