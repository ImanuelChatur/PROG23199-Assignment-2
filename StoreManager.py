import sqlite3


class StoreManager:
    def __init__(self):
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

