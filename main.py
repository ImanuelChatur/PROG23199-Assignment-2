import json
import sqlite3
import csv
from Customer import Customer
from Item import Item


def create_connection():
    try:
        conn = sqlite3.connect('MyStore_Imanuel.db')
        c = conn.cursor()
        return conn, c

    except Exception as e:
        print(e)


def reset_db(conn, cursor):
    cursor.execute('DELETE FROM Customers_Imanuel')
    cursor.execute('DELETE FROM Items_Imanuel')
    cursor.execute('DELETE FROM Transactions_Imanuel')
    conn.commit()


def write_csv_to_db(conn, cursor):
    r = csv.reader(open('Customers_Imanuel.csv'), delimiter='-')
    customers = [cust for cust in r]
    sql = "INSERT INTO Customers_Imanuel VALUES (?, ?, ?, ?)"
    cursor.executemany(sql, customers)
    conn.commit()
    print("Customer CSV Inserted successfully")


def write_json_to_db(conn, cursor):
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
    sql = "SELECT * FROM Items_Imanuel"
    c.execute(sql)
    item_list = [Item(i[0], i[1], i[2], i[3]) for i in c.fetchall()]
    dairy_list = [i for i in item_list if i.get_category() == "Dairy"]
    meat_list = [i for i in item_list if i.get_category() == "Meat"]
    fruit_list = [i for i in item_list if i.get_category() == "Fruit"]
    snack_list = [i for i in item_list if i.get_category() == "Snacks"]
    veg_list = [i for i in item_list if i.get_category() == "Vegetables"]
    print(item_list)
    print(dairy_list)


def main():
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
