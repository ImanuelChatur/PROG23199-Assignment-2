# Assignment: 2
# Course: PROG23199
# Submission date: 20205-03-16
# Name: Imanuel Chatur
# Sheridan ID: 991637637
# Instructors name: Syed Tanbeer
import csv
import json
import sqlite3
from Customer import Customer
from Item import Item
from Transaction import Transaction


class StoreManager:
    """Store Manager Class
    Manages the entire database; performs actions modifies tables etc.
    Done in a class to stay modular and avoid global usage
    """

    # Class variables
    store_db = "MyStore_Imanuel.db"
    valid_categories = ("dairy", "vegetables", "fruit", "meat", "snacks")

    def __init__(self):
        """Initialize connection for Store database"""
        try:
            self.conn = sqlite3.connect(StoreManager.store_db)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(e)

        # Get lists from tables
        self.items = self.get_items()
        self.transactions = self.get_transactions()
        self.customers = self.get_customers()
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

        # Fill Database
        self.write_csv_to_db()
        self.write_json_to_db()
        self.write_file_to_db()

        # Create and fill tables
        self.create_tables()
        self.fill_categories()
        self.conn.commit()

    def get_items(self):
        """Gets items from database
        Grabs updated tables from database
        """
        try:
            sql = "SELECT * FROM Items_Imanuel"
            self.cursor.execute(sql)
            self.items = [Item(i[0], i[1], i[2], i[3])
                          for i in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(e)

        return self.items

    def get_transactions(self):
        """Gets transactions from database
        Grabs updated tables from database"""
        try:
            sql = "SELECT * FROM Transactions_Imanuel"
            self.cursor.execute(sql)
            self.transactions = [Transaction(
                t[0], t[1], t[2], t[3]) for t in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(e)

        return self.transactions

    def get_customers(self):
        """Gets customers from database
        Grabs updated tables from database"""
        try:
            sql = "SELECT * FROM Customers_Imanuel"
            self.cursor.execute(sql)
            self.customers = [Customer(
                c[0], c[1], c[2], c[3]) for c in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(e)

        return self.customers

    def write_csv_to_db(self):
        """Write CSV to database
        reads .csv file and inserts directly into database"""
        try:
            with open('Customers_Imanuel.csv', 'r') as f:
                r = csv.reader(f, delimiter='-')
                customers = [cust for cust in r]
                sql = "INSERT INTO Customers_Imanuel VALUES (?, ?, ?, ?)"
                self.cursor.executemany(sql, customers[1:])
                self.conn.commit()
            print("Customer CSV Inserted successfully")
        except Exception as e:
            print(e)

    def write_json_to_db(self):
        """Write JSON to Database
        reads .json file and inserts directly into database
        """
        try:
            # Takes JSON as a dict, then with its keys assigns values
            with open('Items_Imanuel.json', 'r') as f:
                loader = json.load(f)
                items = [[i['iid'], i['name'], i['category'], i['price']
                          ] for i in loader]
                sql = "INSERT INTO Items_Imanuel VALUES (?, ?, ?, ?)"
                self.cursor.executemany(sql, items)
                self.conn.commit()
                print("Item json Inserted successfully")
        except Exception as e:
            print(e)

    def write_file_to_db(self):
        """Write Text file to Database
        reads .txt file and inserts directly into database"""
        try:
            with open('Transactions_Imanuel.txt', 'r') as f:
                transactions = [list(line.split()) for line in f.readlines()]
                sql = "INSERT INTO Transactions_Imanuel VALUES (?, ?, ?, ?)"
                self.cursor.executemany(sql, transactions[2:])
                self.conn.commit()
                print("Transaction file Inserted successfully")
        except Exception as e:
            print(e)

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
        try:
            for item in self.items:
                # For every item, check transaction table and add all quantities
                quantity = sum(
                    q.get_quantity()
                    for q in self.transactions
                    if q.get_iid() == item.get_id())

                # Calculate item price * the quantity
                total = (item.get_id(),
                         item.get_name(),
                         item.get_price() * quantity)

                sql = (f"INSERT INTO CategoryTotal_{item.get_category()}"
                       f"(ItemID, Item, Amount) VALUES(?,?,?)")
                self.cursor.execute(sql, total)
            # insert into db
            self.conn.commit()
        except Exception as e:
            print(e)

    def display_customer_transactions(self, cust_email):
        """Retrieve Customer and their transactions
        Gets transactions that belong to the customer into a list
        """
        sql = f"""
        SELECT c.name, i.name, i.price, t.quantity,
         i.price * t.quantity as 'total' from Transactions_Imanuel as t
        INNER JOIN Items_Imanuel as i
        ON i.iid = t.iid
        INNER JOIN Customers_Imanuel as c
        ON t.cid = c.cid
        WHERE c.email = ?
        """

        try:  # Try to execute query, return error if not
            self.cursor.execute(sql, (cust_email,))
            # Fetch all customer transactions based off email
            cust_transactions = self.cursor.fetchall()

        except sqlite3.Error as e:
            print("Database Error!")
            return

        if not cust_transactions:  # Check if email has anything
            print(f"No transactions found for {cust_email}")
            return

        # Formatted printing
        print(f"Transactions of {cust_transactions[0][0]}\n{"-" * 40}")
        print("Item\tPrice\tQuantity")
        total_cost = 0
        for i in cust_transactions:
            # Unpack tuple and formatted print
            cust_name, item_name, item_price, item_quantity, cost = i
            total_cost += cost
            print(f"{item_name}\t{item_price}\t{item_quantity}\t{cost}")
        print(f"Total Cost of "
              f"{cust_transactions[0][0]} is {total_cost}\n{"-" * 40}")

    def display_category_totals(self, category):
        """Display Category_total tables
        Protects from SQL injection by checking if in list
        Selects table and displays information via query"""

        if category.lower() not in StoreManager.valid_categories:
            print("Invalid Category")
            return

        try:
            sql = f"SELECT * FROM CategoryTotal_{category}"
            self.cursor.execute(sql)
        except sqlite3.Error as e:
            print("Database Error!")

        print(f"Display Information of {category}\n{"-" * 40}")
        for item in self.cursor.fetchall():
            print(f"{item[1]} costs ${item[2]}")

    def display_item_query(self, x, y):
        """Display Item query
        Make a selection (x)
        Add conditionals (y)
        Displays the query line by line or throws error"""

        try:
            sql = f"SELECT {x} from Items_Imanuel WHERE {y}"
            print(sql)
            self.cursor.execute(sql)
            for item in self.cursor.fetchall():
                print(item)
        except Exception as e:
            print(e)

    def close_database(self):
        """Close database
        Just closes up"""
        self.cursor.close()
        self.conn.close()
