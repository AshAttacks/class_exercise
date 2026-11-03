import logging
import sqlite3
from pathlib import Path

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

class BookStorage:
    def __init__(self, db_path="data/books.db"):
        self.db_path = db_path

    def add_book(self, title, price):
        connection = sqlite3.connect(self.db_path)
        try:
            # TODO: INSERT using sql_statement and placeholders
            sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
            # Keep cursor.lastrowid, commit, and log the new ID at DEBUG.
            row = connection.execute(sql_statement, (title, price))
            # Return the assigned ID.
            book_id = row.lastrowid
            logger.info(f"Book {title} : ID {book_id}")
            connection.commit()
            return book_id
        except sqlite3.Error:
            #For a failed write, `rollback()` cancels uncommitted changes and `raise` passes the error to the caller.
            connection.rollback()
            raise
        finally:
            # Always close the connection, whether the operation succeeds or fails.
            connection.close()

    def get_book(self, book_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            # TODO: SELECT by ID using a placeholder and fetchone().
            sql_statement = "SELECT * FROM books WHERE id = ?"
            connection.execute(sql_statement, (book_id,))
            row = connection.execute(sql_statement, (book_id,)).fetchone()
            # Log the ID and whether a row was found (e.g., not None) at DEBUG.
            if row is not None:
                logger.debug(f"Book ID: {book_id} | Row found: {row}")
                return dict(row)
            else:
                return None
            # Return None if missing; otherwise, return dict(row).
        finally:
            connection.close()

    def list_books(self, min_price=0, limit=100):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            # TODO: SELECT id, title, and price where price >= min_price.
            # Sort price DESC, then id ASC (comma-separated),
            # and Apply limit.

            sql_statement = ("SELECT * FROM books "
                             "WHERE price >= ? "
                             "ORDER BY price DESC, id ASC "
                             "LIMIT ?")

            # Use placeholders and fetchall(); return a list of dictionaries.
            rows = connection.execute(sql_statement, (min_price, limit)).fetchall()
            # Log the returned row count at DEBUG.
            logger.debug(f"Returned Rows: {rows}")
            return rows
        finally:
            connection.close()

def main():
    path = Path("data") / "books.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    sql_statement = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL
    )
    """

    connection.execute(sql_statement)
    connection.execute("DELETE FROM books")
    connection.commit()

    sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
    cursor = connection.execute(sql_statement, ("Book A", 12.5))
    book_id = cursor.lastrowid
    connection.commit()

    connection.execute(sql_statement, ("Book B", 25.0))
    connection.execute(sql_statement, ("Book C", 18.0))
    connection.commit()

    rows = [("Book D", 15.0), ("Book E", 10.0)]
    connection.executemany(sql_statement, rows)
    connection.commit()

    # Retrieve one book
    sql_statement = "SELECT id, title, price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(dict(row))

    # Preview the first n
    sql_statement = "SELECT * FROM books ORDER BY id LIMIT ?"
    rows = connection.execute(sql_statement, (5,)).fetchall()
    print([dict(row) for row in rows])

    # Filter and Sort
    sql_statement = """
                    SELECT title, price \
                    FROM books
                    WHERE price >= ? \
                    ORDER BY price DESC LIMIT ? \
                    """
    rows = connection.execute(sql_statement, (15, 2)).fetchall()
    print([dict(row) for row in rows])

    # Total count
    sql_statement = "SELECT COUNT(*) AS total FROM books"
    row = connection.execute(sql_statement).fetchone()
    print(row["total"])

    # Update
    sql_statement = "UPDATE books SET price = ? WHERE id = ?"
    connection.execute(sql_statement, (13.0, book_id))
    connection.commit()

    # Check
    sql_statement = "SELECT price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(row["price"])  # 13.0

    connection.close()

    # ...
    # connection.close()

    storage = BookStorage()
    book_id = storage.add_book("Book A", 12.5)

    print(storage.get_book(book_id)["title"])
    print(storage.get_book(book_id)["price"])
    books = storage.list_books(min_price=15, limit=2)
    print([(book["title"], book["price"]) for book in books])

    logger.info(f"Added book: id={book_id}")



if __name__ == "__main__":
    main()