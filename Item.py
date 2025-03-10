from dataclasses import dataclass


@dataclass
class Item:
    iid: int
    name: str
    category: str
    price: float