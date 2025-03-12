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
    try:
        conn = sqlite3.connect('MyStore_Imanuel.db')
        c = conn.cursor()
        return conn, c

    except Exception as e:
        print(e)


def reset_db(conn, cursor):
    """Resets Database to stock
    Takes connection and cursor, deletes data from tables
    """
    cursor.execute('DELETE FROM Customers_Imanuel')
    cursor.execute('DELETE FROM Items_Imanuel')
    cursor.execute('DELETE FROM Transactions_Imanuel')
    conn.commit()


def write_csv_to_db(conn, cursor):
    """Write CSV to Database
    reads .csv file, and inserts directly into database
    """
    r = csv.reader(open('Customers_Imanuel.csv'), delimiter='-')
    customers = [cust for cust in r]
    sql = "INSERT INTO Customers_Imanuel VALUES (?, ?, ?, ?)"
    cursor.executemany(sql, customers)
    conn.commit()
    print("Customer CSV Inserted successfully")


def write_json_to_db(conn, cursor):
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


def write_file_to_db(conn, cursor):
    with open('Transactions_Imanuel.txt', 'r') as f:
        f.readline()
        f.readline()
        transactions = [list(line.split()) for line in f.readlines()]
        sql = "INSERT INTO Transactions_Imanuel VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, transactions)
        conn.commit()
        print("Transaction file Inserted successfully")


def create_tables(conn, cursor):
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


def fill_categories(conn, c):
    """Fill Category table
    Fetches item and transaction list, then inserts calculated data into
    their respective CategoryTotal table.
    """
    sql = "SELECT * FROM Items_Imanuel"
    c.execute(sql)
    item_list = [Item(i[0], i[1], i[2], i[3]) for i in c.fetchall()]
    sql = "SELECT * FROM Transactions_Imanuel"
    c.execute(sql)
    transaction_list = [Transaction(t[0], t[1], t[2], t[3]) for t in c.fetchall()]

    for item in item_list:
        quantity = sum(q.get_quantity() for q in transaction_list if q.get_id() == item.get_id())
        total = (item.get_id(), item.get_name(), item.get_price()*quantity)
        sql = f"INSERT INTO CategoryTotal_{item.get_category()}(ItemID, Item, Amount) VALUES(?,?,?)"
        c.execute(sql, total)
        print(total)
    conn.commit()


def main():
    """Main program
    Initializes program, fills table and asks user for inputs
    """
    conn, c = create_connection()

    if conn is None:
        print("Unable to Connect to File.")
        return

    reset_db(conn, c)
    write_csv_to_db(conn, c)
    write_json_to_db(conn, c)
    write_file_to_db(conn, c)
    create_tables(conn, c)
    fill_categories(conn, c)


if __name__ == '__main__':
    main()
    print("\n\nSafe Exit :)")
