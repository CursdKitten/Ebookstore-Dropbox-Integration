# Ebookstore/DropBox Integration

## Description

This application is a simple ebookstore that takes in the ID, author, title and stock levels of a book and pushes this information to a MySQL database.

Thereafter, changes can be made to the stock levels, deletions and insertions made, book searches done and the option to backup the database to the cloud displayed (Dropbox).

The user is prompted to enter the access token that will act as the link to the Dropbox API. A check is done to ensure that the key entered has the correct number of characters.

Once the user has successfully logged in, they are presented with a menu with the following options:

* If the user enters 1, they will be propmted to enter the book's ID, title, author name and quantity in stock. This will then be pused to the MySQL database.

* If the user enters 2, they will be prompted to enter the ID of the book they wish to update after which a "sub-menu" of sorts asking which fields they would like to update is 
displayed. These updates will then be comitted to the database

* If the user enters 3, they will be prompted to enter the ID of the book they wish to delete. Thereafter the user is asked for confirmation before deleting the book from the database.

* If the user enters 4, they are propmpted to choose whether to search the database by title/ID/author. They then input the corresponding book ID/title/author and the relevant record/s is displayed.

* If the user enters 5, the database is pushed to the cloud, more specifically a directory with the date and time of upload in the Dropbox folder.

* Finally, the user can enter 0 to quit the application.


### Dependencies

Important: Please consult the configuration appendix to ensure the DB is updated to your Dropbox.

You will need to create a Dropbox account to use the application.

You will also need to install the dropbox SDK and depending on your OS, you might need to install sqlite.

This application makes use of the following to be imported in your text editor:
* sqlite3
* dropbox
* datetime

The program automatically creates the database so there is no need to download the DB file.

### Executing program

The user will be prompted to enter the access token to establish a connection with the Dropbox API.

Once the user has entered the access token, the following menu is displayed:
* 1 - Add a book
* 2 - Update a book
  - Enter corresponding field to be updated:
  -  1 - Update book title
  -  2 - Update book author
  -  3 - Update book quantity
* 3 - Delete a book
* 4 - Search for a book
* 5 - Backup the databse to the cloud
* 0 - Exit

## Authors

* Kirsten Forrester

## Contributors names and contact info

Tel: 071 872 0132

Email: forrestermkirsten@gmail.com

