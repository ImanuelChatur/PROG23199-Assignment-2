from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_id: int
    iid: int
    cid: int
    quantity: int

    def get_quantity(self):
        return self.quantity
    def get_id(self):
        return self.iid