import sqlite3

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

def main():
    conn = create_connection()
    if conn is None:
        print("Unable to Connect to File.")
        return

    c = create_cursor(conn)
    if c is None:
        print("Unable to Connect to File.")
        return



if __name__ == '__main__':
    main()
    print("Program Complete")