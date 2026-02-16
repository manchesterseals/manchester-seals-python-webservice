from flask import Flask, jsonify
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'manchester_seals')
COLLECTION_NAME = 'roster'

# Test connection on startup
print("🚀 Starting Flask application...")
try:
    test_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    test_client.admin.command('ping')
    print(f"✅ MongoDB connection test successful at {MONGO_URI}")
    test_client.close()
except Exception as e:
    print(f"⚠️  MongoDB connection test failed: {e}")


@app.route('/api/roster', methods=['GET'])
def get_roster():
    """
    Endpoint to fetch all data from the roster collection
    Connect fresh on each request to ensure we get current data
    """
    try:
        # Create fresh connection for this request
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        db = client[DB_NAME]
        roster_collection = db[COLLECTION_NAME]

        # Test connection
        client.admin.command('ping')

        # Fetch all documents from roster collection
        roster_data = list(roster_collection.find({}))

        # Debug logging
        print(f"🔍 GET /api/roster - Found {len(roster_data)} documents in {DB_NAME}.{COLLECTION_NAME}")

        # Convert MongoDB ObjectId to string for JSON serialization
        for item in roster_data:
            item['_id'] = str(item['_id'])

        response = jsonify({
            'success': True,
            'count': len(roster_data),
            'data': roster_data
        })

        client.close()
        return response, 200

    except Exception as e:
        print(f"❌ Error in /api/roster: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Manchester Seals API'
    }), 200


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', False)
    )

