import os, sys, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from inventory import Inventory
from billing import Bill
import storage


def make_inventory():
    inv = Inventory()
    inv.add_product("p1", "Milk", 50, 10)
    inv.add_product("p2", "Bread", 30, 3)
    return inv


class InventoryTests(unittest.TestCase):
    def test_add_and_get_is_case_insensitive(self):
        self.assertEqual(make_inventory().get("P1").name, "Milk")

    def test_duplicate_sku_rejected(self):
        with self.assertRaises(ValueError):
            make_inventory().add_product("P1", "Other", 1, 1)

    def test_negative_values_rejected(self):
        with self.assertRaises(ValueError):
            Inventory().add_product("x", "X", -5, 1)

    def test_restock(self):
        inv = make_inventory()
        inv.restock("P2", 7)
        self.assertEqual(inv.get("P2").quantity, 10)

    def test_unknown_sku(self):
        with self.assertRaises(KeyError):
            make_inventory().get("NOPE")

    def test_remove(self):
        inv = make_inventory()
        inv.remove_product("P1")
        self.assertNotIn("P1", inv.products)

    def test_search_and_low_stock(self):
        inv = make_inventory()
        self.assertEqual([p.sku for p in inv.search("mil")], ["P1"])
        self.assertEqual([p.sku for p in inv.low_stock(5)], ["P2"])

    def test_stock_value(self):
        self.assertEqual(make_inventory().total_stock_value(), 590.0)


class BillingTests(unittest.TestCase):
    def test_totals(self):
        bill = Bill(make_inventory(), tax_rate=0.10)
        bill.add_item("P1", 2)          # 100
        bill.add_item("P2", 1)          # 30
        self.assertEqual(bill.subtotal(), 130.0)
        self.assertEqual(bill.total(), 143.0)

    def test_cannot_exceed_stock(self):
        bill = Bill(make_inventory())
        with self.assertRaises(ValueError):
            bill.add_item("P2", 4)

    def test_cart_accumulates_and_checks_stock(self):
        bill = Bill(make_inventory())
        bill.add_item("P2", 2)
        with self.assertRaises(ValueError):
            bill.add_item("P2", 2)

    def test_checkout_reduces_stock_and_clears_cart(self):
        inv = make_inventory()
        bill = Bill(inv)
        bill.add_item("P1", 4)
        bill.checkout()
        self.assertEqual(inv.get("P1").quantity, 6)
        self.assertEqual(bill.cart, {})

    def test_empty_checkout(self):
        with self.assertRaises(ValueError):
            Bill(make_inventory()).checkout()


class StorageTests(unittest.TestCase):
    def test_save_and_load_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            db = os.path.join(d, "t.db")
            storage.save(make_inventory(), db)
            loaded = storage.load(db)
            self.assertEqual(loaded.get("P1").quantity, 10)
            self.assertEqual(len(loaded.products), 2)


if __name__ == "__main__":
    unittest.main()
