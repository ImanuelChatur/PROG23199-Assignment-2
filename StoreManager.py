import csv
import json
import sqlite3

from Item import Item
from Transaction import Transaction


class StoreManager:
    def __init__(self):
        """Initialize connection for Store database"""
        try:
            self.conn = sqlite3.connect('MyStore_Imanuel.db')
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

    def reset_db(self):
        self.cursor.executescript("""
        DELETE FROM Customers_Imanuel;
        DELETE FROM Items_Imanuel;
        DELETE FROM Transactions_Imanuel;
        """)
        self.conn.commit()

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
        sql = "SELECT * FROM Items_Imanuel"
        self.cursor.execute(sql)
        item_list = [Item(i[0], i[1], i[2], i[3]) for i in self.cursor.fetchall()]
        sql = "SELECT * FROM Transactions_Imanuel"
        self.cursor.execute(sql)
        transaction_list = [Transaction(t[0], t[1], t[2], t[3]) for t in self.cursor.fetchall()]

        for item in item_list:
            quantity = sum(q.get_quantity() for q in transaction_list if q.get_id() == item.get_id())
            total = (item.get_id(), item.get_name(), item.get_price() * quantity)
            sql = f"INSERT INTO CategoryTotal_{item.get_category()}(ItemID, Item, Amount) VALUES(?,?,?)"
            self.cursor.execute(sql, total)
        self.conn.commit()