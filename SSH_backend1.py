import sqlite3
import random

def create_database(db_name="SSHDB.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Create households table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS households (
            household_id INTEGER PRIMARY KEY NOT NULL,
            address TEXT NOT NULL
        )
    """)

    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER PRIMARY KEY NOT NULL,
            student_id INTEGER NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER,
            added_at TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """)

    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY NOT NULL,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            availability BOOLEAN,
            supermarket_id INTEGER NOT NULL,
            FOREIGN KEY (supermarket_id) REFERENCES supermarkets(supermarket_id)
        )
    """)

    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY NOT NULL,
            student_name TEXT NOT NULL,
            household_id INTEGER NOT NULL,
            email TEXT UNIQUE NOT NULL,
            FOREIGN KEY (household_id) REFERENCES households(household_id)
        )
    """)

    # Create supermarkets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supermarkets (
            supermarket_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT
        )
    """)

    connection.commit()
    connection.close()
def fileclear(): #clears API file

    with open("API.txt", "w"):
        pass
def filefiller(): #fills file with dummy data
    #list of potential items
    shopping_items = ["Apples", "Bananas", "Bread", "Milk", "Eggs", "Chicken breast", "Rice", "Pasta", "Canned tomatoes", "Carrots", "Potatoes", "Butter", "Cheese", "Coffee", "Sugar", "Olive oil", "Cereal", "Lettuce", "Yogurt", "Toilet paper"]
    with open("API.txt", "a") as file:
        fileclear()  # Clear the file before filling it
        for supermarke in range(3): #items from three shops
            for i in range(len(shopping_items)):
                productid = str((i+1)+(100*supermarke))
                productname = shopping_items[i]
                price = f"{round(random.uniform(0.5, 4), 2):.2f}"
                availability = '0' if random.randint(0, 10) > 9 else '1'
                file.write(productid + "," + productname + "," + str(price) + "," + availability + "," + str(supermarke + 1) + "\n") #writes data in the form: id,name,price,availability,supermarketid

def filetodatabase(db_name="SSHDB.db"):
    connection = sqlite3.connect(db_name) #connecting to the DB
    cursor = connection.cursor() #tool to navigate DB


    cursor.execute("DELETE FROM products") #clearing old data to then put in updated figures

    with open("API.txt", 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                product_id, product_name, price, availability, supermarket_id = line.split(',')
                product_id = int(product_id)
                price = float(price)
                availability = int(availability)
                supermarket_id = int(supermarket_id)

                cursor.execute("""
                    INSERT INTO products (product_id, product_name, price, availability, supermarket_id)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, product_name, price, availability, supermarket_id))

    connection.commit()
    connection.close()

    
def selectfromdatabase(productname, shop): #all products: productname = "getall" #all shops: shop = 0
    connection = sqlite3.connect("SSHDB.db") #connecting to DB
    cursor = connection.cursor() #tool to navigate DB
    if productname == "getall":
        if shop == 0:
            query = "SELECT * FROM products"
            cursor.execute(query)
        else:
            query = "SELECT * FROM products where supermarket_id = ?"
            cursor.execute(query, (shop,))
    elif shop == 0:
        query = "SELECT * FROM products WHERE product_name LIKE ?"
        cursor.execute(query, (f"%{productname}%",))
    else:
        query = "SELECT * FROM products WHERE product_name LIKE ? AND supermarket_id = ?"
        cursor.execute(query, (f"%{productname}%", shop))

    result = cursor.fetchall()
    connection.close()
    for item in result:
        name = item[1]
        price = item[2]
        availability = item[3]
        print(f"Product: {name}, Price: {price}, Available: {availability}")

create_database()  # Create the database with all necessary tables
filefiller()  # Fill the API.txt with sample data
filetodatabase()  # Insert data from API.txt into database
selectfromdatabase("chees", 0)  # Query data from the database
