# Mini Inventory & Billing System

A command-line inventory and billing app built in plain Python with SQLite storage.
Built to practise **hash maps (Python dicts)** in a realistic, business-style project.

## Features
- Add, restock, remove and search products
- Low-stock report and total stock value
- Create bills with automatic tax (default 18% GST) and a printable receipt
- Stock is reduced automatically at checkout, and blocked if there isn't enough
- Data saved in a local SQLite database (`store.db`)

## Where hash maps are used
| Where | Key → Value | Why |
|---|---|---|
| `Inventory.products` | SKU → Product | Instant lookup instead of scanning a list |
| `Bill.cart` | SKU → quantity | Adding the same item twice just updates one entry |

## Project structure
```
inventory.py   Product and Inventory classes (business logic)
billing.py     Bill class: cart, tax, receipt, checkout
storage.py     SQLite load/save
main.py        Command-line menu
tests/         Unit tests
```

## Run
```bash
python main.py
```

## Test
```bash
python -m unittest discover -s tests -v
```

## Possible improvements
- Sales history table and daily/monthly sales report
- Export reports to CSV or Excel
- Discounts and customer records
- Charts with Pandas + Matplotlib
- A web UI with Flask or FastAPI
