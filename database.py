import sqlite3
import json

def connect_db():
    conn = sqlite3.connect("products.db")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_data TEXT,
        improved_data TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_product(original_data, improved_data):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (original_data, improved_data) VALUES (?, ?)",
        (json.dumps(original_data), json.dumps(improved_data))
    )

    conn.commit()
    conn.close()
    
def update_product(product_id, improved_data):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE products SET improved_data = ? WHERE id = ?",
        (json.dumps(improved_data), product_id)
    )

    conn.commit()
    conn.close()

def get_product(product_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    conn.close()
    return row

def get_all_products():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    data = cursor.fetchall()

    conn.close()
    return data