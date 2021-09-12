"""
A simple Python ebookstore that makes use of a MySQL database and the Dropbox API to back
the database up to the cloud.

The application allows the user to 
1. Add a book to the DB
2. Update a book (title/author/quantity)
3. Delete a book
4. Search by title/ID
5. Back up DB to the cloud

"""
import sqlite3
import dropbox
import datetime

# defining a function whereby the user can add a record to the DB
def add_book():

    # retrieving the field information from the user
    new_id = int(input("Please enter the id assigned to the book:\n"))
    new_title = input("Please enter the book title:\n")
    new_author = input("Please enter the author of the book:\n")
    new_qty = input("Please enter the number of books in stock: \n")

    # insert given information into our database
    cursor.execute("INSERT INTO books(id, title, author, qty) VALUES(?,?,?,?)", 
    (new_id, new_title, new_author, new_qty))
    
    # saving changes and confirming changes made
    db.commit()
    print("New book saved!")
    
# defining a function whereby the user can make changes to records in the DB
def update_book():

    while True:
        # we will use the id number of the book to find the position of the 
        # record that requires updating
        user_id = int(input("Please enter the id number of the book you wish to update" + 
        "or -1 to return to main menu :\n"))

        if user_id != -1:
            # presenting a "submenu" to ascertain which fields will be updated
            choice = input("What changes would you like to make?\n1 - Update book title\n" +
            "2 - Update book author\n3 - Update book quantity\n")

            if choice == "1":
                updated_title = input("Please enter updated title:\n")
                cursor.execute("UPDATE books SET title=? WHERE id=?", (updated_title, user_id))
                db.commit()
                print("Book title updated!")
                
            elif choice == "2":
                updated_author = input("Please enter updated author name:\n")
                cursor.execute("UPDATE books SET author=? WHERE id=?", (updated_author, user_id))
                db.commit()
                print("Book author updated!")
        
            elif choice == "3":
                updated_qty = int(input("Please enter updated quantity: \n"))
                cursor.execute("UPDATE books SET qty=? WHERE id=?", (updated_qty, user_id))
                db.commit()
                print("Book stock levels updated!")

        else:
            break

# defining a function that allows the user to delete records from the DB
def delete_book():

    while True:
        delete_id = int(input("Please enter the id number of the book you wish to delete: \n"))
        # ensure the user is certain about the deletion
        yes_no = input(f"Are you sure you want to delete book {delete_id}?\n").lower()
        if yes_no == "no":
            break
        else:
            cursor.execute("DELETE FROM books WHERE id=?", (delete_id,))
            db.commit()
            print(f"Book {delete_id} successfully deleted.")
            break

# defining a function that allows the user to search the database by title
# or book id
def search_book():

    # remmoving case sensitivity from user choice
    title_id = input("Search by book title or id? (title/id)\n").lower()

    if title_id == "title":
        search_title = input("Enter book title:\n").lower()
        # removing case sensitivity when we search the DB
        cursor.execute("SELECT * FROM books WHERE title=? COLLATE NOCASE", (search_title,))
        result = cursor.fetchall()
        print(result)
    
    elif title_id == "id":
        search_id = int(input("Enter book id:\n"))
        cursor.execute("SELECT * FROM books WHERE id=?", (search_id,))
        result = cursor.fetchall()
        print(result)

def upload_database(token, file_from, file_to):

    dbx = dropbox.Dropbox(token)

    with open(file_from, 'rb') as f:
        dbx.files_upload(f.read(), file_to)

# defining a function that outputs a menu and takes in user choices
def menu():

    print("Welcome to the ebookstore! Please enter the corresponding number of the action you would like to carry out:")
    option = int(input("1 - Enter book\n2 - Update book\n3 - Delete book\n4 - Search books \n5 - Backup database to the cloud" +
    "\n0 - Exit\n"))

    # keep showing the menu until user enters 0
    while True:
        if option == 1:
            add_book()
            option = int(input("1 - Enter book\n2 - Update book\n3 - Delete book\n4 - Search books" +
            "\n5 - Backup database to the cloud\n0 - Exit\n"))
        elif option == 2:
            update_book()
            option = int(input("1 - Enter book\n2 - Update book\n3 - Delete book\n4 - Search books" +
            "\n5 - Backup database to the cloud\n0 - Exit\n"))
        elif option == 3:
            delete_book()
            option = int(input("1 - Enter book\n2 - Update book\n3 - Delete book\n4 - Search books" +
            "\n5 - Backup database to the cloud\n0 - Exit\n"))
        elif option == 4:
            search_book()
            option = int(input("1 - Enter book\n2 - Update book\n3 - Delete book\n4 - Search books" +
            "\n5 - Backup database to the cloud\n0 - Exit\n"))
        elif option == 5:
            try:
                upload_database(token, file_from, file_to)
                print("Success! Your database has been synced to the cloud!")
                break
            except:
                print("Something went wrong :( Please try again.")
                break
        elif option == 0:
            break
        else:
            print("Invalid selection, please choose an option from the menu below.")
            option = int(input("1 - Enter book\n2 - Update book\n3 - Delete book\n4 - Search books" +
            "\n5 - Backup database to the cloud\n0 - Exit\n"))
            

"""
This is the portion whereby we implement all the functions above

"""

db = sqlite3.connect('ebookstore.db') # creating/connecting to our database

cursor = db.cursor()  # initialising a cursor object

# deleting the table so that we don't get an error when we run this program again
cursor.execute("DROP TABLE books")

# creating books table
cursor.execute("CREATE TABLE books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)")

# creating a list which we will use to populate our table
books = [(3001, "A Tale of Two Cities", "Charles Dickens", 30), 
(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
(3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
(3004, "The Lord of the Rings", "J.R.R. Tolkien", 37),
(3005, "Alice in Wonderland", "Lewis Caroll", 12)]

# populating our database
cursor.executemany("INSERT INTO books(id, title, author, qty) VALUES(?,?,?,?)", books)

# saving changes
db.commit()

# retrieving the date so that each update is stored in its
# corresponding time folder
today = datetime.datetime.now()
today_date = "/" + str(today.strftime("%d %b %Y %X")).replace(":", "-")

file_from = 'ebookstore.db' # the file we wish to upload
file_to = today_date + '/ebookstore.db'  # the path where we want to upload to

while True:
    token = input("Please enter the access token:\n").strip()

    if len(token) < 64:
        token = print("Access token too short, please try again.\n")
    elif len(token) > 64:
        token = print("Access token too long, please try again.\n")
    else:
        break

# creating a link to our Dropbox app via access token
dbx = dropbox.Dropbox(token)

# calling upon the menu function
menu()

# displaying info from the database showcasing the changes we made
cursor.execute("SELECT * FROM books")
new_database = cursor.fetchall()
print(new_database)