"""Billing: a cart is also a hash map (sku -> quantity)."""

from datetime import datetime

TAX_RATE = 0.18  # 18% GST, change as needed


class Bill:
    def __init__(self, inventory, tax_rate=TAX_RATE):
        self.inventory = inventory
        self.tax_rate = tax_rate
        self.cart: dict[str, int] = {}   # sku -> quantity

    def add_item(self, sku, quantity=1):
        product = self.inventory.get(sku)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        wanted = self.cart.get(product.sku, 0) + quantity
        if wanted > product.quantity:
            raise ValueError(f"Only {product.quantity} of {product.name} in stock")
        self.cart[product.sku] = wanted

    def remove_item(self, sku):
        self.cart.pop(sku.strip().upper(), None)

    def subtotal(self):
        return round(
            sum(self.inventory.get(s).price * q for s, q in self.cart.items()), 2
        )

    def tax(self):
        return round(self.subtotal() * self.tax_rate, 2)

    def total(self):
        return round(self.subtotal() + self.tax(), 2)

    def checkout(self):
        """Reduce stock, return the receipt text, and clear the cart."""
        if not self.cart:
            raise ValueError("Cart is empty")
        receipt = self.receipt()
        for sku, qty in self.cart.items():
            self.inventory.reduce_stock(sku, qty)
        self.cart.clear()
        return receipt

    def receipt(self):
        lines = ["=" * 42, f"{'RECEIPT':^42}", datetime.now().strftime("%d-%m-%Y %H:%M").center(42), "=" * 42]
        for sku, qty in self.cart.items():
            p = self.inventory.get(sku)
            lines.append(f"{p.name[:20]:<20} {qty:>3} x {p.price:>7.2f} = {p.price * qty:>8.2f}")
        lines += [
            "-" * 42,
            f"{'Subtotal':<30}{self.subtotal():>12.2f}",
            f"{f'Tax ({self.tax_rate:.0%})':<30}{self.tax():>12.2f}",
            f"{'TOTAL':<30}{self.total():>12.2f}",
            "=" * 42,
        ]
        return "\n".join(lines)
