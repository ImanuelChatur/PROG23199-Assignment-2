from StoreManager import StoreManager

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

    print(f"{"-"*40}\nWelcome to the ABC Store\n{"-"*40}")
    category = input("Enter a category: ")
    store.display_category_totals(category)

    email = input("Enter email: ")
    store.display_customer_transactions("alex@myemail.com")


if __name__ == '__main__':
    main()
    print("\n\nSafe Exit :)")