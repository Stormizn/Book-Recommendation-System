import mysql.connector

# database config
HOST = 'localhost'
USER = 'root'
PASSWORD = 'your_password'
DATABASE = 'book_recommendation_db'

current_user_id = 0 #0 = not logged in
current_username = "" 

def connect_database():
    connection = mysql.connector.connect(
        host = HOST,
        user = USER,
        password = PASSWORD,
        database = DATABASE
    )
    return connection

def get_int(prompt, low, high):
    """takes an int input from the user within a specified range."""
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            else:
                print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

def display_books(rows):
    """displays book list"""
    if len(rows) == 0:
        print("\nNo books found!")
        return
    print()
    print("-" * 60)
    print("ID  Title                    Author                Genre")
    print("-" * 60)
    for row in rows:
        print(str(row[0]).ljust(4), row[1].ljust(25), row[2].ljust(20), row[3])
    print("-" * 60)

def register_user(connection):
    """register new user"""
    cursor=connection.cursor()
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()

    if username=="" or password=="":
        print("Username and password cannot be empty!")
        cursor.close()
        return

    #check if username alr exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone() is not None:
        print("Username already exists! Please choose a different username.")
        cursor.close()
        return

    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password))
    connection.commit()
    cursor.close()
    print("User registered successfully! You can now log in.")

def login_user(connection):
    """loggs in existing user"""
    global current_user_id, current_username

    cursor=connection.cursor()
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    query="SELECT user_id, username FROM users WHERE username = %s AND password_hash = %s"
    cursor.execute(query, (username, password))
    row=cursor.fetchone()
    cursor.close()

    if row is None:
        print("Invalid username or password! Please try again.")
    else:
        current_user_id = row[0]
        current_username = row[1]
        print(f"Login successful! Welcome, {current_username}.")

def login_menu(connection):
    """login menu"""
    while True:
        print()
        print("=" * 40)
        print("   BOOK RECOMMENDATION SYSTEM")
        print("=" * 40)
        print("1. Register")
        print("2. Login")
        print("3. Back to Main Menu")
        choice = get_int("Enter your choice (1-3): ", 1, 3)

        if choice == 1:
            register_user(connection)
        elif choice == 2:
            login_user(connection)
            if current_user_id != 0:  # Successful login
                return
        else:
            print("Baii...")
            return False

def browse_books(connection):
    """browse all/chosen genre books"""
    cursor=connection.cursor()

    print("\n1. Show all books")
    print("2. Filter by genre")
    choice = get_int("Enter your choice: ", 1, 2)

    if choice ==1:
        cursor.execute("SELECT book_id, title, author, genre FROM books")
        rows = cursor.fetchall()
        display_books(rows)
    else:
        genre = input("Enter the genre to filter by: ").strip()
        cursor.execute("SELECT book_id, title, author, genre FROM books WHERE genre = %s", (genre,))
        rows = cursor.fetchall()
        display_books(rows)

    cursor.close()

def search_books(connection):
    """search books by title or author"""
    cursor=connection.cursor()

    print("\n1. Search by title")
    print("2. Search by author")
    choice = get_int("Enter your choice: ", 1, 2)

    keyword = input("Enter the search keyword: ").strip()
    pattern = "%" + keyword + "%"

    if choice == 1:
        cursor.execute("SELECT book_id, title, author, genre FROM books WHERE title LIKE %s", (pattern,))
    else:
        cursor.execute("SELECT book_id, title, author, genre FROM books WHERE author LIKE %s", (pattern,))

    rows = cursor.fetchall()
    display_books(rows)
    cursor.close()

def rate_book(connection):
    """rates a book"""
    cursor = connection.cursor()
    book_id = get_int("Enter the book ID to rate: ", 1, 200)

    cursor.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
    row = cursor.fetchone()

    if row is None:
        print("Book not found! Please check the book ID and try again.")
        cursor.close()
        return

    cursor.execute("SELECT rating_id FROM ratings WHERE user_id = %s AND book_id = %s", (current_user_id, book_id))
    if cursor.fetchone() is not None:
        print("You have already rated this book! You can only rate a book once.")
        cursor.close()
        return

    rating = get_int("Enter your rating (1-5): ", 1, 5)
    cursor.execute("INSERT INTO ratings (user_id, book_id, rating) VALUES (%s, %s, %s)", (current_user_id, book_id, rating))
    connection.commit()
    cursor.close()
    print(f"Thank you for rating '{row[0]}' with a score of {rating}!")

