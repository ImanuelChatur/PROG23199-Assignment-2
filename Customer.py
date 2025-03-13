class Customer:
    def __init__(self, cid, name, city, email):
        self.cid = cid
        self.name = name
        self.city = city
        self.email = email
    def get_email(self):
        return self.email
    def get_name(self):
        return self.name
    def get_id(self):
        return self.cid
    def __str__(self):
        return f"Customer({self.cid}, {self.name}, {self.city}, {self.email})"
    def __repr__(self):
        return f"Customer({self.cid}, {self.name}, {self.city}, {self.email})"