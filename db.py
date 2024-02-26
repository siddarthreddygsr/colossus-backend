from pymongo import MongoClient

def check_mongodb_connection():
    try:
        print("hi")
        # Replace the URL with your MongoDB server URL (including the port)
        client = MongoClient("mongodb://165.232.152.128:27017/")
        # Access any collection or database to check the connection
        _ = client.list_database_names()
        print("Connected to MongoDB server successfully!")
        return True
    except Exception as e:
        print(f"Failed to connect to MongoDB server: {e}")
        return False

# Call the function to check the connection
check_mongodb_connection()

