"""SQLite persistence: load products into the in-memory dict and save them back."""

import sqlite3
from inventory import Inventory

DB_FILE = "store.db"


def _connect(db_file):
    conn = sqlite3.connect(db_file)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS products (
               sku TEXT PRIMARY KEY,
               name TEXT NOT NULL,
               price REAL NOT NULL,
               quantity INTEGER NOT NULL)"""
    )
    return conn


def load(db_file=DB_FILE):
    inventory = Inventory()
    with _connect(db_file) as conn:
        for sku, name, price, qty in conn.execute("SELECT sku, name, price, quantity FROM products"):
            inventory.add_product(sku, name, price, qty)
    return inventory


def save(inventory, db_file=DB_FILE):
    with _connect(db_file) as conn:
        conn.execute("DELETE FROM products")
        conn.executemany(
            "INSERT INTO products VALUES (?, ?, ?, ?)",
            [(p.sku, p.name, p.price, p.quantity) for p in inventory.products.values()],
        )