def reading_list_menu(connection):
    """manage the user's reading list"""
    cursor = connection.cursor()

    print("\n1. View my reading list")
    print("2. Add a book to my reading list")
    choice = get_int("Enter your choice: ", 1, 2)

    if choice == 1:
        query = """SELECT b.book_id, b.title, b.author, b.genre
                   FROM reading_lists rl
                   JOIN books b ON rl.book_id = b.book_id
                   WHERE rl.user_id = %s"""
        cursor.execute(query, (current_user_id,))
        rows = cursor.fetchall()
        display_books(rows)
    else:
        book_id = get_int("Enter the book ID to add to your reading list: ", 1, 200)

        cursor.execute("SELECT title FROM books WHERE book_id = %s", (book_id,))
        row = cursor.fetchone()

        if row is None:
            print("Book not found! Please check the book ID and try again.")
            cursor.close()
            return

        cursor.execute("SELECT list_id FROM reading_lists WHERE user_id = %s AND book_id = %s", (current_user_id, book_id))
        if cursor.fetchone() is not None:
            print("This book is already in your reading list!")
            cursor.close()
            return

        cursor.execute("INSERT INTO reading_lists (user_id, book_id) VALUES (%s, %s)", (current_user_id, book_id))
        connection.commit()
        print(f"'{row[0]}' has been added to your reading list!")

    cursor.close()

def get_recommendations(connection):
    """get book recommendations based on user's ratings"""
    cursor = connection.cursor()

    query="""SELECT b.genre, r.rating
            FROM ratings r
            JOIN books b ON r.book_id = b.book_id
            WHERE r.user_id = %s"""
    cursor.execute(query, (current_user_id,))
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("You haven't rated any books yet! Please rate some books to get recommendations!")
        cursor.close()
        return

    #calculate avg genre ratings
    genre_totals={}
    genre_counts={}

    for genre, rating in rows:
        genre_totals[genre] = genre_totals.get(genre, 0) + rating
        genre_counts[genre] = genre_counts.get(genre, 0) + 1

    preferred_genre = [] # genre rating >= 3.0
    for genre in genre_totals:
        avg_rating = genre_totals[genre] / genre_counts[genre]
        if avg_rating >= 4:
            preferred_genre.append(genre)

    if len(preferred_genre) == 0:
        print("You haven't rated any books with a high enough score to get recommendations! Please rate some books with a score of 4 or higher to get recommendations!")
        cursor.close()
        return

    #recommend books from preferred genres that the user hasn't rated yet
    placeholders = ', '.join(['%s'] * len(preferred_genre))
    query="""SELECT book_id, title, author, genre
            FROM books
            WHERE genre IN (""" + placeholders + """) 
            AND book_id NOT IN (
                SELECT book_id FROM ratings WHERE user_id = %s
            )
            ORDER BY genre"""
    params=preferred_genre + [current_user_id]
    cursor.execute(query, params)
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No recommendations found based on your ratings! Please rate more books to get better recommendations!")
    else:
        print("\nRecommended Books:")
        display_books(rows)

    cursor.close()

def main_menu(connection):
    """main menu"""
    while True:
        print()
        print("=" * 40)
        print("   MAIN MENU - " + current_username)
        print("=" * 40)
        print("1. Browse Books")
        print("2. Search Books")
        print("3. Rate a Book")
        print("4. My Reading List")
        print("5. Get Recommendations")
        print("6. Exit")
        choice = get_int("Enter your choice (1-6): ", 1, 6)

        if choice == 1:
            browse_books(connection)
        elif choice == 2:
            search_books(connection)
        elif choice == 3:
            rate_book(connection)
        elif choice == 4:
            reading_list_menu(connection)
        elif choice == 5:
            get_recommendations(connection)
        else:
            print("Exiting the program... Baii!")
            return

def main():
    """starts the program"""
    try:
        connection = connect_database()
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return
    if login_menu(connection) is False:
        connection.close()
        return

    main_menu(connection)
    connection.close()

main()