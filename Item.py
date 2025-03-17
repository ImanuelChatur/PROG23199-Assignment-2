# Assignment: 2
# Course: PROG23199
# Submission date: 20205-03-16
# Name: Imanuel Chatur
# Sheridan ID: 991637637
# Instructors name: Syed Tanbeer
from dataclasses import dataclass


@dataclass
class Item:
    """Item Class
    Just a dataclass to hold item from table"""
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
