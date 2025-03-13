class Transaction:
    def __init__(self, transaction_id, iid, cid, quantity):
        self.transaction_id = transaction_id
        self.iid = iid
        self.cid = cid
        self.quantity = quantity

    def get_quantity(self):
        return self.quantity
    def get_cid(self):
        return self.cid
    def get_iid(self):
        return self.iid
    def __str__(self):
        return f"{self.transaction_id} {self.iid} {self.cid} {self.quantity}"
    def __repr__(self):
        return self.__str__()