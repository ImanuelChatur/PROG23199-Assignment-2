from dataclasses import dataclass


@dataclass
class Customer:
    cid: int
    name: str
    city: str
    email: str