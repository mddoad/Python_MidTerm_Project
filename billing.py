from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CartItem:
    product_id: int
    name: str
    price: float
    qty: int

    @property
    def line_total(self) -> float:
        return self.price * self.qty


@dataclass
class Invoice:
    invoice_id: int
    created_at: str
    items: list[CartItem] = field(default_factory=list)

    def total(self) -> float:
        return sum(i.line_total for i in self.items)

    def to_dict(self) -> dict:
        return {
            "invoice_id": self.invoice_id,
            "created_at": self.created_at,
            "total": self.total(),
            "items": [
                {
                    "product_id": i.product_id,
                    "name": i.name,
                    "price": i.price,
                    "qty": i.qty,
                    "line_total": i.line_total,
                }
                for i in self.items
            ],
        }


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")