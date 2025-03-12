import json
import sqlite3
import csv

from Customer import Customer
from Item import Item
from Transaction import Transaction


def create_connection():
    """Opens SQL connection
    returns:
        conn: sql connection
        c: sql cursor
    """
    global conn
    global cursor
    try:
        conn = sqlite3.connect('MyStore_Imanuel.db')
        cursor = conn.cursor()
    except Exception as e:
        print(e)


def reset_db():
    """Resets Database to stock
    Takes connection and cursor, deletes data from tables
    """
    cursor.execute('DELETE FROM Customers_Imanuel')
    cursor.execute('DELETE FROM Items_Imanuel')
    cursor.execute('DELETE FROM Transactions_Imanuel')
    conn.commit()


def write_csv_to_db():
    """Write CSV to Database
    reads .csv file, and inserts directly into database
    """
    r = csv.reader(open('Customers_Imanuel.csv'), delimiter='-')
    customers = [cust for cust in r]
    sql = "INSERT INTO Customers_Imanuel VALUES (?, ?, ?, ?)"
    cursor.executemany(sql, customers)
    conn.commit()
    print("Customer CSV Inserted successfully")


def write_json_to_db():
    """Write JSON to Database
    reads .json file and inserts directly into database
    """
    with open('Items_Imanuel.json', 'r') as f:
        loader = json.load(f)
        items = [[i['iid'], i['name'], i['category'], i['price']] for i in loader]
        sql = "INSERT INTO Items_Imanuel VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, items)
        conn.commit()
        print("Item json Inserted successfully")


def write_file_to_db():
    with open('Transactions_Imanuel.txt', 'r') as f:
        f.readline()
        f.readline()
        transactions = [list(line.split()) for line in f.readlines()]
        sql = "INSERT INTO Transactions_Imanuel VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, transactions)
        conn.commit()
        print("Transaction file Inserted successfully")


def create_tables():
    """Create tables
    Creates category in database, drops tables if existed before
    """
    cursor.executescript(
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
    conn.commit()


def fill_categories():
    """Fill Category table
    Fetches item and transaction list, then inserts calculated data into
    their respective CategoryTotal table.
    """
    sql = "SELECT * FROM Items_Imanuel"
    cursor.execute(sql)
    item_list = [Item(i[0], i[1], i[2], i[3]) for i in cursor.fetchall()]
    sql = "SELECT * FROM Transactions_Imanuel"
    cursor.execute(sql)
    transaction_list = [Transaction(t[0], t[1], t[2], t[3]) for t in cursor.fetchall()]

    for item in item_list:
        quantity = sum(q.get_quantity() for q in transaction_list if q.get_id() == item.get_id())
        total = (item.get_id(), item.get_name(), item.get_price()*quantity)
        sql = f"INSERT INTO CategoryTotal_{item.get_category()}(ItemID, Item, Amount) VALUES(?,?,?)"
        cursor.execute(sql, total)
    conn.commit()

def display_item_information(category):
    sql = f"SELECT * FROM CategoryTotal_{category}"
    cursor.execute(sql)
    print(f"Display Information of {category}")
    print(cursor.fetchall())
    for item in cursor.fetchall():
        print(f"{item[1]} costs ${item[2]}")

def display_customer_information(email):
    sql = f"SELECT * FROM Customers_Imanuel WHERE Email = '{email}'"
    cursor.execute(sql)


def main():
    """Main program
    Initializes program, fills table and asks user for inputs
    """
    create_connection()
    reset_db()
    write_csv_to_db()
    write_json_to_db()
    write_file_to_db()
    create_tables()
    fill_categories()

    print("Welcome to the program!")
    category = input("Enter category: ")
    display_item_information(category)
    email = input("Enter email: ")


if __name__ == '__main__':
    main()
    print("\n\nSafe Exit :)")