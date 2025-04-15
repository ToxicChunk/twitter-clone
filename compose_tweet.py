import uuid
from datetime import datetime

def compose_tweet(tweets_collection, content):
    try:
        new_tweet = {
            "id": str(uuid.uuid4()),  # Generate a unique ID
            "date": datetime.now().isoformat(),
            "content": content,
            "user": {"username": "291user"}
        }
        tweets_collection.insert_one(new_tweet)
        print("Your tweet has been posted!")
    except Exception as e:
        print(f"Error composing tweet: {e}")

def list_my_tweets(port):
    from pymongo import MongoClient
    
    client = MongoClient(f"mongodb://localhost:{port}")
    db = client['291db']
    collection = db['tweets']
    
    try:
        my_tweets = collection.find({"user.username": "291user"})
        print("Your Tweets:")
        for tweet in my_tweets:
            tweet_id = tweet.get("id", "N/A")  # Use "N/A" if id is missing
            date = tweet.get("date", "N/A")
            content = tweet.get("content", "No content available")
            print(f"ID: {tweet_id}, Date: {date}, Content: {content}")
    except Exception as e:
        print(f"Error retrieving your tweets: {e}")
    finally:
        client.close()

