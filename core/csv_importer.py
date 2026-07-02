import csv
from pathlib import Path


REQUIRED_COLUMNS = {"title", "price", "reviews", "rating"}


def import_products_from_csv(file_path):
    path = Path(file_path).expanduser()

    if not path.exists():
        print()
        print("[ERROR] CSV file was not found.")
        print(f"Path: {path}")
        print()
        return []

    if not path.is_file():
        print()
        print("[ERROR] The selected path is not a file.")
        print(f"Path: {path}")
        print()
        return []

    products = []
    skipped_rows = 0

    try:
        with open(path, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print()
                print("[ERROR] CSV file is empty or missing a header row.")
                print()
                return []

            columns = {column.strip().lower() for column in reader.fieldnames}
            missing_columns = REQUIRED_COLUMNS - columns

            if missing_columns:
                print()
                print("[ERROR] CSV file is missing required columns:")
                for column in sorted(missing_columns):
                    print(f"- {column}")
                print()
                return []

            for row_number, row in enumerate(reader, start=2):
                product = _parse_product_row(row, row_number)

                if product is None:
                    skipped_rows += 1
                else:
                    products.append(product)

    except OSError as error:
        print()
        print("[ERROR] CSV file could not be read.")
        print(error)
        print()
        return []

    print()
    print(f"[OK] Valid CSV rows found: {len(products)}")

    if skipped_rows:
        print(f"[INFO] Skipped invalid rows: {skipped_rows}")

    print()
    return products


def _parse_product_row(row, row_number):
    normalized_row = {
        key.strip().lower(): value
        for key, value in row.items()
        if key is not None
    }

    title = normalized_row.get("title", "").strip()

    if not title:
        print(f"[SKIP] Row {row_number}: title is empty.")
        return None

    try:
        price = float(normalized_row.get("price", "").strip())
        reviews = int(normalized_row.get("reviews", "").strip())
        rating = float(normalized_row.get("rating", "").strip())
    except ValueError:
        print(f"[SKIP] Row {row_number}: price, reviews, or rating is not a valid number.")
        return None

    if price < 0:
        print(f"[SKIP] Row {row_number}: price cannot be negative.")
        return None

    if reviews < 0:
        print(f"[SKIP] Row {row_number}: reviews cannot be negative.")
        return None

    if rating < 0 or rating > 5:
        print(f"[SKIP] Row {row_number}: rating must be between 0 and 5.")
        return None

    return {
        "title": title,
        "platform": "CSV Import",
        "price": price,
        "reviews": reviews,
        "rating": rating
    }
