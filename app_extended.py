"""
Advanced Flask application with extended features for Manchester Seals API
This file can be used as an extension or replacement for app.py with more features
"""

from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB connection setup
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'manchester_seals')
COLLECTION_NAME = 'roster'

try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    roster_collection = db[COLLECTION_NAME]
    # Test connection
    client.admin.command('ping')
    print(f"Successfully connected to MongoDB at {MONGO_URI}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    roster_collection = None


def convert_objectid(document):
    """Convert ObjectId to string in document"""
    if document and '_id' in document:
        document['_id'] = str(document['_id'])
    return document


def convert_objectid_list(documents):
    """Convert ObjectIds to strings in list of documents"""
    return [convert_objectid(doc) for doc in documents]


# ==================== ROSTER ENDPOINTS ====================

@app.route('/api/roster', methods=['GET'])
def get_roster():
    """
    Fetch all roster data with optional pagination and filtering
    Query parameters:
    - page: Page number (default: 1)
    - limit: Results per page (default: 10)
    - search: Search by name
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        search = request.args.get('search', '', type=str)

        # Ensure valid pagination
        page = max(page, 1)
        limit = min(max(limit, 1), 100)  # Max 100 per page

        # Build query
        query = {}
        if search:
            query['name'] = {'$regex': search, '$options': 'i'}

        # Get total count
        total = roster_collection.count_documents(query)

        # Fetch paginated data
        skip = (page - 1) * limit
        roster_data = list(roster_collection.find(query).skip(skip).limit(limit))
        roster_data = convert_objectid_list(roster_data)

        return jsonify({
            'success': True,
            'count': len(roster_data),
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit,
            'data': roster_data
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/roster/<id>', methods=['GET'])
def get_roster_by_id(id):
    """
    Fetch a single roster entry by ID
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        try:
            object_id = ObjectId(id)
        except:
            return jsonify({
                'success': False,
                'error': 'Invalid ID format'
            }), 400

        data = roster_collection.find_one({'_id': object_id})

        if data:
            data = convert_objectid(data)
            return jsonify({
                'success': True,
                'data': data
            }), 200

        return jsonify({
            'success': False,
            'error': 'Roster entry not found'
        }), 404

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/roster', methods=['POST'])
def create_roster():
    """
    Create a new roster entry
    Request body should be JSON:
    {
        "name": "John Doe",
        "position": "Manager",
        "department": "Operations",
        "email": "john@example.com"
    }
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Validate required fields
        if 'name' not in data or not data['name']:
            return jsonify({
                'success': False,
                'error': 'Name is required'
            }), 400

        # Insert document
        result = roster_collection.insert_one(data)

        return jsonify({
            'success': True,
            'id': str(result.inserted_id),
            'message': 'Roster entry created successfully'
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/roster/<id>', methods=['PUT'])
def update_roster(id):
    """
    Update a roster entry by ID
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        try:
            object_id = ObjectId(id)
        except:
            return jsonify({
                'success': False,
                'error': 'Invalid ID format'
            }), 400

        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Update document
        result = roster_collection.update_one(
            {'_id': object_id},
            {'$set': data}
        )

        if result.matched_count == 0:
            return jsonify({
                'success': False,
                'error': 'Roster entry not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Roster entry updated successfully',
            'modified_count': result.modified_count
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/roster/<id>', methods=['DELETE'])
def delete_roster(id):
    """
    Delete a roster entry by ID
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        try:
            object_id = ObjectId(id)
        except:
            return jsonify({
                'success': False,
                'error': 'Invalid ID format'
            }), 400

        result = roster_collection.delete_one({'_id': object_id})

        if result.deleted_count == 0:
            return jsonify({
                'success': False,
                'error': 'Roster entry not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Roster entry deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== STATISTICS ENDPOINTS ====================

@app.route('/api/roster/stats/count', methods=['GET'])
def get_roster_count():
    """
    Get total count of roster entries
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        count = roster_collection.count_documents({})

        return jsonify({
            'success': True,
            'count': count
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/roster/stats/by-department', methods=['GET'])
def get_stats_by_department():
    """
    Get roster count grouped by department
    """
    try:
        if roster_collection is None:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500

        pipeline = [
            {
                '$group': {
                    '_id': '$department',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            }
        ]

        stats = list(roster_collection.aggregate(pipeline))

        return jsonify({
            'success': True,
            'data': stats
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ==================== HEALTH & INFO ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    db_status = 'connected' if roster_collection else 'disconnected'
    return jsonify({
        'status': 'healthy',
        'service': 'Manchester Seals API',
        'database': db_status
    }), 200


@app.route('/api/info', methods=['GET'])
def api_info():
    """
    API information and available endpoints
    """
    endpoints = {
        'GET /api/roster': 'Fetch all roster data (supports pagination and search)',
        'GET /api/roster/<id>': 'Fetch a single roster entry by ID',
        'POST /api/roster': 'Create a new roster entry',
        'PUT /api/roster/<id>': 'Update a roster entry by ID',
        'DELETE /api/roster/<id>': 'Delete a roster entry by ID',
        'GET /api/roster/stats/count': 'Get total roster count',
        'GET /api/roster/stats/by-department': 'Get roster count by department',
        'GET /api/health': 'Health check',
        'GET /api/info': 'API information'
    }

    return jsonify({
        'service': 'Manchester Seals API',
        'version': '1.0.0',
        'endpoints': endpoints
    }), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', False)
    )

