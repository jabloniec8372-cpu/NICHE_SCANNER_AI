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

    _add_missing_columns(cursor)

    connection.commit()
    connection.close()


def add_product(
    title,
    platform,
    price,
    reviews,
    rating=0,
    listing_id="",
    product_url="",
    image_url="",
    shop_name="",
    shop_url="",
    currency=""
):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    _add_missing_columns(cursor)

    cursor.execute("""
    INSERT OR IGNORE INTO products(
        title,
        platform,
        price,
        reviews,
        rating,
        listing_id,
        product_url,
        image_url,
        shop_name,
        shop_url,
        currency
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        platform,
        price,
        reviews,
        rating,
        listing_id,
        product_url,
        image_url,
        shop_name,
        shop_url,
        currency
    ))

    inserted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return inserted


def get_products():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        title,
        platform,
        price,
        reviews,
        rating,
        listing_id,
        product_url,
        image_url,
        shop_name,
        shop_url,
        currency
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


def _add_missing_columns(cursor):
    cursor.execute("PRAGMA table_info(products)")
    columns = [column[1] for column in cursor.fetchall()]

    if "rating" not in columns:
        cursor.execute("ALTER TABLE products ADD COLUMN rating REAL DEFAULT 0")

    optional_text_columns = [
        "listing_id",
        "product_url",
        "image_url",
        "shop_name",
        "shop_url",
        "currency"
    ]

    for column_name in optional_text_columns:
        if column_name not in columns:
            cursor.execute(f"ALTER TABLE products ADD COLUMN {column_name} TEXT DEFAULT ''")
