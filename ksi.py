import mysql.connector
con = mysql.connector.connect(host="localhost",user="root",password="root")
cur = con.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS ksi_cars")
cur.execute("USE ksi_cars")
cur.execute("""
CREATE TABLE IF NOT EXISTS cars(
car_number INT PRIMARY KEY,
car_name VARCHAR(50),
car_brand_name VARCHAR(50),
car_price FLOAT,
car_engine VARCHAR(30),
fuel_type VARCHAR(20)
)
""")
con.commit()
total = 0
while True:

    print("==========================================")
    print("       KSI CAR SHOWROOM MANAGEMENT")
    print("==========================================")
    print("1. Add Car")
    print("2. View Cars")
    print("3. Search Car")
    print("4. Update Car")
    print("5. Delete Car")
    print("6. Sell Car")
    print("7. Total")
    print("8. Exit")
    print("==========================================")
    ch = int(input("Enter your choice: "))
    if ch == 1:
        print("---------- ADD CAR ----------")
        number = int(input("Enter car number: "))
        name = input("Enter car name: ")
        brand = input("Enter car brand name: ")
        price = float(input("Enter car price: "))
        engine = input("Enter car engine: ")
        fuel = input("Enter fuel type: ")
        cur.execute(
            """INSERT INTO cars
            VALUES(%s,%s,%s,%s,%s,%s)""",
            (number,name,brand,price,engine,fuel)
        )
        con.commit()
        print("Car added successfully.")
    elif ch == 2:
        print("---------- CAR LIST ----------")
        cur.execute("SELECT * FROM cars")
        data = cur.fetchall()
        if len(data) == 0:
            print("No cars available.")
        else:
            print("Number | Name | Brand | Price | Engine | Fuel")
            for x in data:
                print(
                    x[0],
                    x[1],
                    x[2],
                    x[3],
                    x[4],
                    x[5]
                )
    elif ch == 3:

        print("---------- SEARCH CAR ----------")

        name = input("Enter car name: ")

        cur.execute(
            "SELECT * FROM cars WHERE car_name LIKE %s",
            ("%" + name + "%",)
        )

        data = cur.fetchall()

        if len(data) == 0:

            print("Car not found.")

        else:

            for x in data:

                print("Car Number :",x[0])
                print("Car Name   :",x[1])
                print("Brand Name :",x[2])
                print("Car Price  :",x[3])
                print("Engine     :",x[4])
                print("Fuel Type  :",x[5])
    elif ch == 4:
        print("---------- UPDATE CAR ----------")
        number = int(input("Enter car number: "))
        cur.execute(
            "SELECT * FROM cars WHERE car_number=%s",
            (number,)
        )
        data = cur.fetchone()
        if data is None:
            print("Car not found.")
        else:
            print("1. Car Name")
            print("2. Brand Name")
            print("3. Car Price")
            print("4. Engine")
            print("5. Fuel Type")
            choice = int(input("What do you want to update? "))
            if choice == 1:
                value = input("Enter new car name: ")
                cur.execute(
                    "UPDATE cars SET car_name=%s WHERE car_number=%s",
                    (value,number)
                )
            elif choice == 2:
                value = input("Enter new brand name: ")
                cur.execute(
                    "UPDATE cars SET car_brand_name=%s WHERE car_number=%s",
                    (value,number)
                )
            elif choice == 3:
                value = float(input("Enter new car price: "))
                cur.execute(
                    "UPDATE cars SET car_price=%s WHERE car_number=%s",
                    (value,number)
                )
            elif choice == 4:
                value = input("Enter new engine: ")

                cur.execute(
                    "UPDATE cars SET car_engine=%s WHERE car_number=%s",
                    (value,number)
                )
            elif choice == 5:
                value = input("Enter new fuel type: ")
                cur.execute(
                    "UPDATE cars SET fuel_type=%s WHERE car_number=%s",
                    (value,number)
                )
            else:
                print("Invalid choice.")
                continue
            con.commit()
            print("Car updated successfully.")
    elif ch == 5:
        print("---------- DELETE CAR ----------")
        number = int(input("Enter car number: "))
        cur.execute(
            "SELECT * FROM cars WHERE car_number=%s",
            (number,)
        )
        data = cur.fetchone()
        if data is None:
            print("Car not found.")
        else:
            cur.execute(
                "DELETE FROM cars WHERE car_number=%s",
                (number,)
            )
            con.commit()
            print("Car deleted successfully.")
    elif ch == 6:
        print("---------- SELL CAR ----------")
        number = int(input("Enter car number: "))
        cur.execute(
            "SELECT * FROM cars WHERE car_number=%s",
            (number,)
        )
        data = cur.fetchone()
        if data is None:
            print("Car not found.")
        else:
            print("Car Number :",data[0])
            print("Car Name   :",data[1])
            print("Brand Name :",data[2])
            print("Car Price  :",data[3])
            print("Engine     :",data[4])
            print("Fuel Type  :",data[5])
            confirm = int(input("Enter 1 to confirm sale: "))
            if confirm == 1:
                total = total + data[3]
                cur.execute(
                    "DELETE FROM cars WHERE car_number=%s",
                    (number,)
                )
                con.commit()
                print("Car sold successfully.")
                print("Sold Price :",data[3])
            else:
                print("Sale cancelled.")
    elif ch == 7:
        print("---------- TOTAL ----------")
        cur.execute("SELECT COUNT(*) FROM cars")
        count = cur.fetchone()[0]
        cur.execute("SELECT SUM(car_price) FROM cars")
        stock_total = cur.fetchone()[0]
        if stock_total is None:
            stock_total = 0
        print("Cars Available :",count)
        print("Current Stock Value :",stock_total)
        print("Total Sales :",total)
    elif ch == 8:
        print("Thank you for using KSI Car Showroom Management.")
        break
    else:
        print("Invalid choice.")
cur.close()
con.close()
