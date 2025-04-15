from pymongo import *
from utils import *
import os
import re

def normalize_keyword(keyword:str): # removes all non-alphanumerics that are adjacent to each keyword
                                    # by finding the index of the first and last alphanumeric character
                                    # and isolating the substring between both indicies
    length = len(keyword)

    i = 0

    while i < length:
        if keyword[i].isalnum(): break
        else: i = i+1
    
    j = length - 1
    while j >= 0:
        if keyword[j].isalnum(): break
        else: j = j-1

    if i > j: return ""
    else: return keyword[i:j+1]


    





def find_tweets(content,db):
    # content is the string with all the keywords
    # db is the Mongoclient connection to the server

    db_database = db["291db"] # gettng actual database
    db_connection = db["tweets"] # getting tweets collection

    content = re.sub("[^0-9a-zA-Z']",",", content) # replace every non-alphanumeric with a comma (excluding apostrpohe)
    content_keyword_array = content.split(",") # split by comma

    while '' in content_keyword_array: content_keyword_array.remove('')

    i = 0
    for word in content_keyword_array:
        content_keyword_array[i] = normalize_keyword(word)
        i = i + 1


        

    i = 0
    for word in content_keyword_array: 
        content_keyword_array[i] = "[^a-zA-Z0-9\\s]*".join(list(content_keyword_array[i])) # for ignoring alphanumerics inside each potential keyword of
                                                                                        # the content field for each document when using regex
        i = i + 1 

    

    #length = len(content_keyword_array)
    query = { 
    "$and":[
        {"content": {"$regex": f"\\b[^a-zA-Z0-9\\s]*{keyword}[^a-zA-Z0-9\\s]*\\b", "$options": "i"}}  # this regex uses the boundary sequence to prevent catching keywords inside bigger words
                                                                                                      # and allows for non-alphanumerics that arent spaces to be adjacent to each word of each document
                                                                                                      # option i makes it case-insensitive
        for keyword in content_keyword_array # this and statement gets repeated for every keyword
    ]
}
    test = db_connection.find(query) # actually running the query - test is a list of documents in the form of dictionaries
    return test

def print_tweets(results:list): # prints every document
    i = 1
    for document in results:
        print(i , ". " , "Id: ", document["id"], " Date: ", document["date"], " User: ", (document["user"])["username"],"\nContent: ", document["content"],'\n')
        i = i+1

def clear_screen(): # clears the screen completely
    os.system("cls" if os.name == "nt" else "clear")


def search_tweets(content,db):
    results = list(find_tweets(content,db)) # find results of given keywords

    clear_screen() # clear the screen
    length_of_list = len(results) # get the length of list

    if length_of_list == 0:
        print("No results found.")
        return

    search_tweets_input:str = "" # input for selecting each tweet
    print_tweets(results)

    while (search_tweets_input != 'exit'):

        
        search_tweets_input = input("Select the index of the tweet you wish to examine (or type 'exit' to leave this menu): ")
        if search_tweets_input.isnumeric(): # if is an acutual number
            index = int(search_tweets_input) - 1 # index for array

            if index < 0 or index >= length_of_list: # if index is invalid
                print("Error: invalid index")
                clear_screen()
                print_tweets(results)

            else:
                desiredField = input("Enter all fields you wish to see (space separated, and type 'all' to see every field): ")
                desiredField = desiredField.lower().split(" ") # list of all desired fields
                if desiredField[0] == "all": print(results[index]) # prints all fields if user types 'all'

                else: 
                    for field in desiredField:
                        if field in results[index]: # if valid field
                            print(field + ": ", results[index][field])
                        else: print(field + ": invalid field") # if invalid, mark specified field as invalid

        elif search_tweets_input.lower() == "exit": # if not number, and exit then return
            clear_screen()
            return
        else:
            print("Invalid input") # else, must be invalid input, clear everything and show the results again.
            clear_screen()
            print_tweets(results)





if __name__ == "__main__":
    search_tweets("at wh", get_database(27012))
