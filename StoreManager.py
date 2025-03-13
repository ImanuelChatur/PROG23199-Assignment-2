import csv
import json
import sqlite3

from Customer import Customer
from Item import Item
from Transaction import Transaction


class StoreManager:
    customer_csv = "Customers_Imanuel.csv"
    items_json = "Items_Imanuel.json"
    transactions_txt = "Transactions_Imanuel.txt"
    store_db = "MyStore_Imanuel.db"

    def __init__(self):
        """Initialize connection for Store database"""
        try:
            self.conn = sqlite3.connect(StoreManager.store_db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)
        self.items = self.get_items()
        self.transactions = self.get_transactions()
        self.customers = self.get_customer()

        self.initialize_db()

    def initialize_db(self):
        """Initialize Database
        - Empties Customers, Items and Transaction tables
        - Writes CSV, JSON and TXT files into the now empty tables
        - Creates category tables
        - Populates category tables
        """
        self.cursor.executescript("""
        DELETE FROM Customers_Imanuel;
        DELETE FROM Items_Imanuel;
        DELETE FROM Transactions_Imanuel; """)

        #Fill Database
        self.write_csv_to_db()
        self.write_json_to_db()
        self.write_file_to_db()

        #Create and fill tables
        self.create_tables()
        self.fill_categories()
        self.conn.commit()

    def get_items(self):
        sql = "SELECT * FROM Items_Imanuel"
        self.cursor.execute(sql)
        self.items = [Item(i[0], i[1], i[2], i[3]) for i in self.cursor.fetchall()]
        return self.items

    def get_transactions(self):
        sql = "SELECT * FROM Transactions_Imanuel"
        self.cursor.execute(sql)
        self.transactions = [Transaction(t[0], t[1], t[2], t[3]) for t in self.cursor.fetchall()]
        return self.transactions
    def get_customers(self):
        sql = "SELECT * FROM Customers_Imanuel"
        self.cursor.execute(sql)
        self.customers = Customer(Customer(c[0],c[1],c[2],c[3]) for c in self.cursor.fetchall())

    def write_csv_to_db(self):
        r = csv.reader(open('Customers_Imanuel.csv'), delimiter='-')
        customers = [cust for cust in r]
        sql = "INSERT INTO Customers_Imanuel VALUES (?, ?, ?, ?)"
        self.cursor.executemany(sql, customers)
        self.conn.commit()
        print("Customer CSV Inserted successfully")

    def write_json_to_db(self):
        """Write JSON to Database
        reads .json file and inserts directly into database
        """
        with open('Items_Imanuel.json', 'r') as f:
            loader = json.load(f)
            items = [[i['iid'], i['name'], i['category'], i['price']] for i in loader]
            sql = "INSERT INTO Items_Imanuel VALUES (?, ?, ?, ?)"
            self.cursor.executemany(sql, items)
            self.conn.commit()
            print("Item json Inserted successfully")

    def write_file_to_db(self):
        with open('Transactions_Imanuel.txt', 'r') as f:
            f.readline()
            f.readline()
            transactions = [list(line.split()) for line in f.readlines()]
            sql = "INSERT INTO Transactions_Imanuel VALUES (?, ?, ?, ?)"
            self.cursor.executemany(sql, transactions)
            self.conn.commit()
            print("Transaction file Inserted successfully")

    def create_tables(self):
        """Create tables
        Creates category in database, drops tables if existed before
        """
        self.cursor.executescript(
            '''
            DROP TABLE IF EXISTS CategoryTotal_Dairy;
            DROP TABLE IF EXISTS CategoryTotal_Meat;
            DROP TABLE IF EXISTS CategoryTotal_Fruit;
            DROP TABLE IF EXISTS CategoryTotal_Snacks;
            DROP TABLE IF EXISTS CategoryTotal_Vegetables;
            CREATE TABLE "CategoryTotal_Dairy" (
                "ItemID"	INTEGER,
    	        "Item"	VARCHAR(20),
    	        "Amount"	FLOAT,
    	        PRIMARY KEY("ItemID")
                );
            CREATE TABLE "CategoryTotal_Meat" (
    	        "ItemID"	INTEGER,
    	        "Item"	VARCHAR(20),
    	        "Amount"	FLOAT,
    	        PRIMARY KEY("ItemID")
            );
            CREATE TABLE "CategoryTotal_Fruit" (
    	        "ItemID"	INTEGER,
    	        "Item"	VARCHAR(20),
    	        "Amount"	FLOAT,
    	        PRIMARY KEY("ItemID")
            );
            CREATE TABLE "CategoryTotal_Snacks" (
    	        "ItemID"	INTEGER,
    	        "Item"	VARCHAR(20),
    	        "Amount"	FLOAT,
    	        PRIMARY KEY("ItemID")
            );
            CREATE TABLE "CategoryTotal_Vegetables" (
                "ItemID"	INTEGER,
                "Item"	VARCHAR(20),
                "Amount"	FLOAT,
                PRIMARY KEY("ItemID")
            );
            ''')
        self.conn.commit()

    def fill_categories(self):
        """Fill Category table
        Fetches item and transaction list, then inserts calculated data into
        their respective CategoryTotal table.
        """
        for item in self.items:
            quantity = sum(q.get_quantity() for q in self.transactions if q.get_id() == item.get_id())
            total = (item.get_id(), item.get_name(), item.get_price() * quantity)
            sql = f"INSERT INTO CategoryTotal_{item.get_category()}(ItemID, Item, Amount) VALUES(?,?,?)"
            self.cursor.execute(sql, total)
        self.conn.commit()

    def display_item_by_category(self):
        pass

    def retrieve_customer_transactions(self, cust_email):
        """
        """
        sql = f"""
        SELECT c.name, i.name, i.price, t.quantity, i.price * t.quantity as 'total' from Transactions_Imanuel as t
        INNER JOIN Items_Imanuel as i
        ON i.iid = t.iid
        INNER JOIN Customers_Imanuel as c
        ON t.cid = c.cid
        WHERE c.email = '{cust_email}'
        """
        self.cursor.execute(sql)
        for i in self.cursor.fetchall():
            print(i)

    def display_category_totals(self, category):
        sql = f"SELECT * FROM CategoryTotal_{category}"
        self.cursor.execute(sql)
        print(f"Display Information of {category}")
        for item in self.cursor.fetchall():
            print(f"{item[1]} costs ${item[2]}")