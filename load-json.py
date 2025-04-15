from pymongo import *
import pymongo
import string
import json


def main():
    json_name:string = input("Type the name of your JSON: ") # recieve input for json name
    database_port = input("Enter the port of your database: ") # recieve input for port
    if not database_port.isdigit(): # if port not int, close program
        print("Invalid Port.\n")
        return -1
    
    database_port = int(database_port) # convert port to int
    
    client_connection = MongoClient('localhost', database_port)

    try: 
        print("Verifying port integrity...") # checking if server if open
        client_connection.server_info()
    except: 
        print("Connection Error: check your port.")
        return -1

    client_db = client_connection["291db"] # connection to 291db

    if "tweets" in client_db.list_collection_names(): # drop tweets collection if already exists
        client_db.drop_collection("tweets")


    client_tweet_collection = client_db["tweets"] # actual tweets collection




    json_connection = open(json_name) # opening the json

    if json_connection.closed: # checking if opening succeeds
        print("Error: could not open specified JSON file.\n")
        return -2
    
    json_data:list = [] # holds chunks of data as dictionaries
    
    for line in json_connection: # for every document in json_connection

        if len(json_data) >= 1000: # inserting in packets of 1000, if this limit is reached, insert the documents and flush the list
            client_tweet_collection.insert_many(json_data)
            json_data.clear()


        json_data.append(json.loads(line)) 

    client_tweet_collection.insert_many(json_data) # to insert the final remaining documents
    json_data.clear() # clearing data


    client_connection.close()
    json_connection.close()
    print("Documents have been loaded.")
    return 0
    
    

if __name__ == "__main__": 
    main()