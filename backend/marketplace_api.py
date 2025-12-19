"""
Flask API for KisanMitra Marketplace
Handles listings, orders, and users
Run on port 5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import database as db

app = Flask(__name__)
CORS(app)

# ==================== LISTINGS ENDPOINTS ====================

@app.route('/api/listings', methods=['GET'])
def get_listings():
    """Get all listings, optionally filtered by status"""
    status = request.args.get('status')
    listings = db.get_all_listings(status=status)
    return jsonify(listings)

@app.route('/api/listings/<listing_id>', methods=['GET'])
def get_listing(listing_id):
    """Get a single listing by ID"""
    listing = db.get_listing_by_id(listing_id)
    if listing:
        return jsonify(listing)
    return jsonify({'error': 'Listing not found'}), 404

@app.route('/api/listings', methods=['POST'])
def create_listing():
    """Create a new listing"""
    data = request.json
    listing = db.create_listing(data)
    return jsonify(listing), 201

@app.route('/api/listings/<listing_id>', methods=['PUT'])
def update_listing(listing_id):
    """Update a listing"""
    data = request.json
    success = db.update_listing(listing_id, data)
    if success:
        return jsonify({'message': 'Listing updated'})
    return jsonify({'error': 'Failed to update'}), 400

@app.route('/api/listings/<listing_id>', methods=['DELETE'])
def delete_listing(listing_id):
    """Delete a listing"""
    success = db.delete_listing(listing_id)
    if success:
        return jsonify({'message': 'Listing deleted'})
    return jsonify({'error': 'Failed to delete'}), 400

@app.route('/api/listings/farmer/<farmer_id>', methods=['GET'])
def get_farmer_listings(farmer_id):
    """Get all listings for a specific farmer by farmerId"""
    listings = db.get_farmer_listings(farmer_id)
    return jsonify(listings)

@app.route('/api/listings/phone/<phone>', methods=['GET'])
def get_farmer_listings_by_phone(phone):
    """Get all listings for a specific farmer by phone number - NEW ENDPOINT"""
    print(f"📞 API: Fetching listings for phone: {phone}")
    
    # Query MongoDB for listings with this farmerPhone
    from database import listings_collection, serialize_docs
    docs = listings_collection.find({'farmerPhone': phone}).sort('createdAt', -1)
    listings = serialize_docs(list(docs))
    
    print(f"✅ API: Found {len(listings)} listings for phone {phone}")
    return jsonify(listings)

# ==================== ORDERS ENDPOINTS ====================

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.json
    order = db.create_order(data)
    return jsonify(order), 201

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order by ID"""
    order = db.get_order_by_id(order_id)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/orders/buyer/<buyer_id>', methods=['GET'])
def get_buyer_orders(buyer_id):
    """Get all orders for a buyer"""
    orders = db.get_buyer_orders(buyer_id)
    return jsonify(orders)

@app.route('/api/orders/farmer/<farmer_id>', methods=['GET'])
def get_farmer_orders(farmer_id):
    """Get all orders for a farmer"""
    orders = db.get_farmer_orders(farmer_id)
    return jsonify(orders)

@app.route('/api/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    data = request.json
    status = data.get('status')
    additional = data.get('additional_data')
    success = db.update_order_status(order_id, status, additional)
    if success:
        return jsonify({'message': 'Status updated'})
    return jsonify({'error': 'Failed to update'}), 400

@app.route('/api/orders/<order_id>/payment', methods=['POST'])
def record_payment(order_id):
    """Record payment for an order"""
    data = request.json
    blockchain_hash = db.record_payment(order_id, data)
    return jsonify({'blockchainHash': blockchain_hash})

# ==================== GUEST ORDERS ====================

@app.route('/api/orders/guest', methods=['POST'])
def create_guest_order():
    """Create order for guest (non-registered buyer)"""
    data = request.json
    # Generate a guest order
    order_data = {
        'buyerId': f"GUEST-{data['buyer']['phone'][-4:]}",
        'buyerName': data['buyer']['name'],
        'buyerPhone': data['buyer']['phone'],
        **{k: v for k, v in data.items() if k != 'buyer'}
    }
    order = db.create_order(order_data)
    return jsonify(order), 201

# ==================== USERS ENDPOINTS ====================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    data = request.json
    user = db.create_user(data)
    return jsonify(user), 201

@app.route('/api/users/phone/<phone>', methods=['GET'])
def get_user_by_phone(phone):
    """Get user by phone number"""
    user = db.get_user_by_phone(phone)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/buyers/check-phone/<phone>', methods=['GET'])
def check_phone_exists(phone):
    """Check if phone number is already registered"""
    user = db.get_user_by_phone(phone)
    if user:
        return jsonify({'exists': True, 'buyerType': user.get('type')})
    return jsonify({'exists': False})

# ==================== STATS ENDPOINTS ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get marketplace statistics"""
    stats = db.get_marketplace_stats()
    return jsonify(stats)

# ==================== TRANSACTIONS ENDPOINTS ====================

@app.route('/api/transactions/order/<order_id>', methods=['GET'])
def get_order_transactions(order_id):
    """Get all transactions for an order"""
    transactions = db.get_transactions_by_order(order_id)
    return jsonify(transactions)

@app.route('/api/transactions/search/<tx_hash>', methods=['GET'])
def search_transaction(tx_hash):
    """Search transaction by blockchain hash"""
    transaction = db.search_by_hash(tx_hash)
    if transaction:
        return jsonify(transaction)
    return jsonify({'error': 'Transaction not found'}), 404

# ==================== RUN ====================

if __name__ == '__main__':
    print("🚀 KisanMitra Marketplace API starting on http://localhost:5000")
    print("📋 Endpoints:")
    print("   GET  /api/listings")
    print("   GET  /api/listings/phone/<phone>  ← NEW ENDPOINT")
    print("   POST /api/orders/guest")
    app.run(debug=True, port=5000)
