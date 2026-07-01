import sqlite3


DATABASE = "data/nichescanner.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE,
        platform TEXT,
        price REAL,
        reviews INTEGER
    )
    """)

    connection.commit()
    connection.close()


def add_product(title, platform, price, reviews):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO products(title, platform, price, reviews)
    VALUES (?, ?, ?, ?)
    """, (title, platform, price, reviews))

    connection.commit()
    connection.close()


def get_products():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT title, platform, price, reviews
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