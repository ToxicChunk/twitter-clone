from search_tweets import search_tweets
from search_users import search_users
from list_top_tweets import list_top_tweets
from list_top_users import list_top_users
from compose_tweet import compose_tweet, list_my_tweets
from utils import get_database
import uuid
from datetime import datetime

def main():
    port = int(input("Enter MongoDB port number: "))
    db = get_database(port)
    tweets_collection = db['tweets']

    
    while True:
        print("\nMain Menu:")
        print("1. Search for tweets")
        print("2. Search for users")
        print("3. List top tweets")
        print("4. List top users")
        print("5. Compose a tweet")
        print("6. Exit")
        print("7. Bonus! Look at your own wonderful tweets of wisdom.")

        choice = input("Enter your choice: ")

        if choice == "1":
            keywords = input("Enter keywords (space-separated): ")
            search_tweets(keywords, db)
        elif choice == "2":
            keyword = input("Enter user search keyword: ")
            results = search_users(keyword, db)
        elif choice == "3":
            list_top_tweets(db)
        elif choice == "4":
            n = int(input("Enter the number of top users to list: "))
            list_top_users(tweets_collection, n)

            #results = list_top_users(n, db)
            #for user in results:
                #print(user)
        elif choice == "5":
            content = input("Enter tweet content: ")
            compose_tweet(tweets_collection, content)

        elif choice == "6":
            print("Exiting program.")
            break
        elif choice == "7":
            list_my_tweets(port)
        else:
            print("Invalid choice. Try again.")




if __name__ == "__main__":
    main()