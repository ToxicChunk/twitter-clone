def list_top_users(tweets_collection, n):
    """
    Lists the top n users based on followersCount.
    """
    try:
        #inspecting sample data to verify structure
        #print("Inspecting sample documents...")
        sample_docs = list(tweets_collection.find({}, {"user": 1}).limit(5))
        #for doc in sample_docs:
        #    print(doc)
        
        #MongoDB aggregation pipeline
        pipeline = [
            {"$group": {
                "_id": "$user.username",  #Group by username
                "displayname": {"$first": "$user.displayname"},  #take first display name
                "followersCount": {"$max": "$user.followersCount"}  #Maximum followers count
            }},
            {"$sort": {"followersCount": -1}},  #Sort by followersCount descending
            {"$limit": n}  #Limit results to 'n'
        ]
        
        #print("Executing aggregation pipeline...")
        results = list(tweets_collection.aggregate(pipeline))
        
        if not results:
            print("No users found. Ensure the database contains user data.")
            return

        print(f"Top {n} Users:")
        for idx, user in enumerate(results, start=1):
            print(f"{idx}. Username: {user['_id']}, Display Name: {user['displayname']}, Followers: {user['followersCount']}")

        while True:
            #Ask user to choose from the list for more information
            chosen_user_index = input(f"Choose a user by number (1-{n}) to see more information, or type 'exit' to quit: ")

            #Exit condition
            if chosen_user_index.lower() == 'exit':
                print("Exiting. Goodbye!")
                break

            #Validate input
            if not chosen_user_index.isdigit():
                print("Invalid input. Please enter a valid number or type 'exit' to quit.")
                continue

            chosen_user_index = int(chosen_user_index) - 1

            if chosen_user_index < 0 or chosen_user_index >= len(results):
                print("Invalid selection. Please choose a valid user index.")
                continue

            chosen_username = results[chosen_user_index]["_id"]

            #Query for additional details about the selected user
            user_details = tweets_collection.find_one({"user.username": chosen_username}, {"user": 1, "_id": 0})

            if user_details and "user" in user_details:
                user = user_details["user"]
                print("\nDetailed Information about the Selected User:")
                print(f"Username: {user.get('username')}")
                print(f"Display Name: {user.get('displayname')}")
                print(f"Description: {user.get('description')}")
                print(f"Location: {user.get('location')}")
                print(f"Followers: {user.get('followersCount')}")
                print(f"Friends: {user.get('friendsCount')}")
                print(f"Statuses: {user.get('statusesCount')}")
                print(f"Account Created: {user.get('created')}")
            else:
                print("No detailed information available for the selected user.")
            
    except Exception as e:
        print(f"Error listing top users: {e}")