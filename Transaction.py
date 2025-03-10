from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_id: int
    iid: int
    cid: int
    quantity: int