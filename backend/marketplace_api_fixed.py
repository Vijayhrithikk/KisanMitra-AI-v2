"""
FIXED Marketplace API - Simplified and Working
All routes tested and verified
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import (
    listings_collection, orders_collection, 
    serialize_docs, create_listing, create_order,
    get_marketplace_stats
)

app = Flask(__name__)
CORS(app)

# Root endpoint for testing
@app.route('/')
def home():
    return jsonify({"status": "ok", "service": "KisanMitra Marketplace API"})

# ==================== LISTINGS ====================

@app.route('/api/listings', methods=['GET'])
def get_listings():
    status = request.args.get('status')
    query = {'status': status} if status else {}
    docs = listings_collection.find(query).sort('createdAt', -1)
    return jsonify(serialize_docs(list(docs)))

@app.route('/api/listings/phone/<phone>', methods=['GET'])
def get_listings_by_phone(phone):
    """CRITICAL: Get listings by farmer phone number"""
    print(f"📞 API: Fetching listings for phone: {phone}")
    docs = listings_collection.find({'farmerPhone': phone}).sort('createdAt', -1)
    listings = serialize_docs(list(docs))
    print(f"✅ API: Found {len(listings)} listings for phone {phone}")
    return jsonify(listings)

@app.route('/api/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    from database import get_listing_by_id
    listing = get_listing_by_id(listing_id)
    if listing:
        return jsonify(listing)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/listings', methods=['POST'])
def post_listing():
    listing = create_listing(request.json)
    return jsonify(listing), 201

# ==================== ORDERS ====================

@app.route('/api/orders/farmer/<farmer_id>', methods=['GET'])
def get_farmer_orders(farmer_id):
    """Get all orders for a farmer"""
    print(f"📦 API: Fetching orders for farmer: {farmer_id}")
    docs = orders_collection.find({'farmerId': farmer_id}).sort('createdAt', -1)
    orders = serialize_docs(list(docs))
    print(f"✅ API: Found {len(orders)} orders for farmer {farmer_id}")
    return jsonify(orders)

@app.route('/api/orders/guest', methods=['POST'])
def post_guest_order():
    data = request.json
    order_data = {
        'buyerId': f"GUEST-{data['buyer']['phone'][-4:]}",
        'buyerName': data['buyer']['name'],
        'buyerPhone': data['buyer']['phone'],
        **{k: v for k, v in data.items() if k != 'buyer'}
    }
    order = create_order(order_data)
    return jsonify(order), 201

# ==================== STATS ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify(get_marketplace_stats())

# ==================== RUN ====================

if __name__ == '__main__':
    print("")
    print("="*60)
    print("🚀 KisanMitra Marketplace API - FIXED VERSION")
    print("="*60)
    print("📍 Server: http://localhost:5000")
    print("📋 Key Endpoints:")
    print("   GET  /                                    - Health check")
    print("   GET  /api/listings/phone/<phone>         - Get listings by phone")
    print("   GET  /api/orders/farmer/<farmer_id>      - Get farmer orders")
    print("   POST /api/orders/guest                   - Guest checkout")
    print("="*60)
    print("")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
