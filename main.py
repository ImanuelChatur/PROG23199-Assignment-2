from StoreManager import StoreManager

def display_item_information(category):
    pass
    # sql = f"SELECT * FROM CategoryTotal_{category}"
    # cursor.execute(sql)
    # print(f"Display Information of {category}")
    # print(cursor.fetchall())
    # for item in cursor.fetchall():
    #     print(f"{item[1]} costs ${item[2]}")

def display_customer_information(email):
    pass
    # sql = f"SELECT * FROM Customers_Imanuel WHERE Email = '{email}'"
    # cursor.execute(sql)


def main():
    """Main program
    Initializes program, fills table and asks user for inputs
    """
    store = StoreManager()
    store.reset_db()
    store.write_csv_to_db()
    store.write_json_to_db()
    store.write_file_to_db()
    store.create_tables()
    store.fill_categories()

    print("Welcome to the program!")
    category = input("Enter category: ")
    display_item_information(category)
    email = input("Enter email: ")


if __name__ == '__main__':
    main()
    print("\n\nSafe Exit :)")