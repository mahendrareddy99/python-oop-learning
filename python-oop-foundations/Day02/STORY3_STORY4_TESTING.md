# Story 3 and Story 4 verification

Run these commands from the `Day02` folder.

## Story 3

```powershell
python magic_methods.py
```

Expected key output:

```text
1. __str__: Laptop (SKU: LAP-01) — 5 units
2. __repr__: Product(sku='LAP-01', name='Laptop', unit_price=50000.0, quantity=5)
3. __len__: 5
4. __eq__: True
5. __lt__: True
6. __gt__: True
7. __add__: Laptop (SKU: LAP-01) — 8 units
8. __sub__: Laptop (SKU: LAP-01) — 2 units
9. combined quantity: 8
```

## Story 4

Start the app:

```powershell
python -m library_management.app
```

Try the workflow: add a book → register a member → issue book → return book → reports. IDs are shown after adding/registering/issuing. To check JSON persistence, exit and start the app again.

The app uses a default 14-day loan and a fine of ₹5 per overdue day. For a deterministic late-fine test, use the classes directly and pass explicit dates to `issue_book` and `return_book`.
