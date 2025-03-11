from dataclasses import dataclass


@dataclass
class Item:
    iid: int
    name: str
    category: str
    price: float

    def get_category(self):
        return self.category

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_id(self):
        return self.iid
