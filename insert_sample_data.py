#!/usr/bin/env python3
"""
Insert sample roster data into Manchester Seals MongoDB
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('DB_NAME', 'manchester_seals')

# Sample roster data
SAMPLE_DATA = [
    {
        "name": "John Doe",
        "position": "Manager",
        "department": "Operations",
        "email": "john.doe@example.com",
        "salary": 85000,
        "hire_date": "2020-01-15"
    },
    {
        "name": "Jane Smith",
        "position": "Senior Developer",
        "department": "Engineering",
        "email": "jane.smith@example.com",
        "salary": 120000,
        "hire_date": "2019-03-20"
    },
    {
        "name": "Bob Johnson",
        "position": "Data Analyst",
        "department": "Analytics",
        "email": "bob.johnson@example.com",
        "salary": 95000,
        "hire_date": "2021-06-10"
    },
    {
        "name": "Alice Brown",
        "position": "Product Manager",
        "department": "Product",
        "email": "alice.brown@example.com",
        "salary": 110000,
        "hire_date": "2020-09-01"
    },
    {
        "name": "Charlie Davis",
        "position": "UI/UX Designer",
        "department": "Design",
        "email": "charlie.davis@example.com",
        "salary": 90000,
        "hire_date": "2021-02-14"
    },
    {
        "name": "Eva Martinez",
        "position": "Backend Developer",
        "department": "Engineering",
        "email": "eva.martinez@example.com",
        "salary": 115000,
        "hire_date": "2020-05-18"
    },
    {
        "name": "Frank Wilson",
        "position": "DevOps Engineer",
        "department": "Infrastructure",
        "email": "frank.wilson@example.com",
        "salary": 125000,
        "hire_date": "2019-11-05"
    },
    {
        "name": "Grace Lee",
        "position": "QA Engineer",
        "department": "Quality Assurance",
        "email": "grace.lee@example.com",
        "salary": 88000,
        "hire_date": "2021-08-22"
    },
    {
        "name": "Henry Martinez",
        "position": "Tech Lead",
        "department": "Engineering",
        "email": "henry.martinez@example.com",
        "salary": 135000,
        "hire_date": "2018-06-01"
    },
    {
        "name": "Iris Chen",
        "position": "Security Engineer",
        "department": "Infrastructure",
        "email": "iris.chen@example.com",
        "salary": 130000,
        "hire_date": "2020-02-10"
    }
]


def insert_sample_data():
    """Insert sample roster data into MongoDB"""

    print("=" * 60)
    print("Manchester Seals - Insert Sample Roster Data")
    print("=" * 60)
    print(f"\nMongoDB URI: {MONGO_URI}")
    print(f"Database: {DB_NAME}")
    print(f"Collection: roster")

    try:
        # Connect to MongoDB
        print("\nConnecting to MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)

        # Test connection
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully")

        # Get database and collection
        db = client[DB_NAME]
        roster = db['roster']

        # Check if data already exists
        existing_count = roster.count_documents({})

        if existing_count > 0:
            print(f"\n⚠️  Collection already has {existing_count} documents")
            response = input("Do you want to add more data? (yes/no): ").strip().lower()
            if response != 'yes':
                print("✅ No data added")
                client.close()
                return

        # Insert the sample data
        print(f"\nInserting {len(SAMPLE_DATA)} roster records...")
        result = roster.insert_many(SAMPLE_DATA)

        print(f"✅ Successfully inserted {len(result.inserted_ids)} records")

        # Verify the insertion
        total_count = roster.count_documents({})
        print(f"\n📊 Total records in roster collection: {total_count}")

        # Show sample of inserted data
        print("\nSample records:")
        for i, item in enumerate(list(roster.find({}))[:5], 1):
            print(f"  {i}. {item['name']} - {item['position']} ({item['department']})")

        if total_count > 5:
            print(f"  ... and {total_count - 5} more")

        print("\n" + "=" * 60)
        print("Data insertion complete! ✅")
        print("=" * 60)

        # Close connection
        client.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == '__main__':
    insert_sample_data()

