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
    
    def delete_product(self, product_id: int) -> bool:
        for i, p in enumerate(self.products):
            if p.id == product_id:
                self.products.pop(i)
                return True
        return False
    
    def update_product(self, product_id: int, name: str, price: float, qty: int) -> bool:
        name = name.strip()
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if qty < 0:
            raise ValueError("Quantity cannot be negative")

        p = self.get_by_id(product_id)
        if not p:
            return False
        p.name = name
        p.price = price
        p.qty = qty
        return True
    
    def get_by_id(self, product_id: int) -> Product | None:
        for p in self.products:
            if p.id == product_id:
                return p
        return None

    def search_by_name(self, query: str) -> list[Product]:
        q = query.strip().lower()
        if not q:
            return self.products [:]
        return [p for p in self.products if q in p.name.lower()]

    def sort_by_products(self, key: str) -> list[Product]:
        if key == "name":
            return sorted(self.products, key=lambda p: p.name.lower())
        if key == "qty":
            return sorted(self.products, key=lambda p: p.qty)
        return self.products [:]
    
    def total_inventory_value(self) -> float:
        return sum (p.price * p.qty for p in self.products)
    
    def low_stock(self, threshold: int = 5) -> list[Product]:
        return [p for p in self.products if p.qty < threshold]