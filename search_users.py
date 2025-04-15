from pymongo import MongoClient

def search_users(keyword, db):
    """
    Searches for users whose displayname or location contains the keyword.
    Lists username, displayname, and location without duplicates.
    Allows selecting a user to display full information in a formatted way.

    Args:
        keyword (str): The search keyword.
        db: MongoDB database object.

    Returns:
        None
    """
    # MongoDB query to search for users
    query = {
        "$or": [
            {"user.displayname": {"$regex": keyword, "$options": "i"}},  # Search in displayname
            {"user.location": {"$regex": keyword, "$options": "i"}}     # Search in location
        ]
    }

    # Use aggregation to ensure unique results
    users = db["tweets"].aggregate([
        {"$match": query},  # Match the query
        {"$group": {        # Group by username to avoid duplicates
            "_id": "$user.username",
            "displayname": {"$first": "$user.displayname"},
            "location": {"$first": "$user.location"}
        }}
    ])

    # Display the results
    user_list = list(users)
    if not user_list:
        print("No users found.")
        return

    print("\nUsers Found:")
    for idx, user in enumerate(user_list):
        print(f"{idx + 1}. Username: {user['_id']}, Displayname: {user['displayname']}, Location: {user['location']}")

    # Allow selecting a user to display full information
    while True:
        try:
            selected_index = int(input("\nEnter the number of the user to view full information (0 to exit): ")) - 1
            if selected_index == -1:  # Exit condition
                print("Exiting.")
                break
            elif 0 <= selected_index < len(user_list):
                selected_user = user_list[selected_index]["_id"]
                full_info = db["tweets"].find_one({"user.username": selected_user}, {"user": 1})
                if full_info and "user" in full_info:
                    user_info = full_info["user"]
                    print("\nFull Information:")
                    print(f"Username: {user_info.get('username', 'N/A')}")
                    print(f"Displayname: {user_info.get('displayname', 'N/A')}")
                    print(f"User ID: {user_info.get('id', 'N/A')}")
                    print(f"Description: {user_info.get('description', 'N/A')}")
                    print(f"Location: {user_info.get('location', 'N/A')}")
                    print(f"Followers Count: {user_info.get('followersCount', 'N/A')}")
                    print(f"Friends Count: {user_info.get('friendsCount', 'N/A')}")
                    print(f"Statuses Count: {user_info.get('statusesCount', 'N/A')}")
                    print(f"Favourites Count: {user_info.get('favouritesCount', 'N/A')}")
                    print(f"Profile Image URL: {user_info.get('profileImageUrl', 'N/A')}")
                    print(f"Profile Banner URL: {user_info.get('profileBannerUrl', 'N/A')}")
                    print(f"Verified: {user_info.get('verified', 'N/A')}")
                    print(f"Protected: {user_info.get('protected', 'N/A')}")
                    print(f"Created Date: {user_info.get('created', 'N/A')}")
                else:
                    print("No detailed information available for this user.")
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
