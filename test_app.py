"""
Unit tests for the Manchester Seals API
"""
import unittest
import json
import os
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
from bson import ObjectId
from app import app

load_dotenv()


class RosterAPITestCase(unittest.TestCase):
    """Test cases for roster API endpoints"""

    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_health_check_endpoint(self):
        """Test health check endpoint returns 200"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    @patch('app.MongoClient')
    def test_get_roster_success(self, mock_mongo_client):
        """Test getting roster data successfully"""
        # Mock MongoDB client and collection
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()

        mock_mongo_client.return_value = mock_client
        mock_client.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection

        # Mock successful connection test
        mock_client.admin.command.return_value = {'ok': 1}

        # Mock MongoDB find response
        mock_collection.find.return_value = [
            {
                '_id': ObjectId('507f1f77bcf86cd799439011'),
                'name': 'John Doe',
                'position': 'Manager',
                'department': 'Operations'
            },
            {
                '_id': ObjectId('507f1f77bcf86cd799439012'),
                'name': 'Jane Smith',
                'position': 'Developer',
                'department': 'Engineering'
            }
        ]

        response = self.client.get('/api/roster')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 2)
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['name'], 'John Doe')

        # Verify client was closed
        mock_client.close.assert_called_once()

    @patch('app.MongoClient')
    def test_get_roster_no_connection(self, mock_mongo_client):
        """Test roster endpoint when database connection fails"""
        # Mock connection failure
        mock_mongo_client.side_effect = Exception('Connection failed')

        response = self.client.get('/api/roster')
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

    def test_404_endpoint(self):
        """Test 404 error handling"""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()

