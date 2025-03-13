from StoreManager import StoreManager

def display_item_information(category):
    pass


def display_customer_information(email):
    pass
    # sql = f"SELECT * FROM Customers_Imanuel WHERE Email = '{email}'"
    # cursor.execute(sql)


def main():
    """Main program
    Initializes program, fills table and asks user for inputs

    1. Initialize Database On launch !
    2. User input category; display detailed information !
    3. User input email; display all customer transactions ?
        Calculate and display total cost of all transactions
    4. User enters SQL query; do it
    """
    store = StoreManager()

    print("Welcome to the program!")
    category = input("Enter category: ")
    store.display_category_totals(category)

    email = input("Enter email: ")
    customer = store.retrieve_customer_transactions("alex@myemail.com")


if __name__ == '__main__':
    main()
    print("\n\nSafe Exit :)")