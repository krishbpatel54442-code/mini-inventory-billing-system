"""Inventory logic. Products live in a dict (a hash map) keyed by SKU,
so lookup, add, update and delete are all O(1) on average."""

from dataclasses import dataclass


@dataclass
class Product:
    sku: str
    name: str
    price: float
    quantity: int = 0


class Inventory:
    def __init__(self):
        self.products: dict[str, Product] = {}   # sku -> Product

    def add_product(self, sku, name, price, quantity=0):
        sku = sku.strip().upper()
        if sku in self.products:
            raise ValueError(f"SKU {sku} already exists")
        if price < 0 or quantity < 0:
            raise ValueError("Price and quantity cannot be negative")
        self.products[sku] = Product(sku, name.strip(), float(price), int(quantity))
        return self.products[sku]

    def get(self, sku):
        product = self.products.get(sku.strip().upper())
        if product is None:
            raise KeyError(f"No product with SKU {sku}")
        return product

    def restock(self, sku, amount):
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        product = self.get(sku)
        product.quantity += amount
        return product

    def reduce_stock(self, sku, amount):
        product = self.get(sku)
        if amount > product.quantity:
            raise ValueError(
                f"Only {product.quantity} of {product.name} in stock, requested {amount}"
            )
        product.quantity -= amount

    def remove_product(self, sku):
        self.get(sku)
        del self.products[sku.strip().upper()]

    def search(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.products.values() if keyword in p.name.lower()]

    def low_stock(self, threshold=5):
        return sorted(
            (p for p in self.products.values() if p.quantity <= threshold),
            key=lambda p: p.quantity,
        )

    def total_stock_value(self):
        return round(sum(p.price * p.quantity for p in self.products.values()), 2)
