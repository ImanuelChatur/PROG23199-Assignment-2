import json
import sqlite3
import csv
from Customer import Customer


def create_connection():
    try:
        return sqlite3.connect('MyStore_Imanuel.db')

    except sqlite3.Error as e:
        print(e)


def create_cursor(conn):
    try:
        return conn.cursor()
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
    print(customers)
    sql = "INSERT INTO Customers_Imanuel VALUES (?, ?, ?, ?)"
    cursor.executemany(sql, customers)
    conn.commit()
    print("Customer CSV Inserted successfully")


def write_json_to_db(conn, cursor):
    with open('Items_Imanuel.json', 'r') as f:
        loader = json.load(f)
        items = [[i['iid'], i['name'], i['category'],i['price']] for i in loader]
        sql = "INSERT INTO Items_Imanuel VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, items)
        conn.commit()
        print("Item json Inserted successfully")


def write_file_to_db(conn, cursor):
    with open('Transactions_Imanuel.txt', 'r') as f:
        f.readline()
        f.readline()
        transactions = [list(line.split()) for line in f.readlines()]
        print(transactions)
        sql = "INSERT INTO Transactions_Imanuel VALUES (?, ?, ?, ?)"
        cursor.executemany(sql, transactions)
        conn.commit()


def main():
    conn = create_connection()
    if conn is None:
        print("Unable to Connect to File.")
        return

    c = create_cursor(conn)
    if c is None:
        print("Unable to Connect to File.")
        return

    reset_db(conn, c)
    write_csv_to_db(conn, c)
    write_json_to_db(conn, c)
    write_file_to_db(conn, c)


if __name__ == '__main__':
    main()
    print("Safe Exit :)")