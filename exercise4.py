import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create three tables: Books, Users, and Reservations
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

# Function to add a new book to the database
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    cursor.execute('''
        INSERT INTO Books (BookID, Title, Author, ISBN, Status)
        VALUES (?, ?, ?, ?, ?)
    ''', (book_id, title, author, isbn, status))

    conn.commit()
    print("Book added successfully.")

# Function to find book details by BookID
def find_book_by_id():
    book_id = input("Enter BookID: ")

    cursor.execute('''
        SELECT Books.*, Users.Name AS UserName, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))

    book_details = cursor.fetchone()

    if book_details:
        print("BookID:", book_details[0])
        print("Title:", book_details[1])
        print("Author:", book_details[2])
        print("ISBN:", book_details[3])
        print("Status:", book_details[4])
        if book_details[5]:
            print("Reserved by:", book_details[5])
            print("User Email:", book_details[6])
        else:
            print("Not reserved.")
    else:
        print("Book not found.")

# Function to find book reservation status
def find_reservation_status():
    input_text = input("Enter BookID, Title, UserID, or ReservationID: ")

    if input_text.startswith("LB"):
        # BookID
        cursor.execute('''
            SELECT Books.BookID, Title, Status, Users.Name AS UserName, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Books.BookID = ?
        ''', (input_text,))
    elif input_text.startswith("LU"):
        # UserID
        cursor.execute('''
            SELECT Books.BookID, Title, Status, Users.Name AS UserName, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Users.UserID = ?
        ''', (input_text,))
    elif input_text.startswith("LR"):
        # ReservationID
        cursor.execute('''
            SELECT Books.BookID, Title, Status, Users.Name AS UserName, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Reservations.ReservationID = ?
        ''', (input_text,))
    else:
        # Title
        cursor.execute('''
            SELECT Books.BookID, Title, Status, Users.Name AS UserName, Users.Email
            FROM Books
            LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
            LEFT JOIN Users ON Reservations.UserID = Users.UserID
            WHERE Title = ?
        ''', (input_text,))

    results = cursor.fetchall()

    if results:
        for row in results:
            print("BookID:", row[0])
            print("Title:", row[1])
            print("Status:", row[2])
            if row[3]:
                print("Reserved by:", row[3])
                print("User Email:", row[4])
            else:
                print("Not reserved.")
    else:
        print("No matching records found.")

# Function to retrieve all books
def find_all_books():
    cursor.execute('''
        SELECT Books.BookID, Title, Status, Users.Name AS UserName, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')

    results = cursor.fetchall()

    if results:
        for row in results:
            print("BookID:", row[0])
            print("Title:", row[1])
            print("Status:", row[2])
            if row[3]:
                print("Reserved by:", row[3])
                print("User Email:", row[4])
            else:
                print("Not reserved.")
    else:
        print("No books found in the database.")

# Function to update book details by BookID
def update_book_details():
    book_id = input("Enter BookID to update: ")
    new_status = input("Enter new Status: ")

    cursor.execute('''
        UPDATE Books
        SET Status = ?
        WHERE BookID = ?
    ''', (new_status, book_id))

    conn.commit()
    print("Book details updated successfully.")

# Function to delete a book by BookID
def delete_book():
    book_id = input("Enter BookID to delete: ")

    cursor.execute('''
        DELETE FROM Books WHERE BookID = ?
    ''', (book_id,))

    cursor.execute('''
        DELETE FROM Reservations WHERE BookID = ?
    ''', (book_id,))

    conn.commit()
    print("Book deleted successfully.")

# Main menu
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find book details by BookID")
    print("3. Find book reservation status")
    print("4. Find all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_by_id()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        update_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        conn.close()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
