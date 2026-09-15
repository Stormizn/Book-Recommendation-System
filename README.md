# Book Recommendation System

A command-line book recommendation system built with Python and MySQL as a **Class 12 CBSE Computer Science project**. Users can browse, search, and receive book recommendations based on their genre preferences and reading history.

> **Note:** This project is currently under development. Some features described below are planned and not yet implemented.

---

## Features

### Implemented

- User registration and login system
- Browse books by genre
- Search books by title or author
- Add books to a personal reading list
- Rate books on a scale of 1-5
- Rule-based book recommendations based on genre preferences
- CRUD operations on book data
- Exception handling for database and input errors

### Planned

- Book review and comment system
- Admin panel for managing the book database
- Export reading list to file
- Advanced collaborative filtering recommendations

---

## How It Works

1. The user registers or logs in with their credentials.
2. The system presents a menu-driven interface with options to browse, search, rate, and get recommendations.
3. The user can browse all books or filter by genre.
4. The user can search for books by title or author name.
5. The user rates books they have read, which builds a preference profile.
6. The recommendation engine suggests books based on the user's highest-rated genres.

---

## Recommendation Algorithm

The system uses a **rule-based (content-based) recommendation approach**:

1. The user rates books on a scale of 1–5.
2. The system calculates the user's average rating **per genre**.
3. Genres where the user's average rating exceeds a threshold (e.g., 3.0) are considered preferred genres.
4. The system recommends unread books from the user's preferred genres, sorted by genre match.

### Example

```text
User rated:
  "The Alchemist" (Fiction)         → 5
  "A Brief History of Time" (Science) → 4
  "Da Vinci Code" (Fiction)         → 2

Average ratings by genre:
  Fiction  → (5 + 2) / 2 = 3.5  ✓ Preferred
  Science  → 4 / 1 = 4.0        ✓ Preferred

Recommendation: Unread books from Fiction and Science genres,
                sorted by genre match score.
```

> **Note:** The actual algorithm implementation may vary. This section will be updated once `main.py` is implemented.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| MySQL | Relational database for storing books, users, and ratings |
| mysql-connector-python | Python library for MySQL connectivity |

---

## Project Structure

```text
Book-Recommendation-System/
├── main.py            # Main application entry point
├── database.sql       # Database and table creation scripts
├── requirements.txt   # Python dependencies (to be created)
└── README.md          # Project documentation
```

---

## Database Schema

The project uses a MySQL database named `book_recommendation_db` with the following tables:

### `users`

| Column | Type | Description |
|---|---|---|
| user_id | INT (PK, AUTO_INCREMENT) | Unique user identifier |
| username | VARCHAR(50) | User's display name |
| password | VARCHAR(100) | User's password |

### `books`

| Column | Type | Description |
|---|---|---|
| book_id | INT (PK, AUTO_INCREMENT) | Unique book identifier |
| title | VARCHAR(100) | Book title |
| author | VARCHAR(100) | Author name |
| genre | VARCHAR(50) | Book genre |
| description | TEXT | Brief book description |

### `ratings`

| Column | Type | Description |
|---|---|---|
| rating_id | INT (PK, AUTO_INCREMENT) | Unique rating identifier |
| user_id | INT (FK → users) | The user who rated |
| book_id | INT (FK → books) | The book being rated |
| rating | INT (1–5) | User's rating |

### `reading_list`

| Column | Type | Description |
|---|---|---|
| list_id | INT (PK, AUTO_INCREMENT) | Unique entry identifier |
| user_id | INT (FK → users) | The user |
| book_id | INT (FK → books) | The book added |

> **Note:** The actual schema will be finalized in `database.sql`. Columns and table names may change during implementation.

---

## Setup Instructions (Windows)

### Prerequisites

- **Python 3.8+** installed ([Download Python](https://www.python.org/downloads/))
- **MySQL Server 8.0+** installed ([Download MySQL](https://dev.mysql.com/downloads/mysql/))
- **MySQL Workbench** (optional, for GUI database management)

### Step 1: Clone the Repository

```bash
git clone https://github.com/<your-username>/Book-Recommendation-System.git
cd Book-Recommendation-System
```

### Step 2: Set Up the MySQL Database

1. Open MySQL Workbench or the MySQL command line.

2. Run the database setup script:

```bash
mysql -u root -p < database.sql
```

Or paste the contents of `database.sql` directly into MySQL Workbench.

3. Verify the database was created:

```sql
USE book_recommendation_db;
SHOW TABLES;
```

### Step 3: Configure Database Credentials

Update the database connection settings in `main.py` to match your MySQL setup:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",
    "database": "book_recommendation_db"
}
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not yet created, install the dependency manually:

```bash
pip install mysql-connector-python
```

### Step 5: Run the Project

```bash
python main.py
```

---

## Example Usage

```text
=====================================
  BOOK RECOMMENDATION SYSTEM
=====================================

1. Register
2. Login
3. Exit

Enter your choice: 2

Username: ayush
Password: ****

Login successful! Welcome, ayush.

=====================================
  MAIN MENU
=====================================

1. Browse Books
2. Search Books
3. Rate a Book
4. My Reading List
5. Get Recommendations
6. Logout

Enter your choice: 5

--- Recommended Books for You ---

1. "The God of Small Things" by Arundhati Roy (Genre: Fiction)
2. "Cosmos" by Carl Sagan (Genre: Science)

Enter book number to add to reading list (0 to go back):
```

> **Note:** This is a sample output. Actual output will depend on the implementation.

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'mysql.connector'`

```bash
pip install mysql-connector-python
```

### `Access denied for user 'root'@'localhost'`

- Verify your MySQL password is correct.
- Make sure MySQL server is running.
- Try logging in manually: `mysql -u root -p`

### `Unknown database 'book_recommendation_db'`

Run `database.sql` to create the database:

```bash
mysql -u root -p < database.sql
```

### `ProgrammingError: Table doesn't exist`

The database tables have not been created yet. Execute `database.sql` first.

### Port 3306 already in use

Another MySQL instance may be running. Stop it or change the port in your MySQL configuration.

---

## About This Project

This is a **Class 12 CBSE Computer Science project** that demonstrates:

- Python programming fundamentals (loops, conditionals, functions)
- Exception handling
- MySQL database operations (CRUD)
- Python-MySQL connectivity using `mysql-connector-python`
- A rule-based recommendation algorithm

---

## Future Scope

- **Collaborative Filtering:** Recommend books based on similar users' preferences
- **Web Interface:** Build a frontend using Flask or Django
- **Book Cover Images:** Display book covers in the browsing interface
- **Email Notifications:** Notify users when new books in their preferred genres are added
- **Rating Weighting:** Give more weight to recent ratings vs. older ones
- **NLP Integration:** Analyze book descriptions for more accurate genre matching

---

## License

This project is for educational purposes as part of the CBSE Class 12 curriculum. No license is applied.
