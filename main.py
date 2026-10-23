from billing import Bill
import storage

MENU = """
===== MINI INVENTORY & BILLING =====
1. Add product        5. Search product
2. Restock product    6. Low stock report
3. View all products  7. Create a bill
4. Remove product     8. Stock value
0. Save & exit
"""


def show(products):
    if not products:
        print("No products found.")
        return
    print(f"{'SKU':<8}{'Name':<22}{'Price':>9}{'Qty':>6}")
    for p in products:
        print(f"{p.sku:<8}{p.name[:20]:<22}{p.price:>9.2f}{p.quantity:>6}")


def billing_flow(inv):
    bill = Bill(inv)
    print("Enter SKU and quantity. Leave SKU empty to finish.")
    while True:
        sku = input("SKU: ").strip()
        if not sku:
            break
        try:
            bill.add_item(sku, int(input("Quantity: ")))
        except (KeyError, ValueError) as e:
            print("Error:", e)
    if bill.cart:
        print(bill.checkout())


def main():
    inv = storage.load()
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                inv.add_product(input("SKU: "), input("Name: "),
                                float(input("Price: ")), int(input("Quantity: ")))
            elif choice == "2":
                inv.restock(input("SKU: "), int(input("Add quantity: ")))
            elif choice == "3":
                show(sorted(inv.products.values(), key=lambda p: p.sku))
            elif choice == "4":
                inv.remove_product(input("SKU: "))
            elif choice == "5":
                show(inv.search(input("Keyword: ")))
            elif choice == "6":
                show(inv.low_stock())
            elif choice == "7":
                billing_flow(inv)
            elif choice == "8":
                print("Total stock value:", inv.total_stock_value())
            elif choice == "0":
                storage.save(inv)
                print("Saved. Bye!")
                break
            else:
                print("Invalid choice.")
        except (KeyError, ValueError) as e:
            print("Error:", e)
        storage.save(inv)  # autosave after every action


if __name__ == "__main__":
    main()
