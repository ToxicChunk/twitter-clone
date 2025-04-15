from pymongo import MongoClient

def list_top_tweets(db):
    """
    Lists the top n tweets based on a user-selected field (retweetCount, likeCount, quoteCount).
    Displays id, date, content, and username for the top tweets in a formatted way.
    Allows the user to select a tweet to view all fields.

    Args:
        db: MongoDB database object.

    Returns:
        None
    """
    def display_full_info(data, indent=0):
        """Recursively display a dictionary or list in a readable format."""
        for key, value in data.items():
            if isinstance(value, dict):  #Handle nested dictionaries
                print(" " * indent + f"{key.capitalize()}:")
                display_full_info(value, indent + 4)  #Increase indentation
            elif isinstance(value, list):  #Handle lists
                print(" " * indent + f"{key.capitalize()}:")
                for item in value:
                    if isinstance(item, dict):  #If list contains dictionaries
                        display_full_info(item, indent + 4)
                    else:
                        print(" " * (indent + 4) + f"- {item}")
            else:  # Handle scalar values
                print(" " * indent + f"{key.capitalize()}: {value}")

    print("\nList Top Tweets by Engagement Metrics")
    print("1. Retweets (retweetCount)")
    print("2. Likes (likeCount)")
    print("3. Quotes (quoteCount)")

    field_map = {1: "retweetCount", 2: "likeCount", 3: "quoteCount"}
    field = None

    while field is None:
        try:
            choice = int(input("Enter your choice (1-3): "))
            field = field_map.get(choice)
            if field is None:
                print("Invalid choice. Please select a valid option.")
        except ValueError:
            print("Invalid input. Please enter a number (1-3).")

    n = 0
    while n <= 0:
        try:
            n = int(input("Enter the number of top tweets to display: "))
            if n <= 0:
                print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    # Fetch top tweets from the database
    tweets = db["tweets"].find(
        {}, 
        {"_id": 0, "id": 1, "date": 1, "content": 1, "user.username": 1, field: 1}
    ).sort(field, -1).limit(n)

    tweet_list = list(tweets)
    if not tweet_list:
        print("No tweets found.")
        return

    # Display the top tweets
    print(f"\nTop {n} Tweets by {field.capitalize()}:")
    print("-" * 50)
    for idx, tweet in enumerate(tweet_list):
        # Safeguard for missing fields
        tweet_id = tweet.get('id', 'N/A')
        tweet_date = tweet.get('date', 'N/A')
        tweet_content = tweet.get('content', 'N/A')
        tweet_username = tweet.get('user', {}).get('username', 'N/A')

        print(f"{idx + 1}.")
        print(f"   ID: {tweet_id}")
        print(f"   Date: {tweet_date}")
        print(f"   Content: {tweet_content}")  
        print(f"   Username: {tweet_username}")
        print("-" * 50)

    # Allow the user to view detailed information about a specific tweet
    while True:
        try:
            selected_index = int(input("\nEnter the number of the tweet to view full information (0 to exit): ")) - 1
            if selected_index == -1:  # Exit condition
                print("Exiting.")
                break
            elif 0 <= selected_index < len(tweet_list):
                tweet_id = tweet_list[selected_index]["id"]
                full_info = db["tweets"].find_one({"id": tweet_id})
                if full_info:
                    print("\nFull Information:")
                    display_full_info(full_info)  # Use the recursive display function
                else:
                    print("Details for this tweet are unavailable.")
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
