from models import Product

class InventoryManager:
    def __init__(self):
        self.products: list[Product] = []
        self._next_id = 1

    def load_from_dicts(self, rows: list[dict]) -> None:
        self.products = []
        max_id = 0
        for r in rows:
            p = Product(
                id=int(r["id"]),
                name=str(r["name"]),
                price=float(r["price"]),
                qty=int(r["qty"]),
            )
            self.products.append(p)
            max_id = max(max_id, p.id)
        self._next_id = max_id + 1

    def to_dicts(self) -> list[dict]:
        return [
            {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "qty": p.qty,
            }
            for p in self.products
        ]
    
    def add_product(self, name: str, price: float, qty: int) -> Product:
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if qty < 0:
            raise ValueError("Quantity cannot be negative")
        
        P = Product(
            id=self._next_id,
            name=name,
            price=price,
            qty=qty,
        )
        self.products.append(P)
        self._next_id += 1
        return P
    
    