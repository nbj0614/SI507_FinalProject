import requests
from re import search
import random
import json
import webbrowser
import os
from final_tree import insertTree, traversalTree

# cache for bestsellers
cache_bestsellers = {}


# load API_KEY from text file
def get_api_key(file):
    keyfile = open(file, "r")
    key = keyfile.readline()
    keyfile.close()
    return key

# Get API_KEY
GOOGLE_API_KEY = get_api_key("google_api_key.txt")
BOOKS_API_KEY = get_api_key("books_api_key.txt")
# print(GOOGLE_API_KEY, BOOKS_API_KEY)


def open_cache():
    '''
    opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    try:
        cache_file = open("cache.json", 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}

    ## convert json format to Books object
    if (len(cache_dict) > 0):
        for key, value in cache_dict.items():
            booklist = []
            for book in value:
                booklist.append(Book(book))
            cache_bestsellers[key] = booklist

        # print_bestseller(cache_bestsellers)

def save_cache():
    ''' 
    saves the current state of the cache to disk.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    # convert Books object to json format
    dumped_json_cache = {}
    for key, value in cache_bestsellers.items():
        booklist = []
        for book in value:
            # print(json.dumps(b.__dict__))
            booklist.append(book.__dict__)
        dumped_json_cache[key] = booklist

    dumped_json_cache = json.dumps(dumped_json_cache)
    fw = open("cache.json","w")
    fw.write(dumped_json_cache)
    fw.close() 


TREE_MYLIBRARY = (None, None, None)   # (Book, Left, Right)


def showMyLibrary(tree):
    allbooks = []
    traversalTree(tree, allbooks)
    libraryHTML = ""
    for book in allbooks:
        url = f"https://www.googleapis.com/books/v1/volumes?q={book.primary_isbn13}&key={GOOGLE_API_KEY}"
        additional_info_from_GoogleBooksAPI = get_json(url)["items"][0]["volumeInfo"]
        additional_info = {}
        if "publisher" in additional_info_from_GoogleBooksAPI:
            additional_info["publisher"] = additional_info_from_GoogleBooksAPI["publisher"]
        if "publishedDate" in additional_info_from_GoogleBooksAPI:
            additional_info["publishedDate"] = additional_info_from_GoogleBooksAPI["publishedDate"]
        if "pageCount" in additional_info_from_GoogleBooksAPI:
            additional_info["pageCount"] = additional_info_from_GoogleBooksAPI["pageCount"]
        if "averageRating" in additional_info_from_GoogleBooksAPI:
            additional_info["averageRating"] = additional_info_from_GoogleBooksAPI["averageRating"]
        if "ratingsCount" in additional_info_from_GoogleBooksAPI:
            additional_info["ratingsCount"] = additional_info_from_GoogleBooksAPI["ratingsCount"]
        if "imageLinks" in additional_info_from_GoogleBooksAPI:
            if "thumbnail" in additional_info_from_GoogleBooksAPI["imageLinks"]:
                additional_info["thumbnail"] = additional_info_from_GoogleBooksAPI["imageLinks"]["thumbnail"]
        if "previewLink" in additional_info_from_GoogleBooksAPI:
            additional_info["previewLink"] = additional_info_from_GoogleBooksAPI["previewLink"]
        book.additional_info = additional_info
        # print(book.additional_info)
        # print(json.dumps(book.__dict__))

        libraryHTML += f'<tr><td width="200" align="center">'
        if ("thumbnail" in book.additional_info):
            libraryHTML += f'<img src="{book.additional_info["thumbnail"]}"><br>'
        if ("previewLink" in book.additional_info):
            libraryHTML += f'<a href="{book.additional_info["previewLink"]}" target="_blank">Preview</a>'
        libraryHTML += f'''
                    </td><td><h3>{book.title} <small> by {book.author}</small></h3>
                    {book.description} <br><br>
                    '''
        if ("publisher" in book.additional_info):
            libraryHTML += f'Publisher: {book.additional_info["publisher"]}<br>'
        if ("publishedDate" in book.additional_info):
            libraryHTML += f'Published Date: {book.additional_info["publishedDate"]}<br>'
        if ("pageCount" in book.additional_info):
            libraryHTML += f'Page Count: {book.additional_info["pageCount"]}<br>'
        if ("averageRating" in book.additional_info):
            libraryHTML += f'Average Rating: {book.additional_info["averageRating"]}' 
            if ("ratingsCount" in book.additional_info):
                libraryHTML += f' ({book.additional_info["ratingsCount"]} ratings)'
            libraryHTML += '<br>'

        libraryHTML += f'ISBN: {book.primary_isbn13}<br></td></tr><tr><td colspan="2"><hr></td></tr>'


    # to open/create a new html file in the write mode
    f = open('mylibrary.html', 'w')
    
    # the html code which will saved in the file mylibrary.html
    html_template = f"""
    <html>
    <head></head>
    <body>
        <center>
        <h2>My Library</h2>
        <table width="80%">
        {libraryHTML}
        </table>
        </center>        
    </body>
    </html>
    """
    # writing the code into the file
    f.write(html_template)
    
    # close the file
    f.close()
    
    # 1st method how to open html files in chrome using
    filename = 'file:///'+os.getcwd()+'/' + 'mylibrary.html'
    webbrowser.open_new_tab(filename)



# get json from url
def get_json(url):
    return requests.get(url).json()


