from pymongo import MongoClient

def get_database(port):
    """
    Connect to the MongoDB server and return the database object.

    Args:
        port (int): The MongoDB server port.

    Returns:
        db: The MongoDB database object for the project.
    """
    try:
        client = MongoClient(f"mongodb://localhost:{port}/")
        db = client['291db']  
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None