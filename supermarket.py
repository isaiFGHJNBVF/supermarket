import mysql.connector

con = mysql.connector.connect(host="localhost", user="root", password="root")
cur = con.cursor()

# Fixed SQL Syntax
cur.execute("CREATE DATABASE IF NOT EXISTS `isk_supermarket`")
cur.execute("USE isk_supermarket")

# Creating tables
cur.execute("""
CREATE TABLE IF NOT EXISTS stock(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(30),
    purchase_price FLOAT,
    selling_price FLOAT,
    quantity INT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sold_products(
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(50),
    quantity INT,
    selling_price FLOAT,
    total FLOAT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS staff(
    staff_id INT PRIMARY KEY,
    name VARCHAR(50),
    phone VARCHAR(15),
    position VARCHAR(30),
    salary FLOAT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    expense_name VARCHAR(50),
    amount FLOAT,
    description VARCHAR(100)
)
""")

con.commit()

# Main Menu
while True:
    print("\n" + "=" * 42)
    print("        isk_supermarket MANAGEMENT")
    print("=" * 42)
    print("1. Stock Entry")
    print("2. View Stock")
    print("3. Search Product")
    print("4. Sell Product")
    print("5. View Sold Products")
    print("6. Add Staff")
    print("7. View Staff")
    print("8. Add Expense")
    print("9. View Expenses")
    print("10. Final Total")
    print("11. Exit")
    print("=" * 42)

    ch = input("Enter your choice: ")

    # STOCK ENTRY
    if ch == "1":
        print("\n---------- STOCK ENTRY ----------")
        try:
            pid = int(input("Enter product id: "))
            pname = input("Enter product name: ")
            category = input("Enter category: ")
            purchase = float(input("Enter purchase price: "))
            selling = float(input("Enter selling price: "))
            qty = int(input("Enter quantity: "))

            cur.execute(
                "INSERT INTO stock VALUES(%s,%s,%s,%s,%s,%s)",
                (pid, pname, category, purchase, selling, qty)
            )
            con.commit()
            print("Product added successfully.")
        except ValueError:
            print("Error: Please enter valid numeric values for ID, price, and quantity.")

    # VIEW STOCK
    elif ch == "2":
        print("\n---------------- STOCK ----------------")
        cur.execute("SELECT * FROM stock")
        data = cur.fetchall()

        if len(data) == 0:
            print("No products in stock.")
        else:
            print("ID   Name   Category   Purchase   Selling   Quantity")
            for x in data:
                print(x[0], x[1], x[2], x[3], x[4], x[5])

    # SEARCH PRODUCT
    elif ch == "3":
        print("\n---------- SEARCH PRODUCT ----------")
        name = input("Enter product name: ")
        cur.execute(
            "SELECT * FROM stock WHERE product_name LIKE %s",
            ("%" + name + "%",)
        )
        data = cur.fetchall()

        if len(data) == 0:
            print("Product not found.")
        else:
            for x in data:
                print("\nProduct ID :", x[0])
                print("Name       :", x[1])
                print("Category   :", x[2])
                print("Purchase   :", x[3])
                print("Selling    :", x[4])
                print("Quantity   :", x[5])

    # SELL PRODUCT
    elif ch == "4":
        print("\n---------- SELL PRODUCT ----------")
        try:
            pid = int(input("Enter product id: "))
            qty = int(input("Enter quantity: "))

            cur.execute("SELECT * FROM stock WHERE product_id=%s", (pid,))
            product = cur.fetchone()

            if product is None:
                print("Product not found.")
            else:
                available = product[5]
                if qty > available:
                    print("Not enough stock.")
                    print("Available quantity:", available)
                else:
                    pname = product[1]
                    selling = product[4]
                    total = selling * qty

                    cur.execute(
                        """INSERT INTO sold_products
                        (product_id,product_name,quantity,selling_price,total)
                        VALUES(%s,%s,%s,%s,%s)""",
                        (pid, pname, qty, selling, total)
                    )
                    cur.execute(
                        "UPDATE stock SET quantity=quantity-%s WHERE product_id=%s",
                        (qty, pid)
                    )
                    con.commit()

                    print("\n========== BILL ==========")
                    print("Product  :", pname)
                    print("Quantity :", qty)
                    print("Price    :", selling)
                    print("Total    :", total)
                    print("==========================")
                    print("Sale completed.")
        except ValueError:
            print("Error: Invalid input format.")

    # VIEW SOLD PRODUCTS
    elif ch == "5":
        print("\n---------- SOLD PRODUCTS ----------")
        cur.execute("SELECT * FROM sold_products")
        data = cur.fetchall()

        if len(data) == 0:
            print("No products sold yet.")
        else:
            for x in data:
                print("\nSale ID      :", x[0])
                print("Product ID   :", x[1])
                print("Product Name :", x[2])
                print("Quantity     :", x[3])
                print("Selling Price:", x[4])
                print("Total        :", x[5])

    # ADD STAFF
    elif ch == "6":
        print("\n---------- STAFF INFORMATION ----------")
        try:
            sid = int(input("Enter staff id: "))
            name = input("Enter staff name: ")
            phone = input("Enter phone number: ")
            position = input("Enter position: ")
            salary = float(input("Enter salary: "))

            cur.execute(
                "INSERT INTO staff VALUES(%s,%s,%s,%s,%s)",
                (sid, name, phone, position, salary)
            )
            con.commit()
            print("Staff added successfully.")
        except ValueError:
            print("Error: Invalid numeric input for ID or salary.")

    # VIEW STAFF
    elif ch == "7":
        print("\n---------- STAFF LIST ----------")
        cur.execute("SELECT * FROM staff")
        data = cur.fetchall()

        if len(data) == 0:
            print("No staff records.")
        else:
            for x in data:
                print("\nStaff ID :", x[0])
                print("Name     :", x[1])
                print("Phone    :", x[2])
                print("Position :", x[3])
                print("Salary   :", x[4])

    # ADD EXPENSE
    elif ch == "8":
        print("\n---------- EXPENSE ----------")
        try:
            ename = input("Enter expense name (Electricity/Maintenance/etc): ")
            amount = float(input("Enter amount: "))
            description = input("Enter description: ")

            cur.execute(
                """INSERT INTO expenses (expense_name,amount,description)
                VALUES(%s,%s,%s)""",
                (ename, amount, description)
            )
            con.commit()
            print("Expense added successfully.")
        except ValueError:
            print("Error: Invalid amount entered.")

    # VIEW EXPENSES
    elif ch == "9":
        print("\n---------- EXPENSE LIST ----------")
        cur.execute("SELECT * FROM expenses")
        data = cur.fetchall()

        if len(data) == 0:
            print("No expenses recorded.")
        else:
            for x in data:
                print("\nExpense ID :", x[0])
                print("Name       :", x[1])
                print("Amount     :", x[2])
                print("Description:", x[3])

    # FINAL TOTAL
    elif ch == "10":
        print("\n" + "=" * 42)
        print("          isk_supermarket")
        print("             FINAL TOTAL")
        print("=" * 42)

        cur.execute("SELECT SUM(total) FROM sold_products")
        sales = cur.fetchone()[0] or 0

        cur.execute("""
            SELECT SUM(sp.quantity * s.purchase_price)
            FROM sold_products sp
            JOIN stock s ON sp.product_id = s.product_id
        """)
        cost = cur.fetchone()[0] or 0

        cur.execute("SELECT SUM(amount) FROM expenses")
        expenses = cur.fetchone()[0] or 0

        cur.execute("SELECT SUM(purchase_price*quantity) FROM stock")
        stock_value = cur.fetchone()[0] or 0

        gross_profit = sales - cost
        net_profit = gross_profit - expenses

        print("Total Sales       :", sales)
        print("Cost of Products  :", cost)
        print("Gross Profit      :", gross_profit)
        print("Total Expenses    :", expenses)
        print("Net Profit        :", net_profit)
        print("Current Stock     :", stock_value)

        print("-" * 42)
        if net_profit > 0:
            print("Status            : PROFIT")
        elif net_profit < 0:
            print("Status            : LOSS")
        else:
            print("Status            : NO PROFIT / NO LOSS")
        print("=" * 42)

    # EXIT
    elif ch == "11":
        print("\nThank you for using isk_supermarket.")
        break

    else:
        print("Invalid choice.")

cur.close()
con.close()