def main():


    ### Get all category list from BOOKS API
    # categorylist = get_json('https://api.nytimes.com/svc/books/v3/lists/names?api-key='+BOOKS_API_KEY)
    # for c in categorylist["results"]:
    #     print(c["display_name"], ',', c["list_name_encoded"])

    ### Count available data from BOOKS API
    # categorylist = get_json('https://api.nytimes.com/svc/books/v3/lists/names?api-key='+BOOKS_API_KEY)
    # for c in categorylist["results"]:
    #     category_encoded = c["list_name_encoded"]
    #     r = get_json(f"https://api.nytimes.com/svc/books/v3/lists.json?list={category_encoded}&api-key={BOOKS_API_KEY}")
    #     print(category_encoded, r["num_results"])

    print("\n**********************************************") 
    print("* Welcome to the Book Recommendation System! *")
    print("**********************************************\n") 
 
    # load cache
    open_cache()

    # Test tree
    # TREE_MYLIBRARY = (None, None, None)   # (Book, Left, Right)
    # for book in cache_bestsellers["Fiction"]:
    #     TREE_MYLIBRARY = insertTree(TREE_MYLIBRARY, book)

    # # printTree(TREE_MYLIBRARY)
    # print(TREE_MYLIBRARY)

    # allbooks = []
    # traversalTree(TREE_MYLIBRARY, allbooks)
    

    while(True):
        PlaySearch()




# Book class
class Book:
    def __init__(self, book_details):
        self.title = book_details["title"]
        self.description = book_details["description"]
        self.author = book_details["author"]
        self.primary_isbn13 = book_details["primary_isbn13"]
        self.additional_info = None

    def __str__(self):
        return f"{self.title} by {self.author} [ISBN: {self.primary_isbn13}]"

   

# get bestseller list of specific category from Books API
def get_bestseller_by_category_from_BooksAPI(category_encoded):
    url = f"https://api.nytimes.com/svc/books/v3/lists.json?list={category_encoded}&api-key={BOOKS_API_KEY}"
    results = get_json(url)["results"]
    booklist = []
    for r in results:
        booklist.append(Book(r["book_details"][0]))

    return booklist


# print bestseller list
def print_bestseller(list):
    for key, value in list.items():
        print(f"\n====={key}=====")
        for b in value:
            # print(b)
            print(json.dumps(b.__dict__))



def PlaySearch():
    global TREE_MYLIBRARY

    ### -- Category --
    categories = ["Fiction", "Nonfiction", "Business", "Games and Activities", "Humor", "Love and Relationships", "Science", "Sports and Fitness", "Travel"]
    categories_encoded = ["combined-print-fiction", "combined-print-nonfiction", "business-books", "games-and-activities", "humor", "relationships", "science", "sports", "travel"]
    # print(len(categories))
    while(True):
        for i in range(len(categories)):
            print(str(i+1) + ". " + categories[i])

        x = input("Please type a category number: ")
        try:
            x = int(x)
            if (x >= 1 and x <= len(categories)):
                user_category = x-1
                break
            else:
                print("Please type a valid number!")
        except ValueError:
            print("Please type a valid number!")

    # print(user_category)

    

    # Bestsellers data from NYT BOOKS API (use cache if data exists in cache)
    if (categories[user_category] in cache_bestsellers):
        print(f"--> {categories[user_category]} list exists in cache!")
    else:
        print(f"--> {categories[user_category]} list doesn't exist in cache! Fetch {categories[user_category]} list from BOOKS API")
        cache_bestsellers[categories[user_category]] = get_bestseller_by_category_from_BooksAPI(categories_encoded[user_category])

    # print_bestseller(cache_bestsellers)
    


    # Author
    x = input("Please type an author's name (enter to skip): ")
    user_author = x

    # Topic (keyword)
    x = input("Please type a topic (enter to skip): ")
    user_topic = x

    recommendation = []
    # search from bestseller list
    for b in cache_bestsellers[categories[user_category]]:
        if user_author != "" and search(user_author.lower(), str(b.author).lower()):
            recommendation.append(b)
        
        if user_topic != "" and (search(user_topic.lower(), str(b.title).lower()) or search(user_topic.lower(), str(b.description).lower())):
            recommendation.append(b)

    # show search result
    # recommend random book in the category if there is no matching result
    if (len(recommendation) > 0):
        print("\n** Here is the search result:")
    else:
        print("\nThere is no matching result, but you might like the following book:")
        recommendation.append(random.choice(cache_bestsellers[categories[user_category]]))

    for b in recommendation:
        print(" - " + b.__str__())
        ## add to mylibrary
        TREE_MYLIBRARY = insertTree(TREE_MYLIBRARY, b)
    print("\nThe result was added to the My Library.\n")
    # printTree(TREE_MYLIBRARY)

    while(True):
        x = input("Please enter to new search, 's' to show my library, 'x' to quit): ")
        if (x == ""):
            break
        elif (x == "s"):
            ## show books in my library
            showMyLibrary(TREE_MYLIBRARY)
        elif (x == "x"):
            print("\nThank you for using the Book Recommendation System!\n")
            
            ## save cache to file
            save_cache()
            
            ## terminate 
            quit()


    

##NYT BOOKS
#list names: https://api.nytimes.com/svc/books/v3/lists/names?api-key=zAThsXGVeIIG1aEeV2A0NGUuKcJ5ayzo



##GOOGLE BOOKS
#Google books metadata
#https://support.google.com/books/partner/answer/3237055?hl=en
#https://bisg.org/page/bisacedition
# https://www.googleapis.com/books/v1/volumes?q=business+subject:juvenile+fiction




if __name__ == '__main__':
    main()
