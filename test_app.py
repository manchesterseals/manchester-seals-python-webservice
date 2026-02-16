"""
Unit tests for the Manchester Seals API
"""
import unittest
import json
import os
from dotenv import load_dotenv
from unittest.mock import patch, MagicMock
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

    @patch('app.roster_collection')
    def test_get_roster_success(self, mock_collection):
        """Test getting roster data successfully"""
        # Mock MongoDB response
        mock_collection.find.return_value = [
            {
                '_id': MagicMock(),
                'name': 'John Doe',
                'position': 'Manager'
            }
        ]

        response = self.client.get('/api/roster')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['count'], 1)

    @patch('app.roster_collection', None)
    def test_get_roster_no_connection(self):
        """Test roster endpoint when database connection fails"""
        response = self.client.get('/api/roster')
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_404_endpoint(self):
        """Test 404 error handling"""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])


if __name__ == '__main__':
    unittest.main()

