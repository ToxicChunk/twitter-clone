from pymongo import MongoClient

def test_connection():
    try:
        # Connect to the MongoDB server
        client = MongoClient('localhost', 27017)  # Default port
        db = client['testdb']  # Use a test database
        print("Connected to MongoDB!")
        print("Databases:", client.list_database_names())
    except Exception as e:
        print("Error connecting to MongoDB:", e)

if __name__ == "__main__":
    test_connection()