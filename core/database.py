import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE = PROJECT_ROOT / "data" / "nichescanner.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        platform TEXT,
        price REAL,
        reviews INTEGER,
        rating REAL DEFAULT 0
    )
    """)

    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]

    if "rating" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN rating REAL DEFAULT 0")

    connection.commit()
    connection.close()


def add_product(title, platform, price, reviews, rating=0):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO products(title, platform, price, reviews, rating)
    VALUES (?, ?, ?, ?, ?)
    """, (title, platform, price, reviews, rating))

    inserted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return inserted


def get_products():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT title, platform, price, reviews, rating
    FROM products
    ORDER BY reviews DESC
    """)

    products = cursor.fetchall()
    connection.close()

    return products


def clear_products():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM products")

    connection.commit()
    connection.close()