import sqlite3
import random
import socket
import threading
import json

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
            availability INTEGER,
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
            email TEXT NOT NULL,
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
                productid = (i+1)+(100*supermarke)
                productname = shopping_items[i]
                price = float(str(random.uniform(0.5, 4))[:4])
                availability = random.randint(0,200)
                file.write(str(productid) + "," + productname + "," + str(price) + "," + str(availability) + "," + str(supermarke + 1) + "\n") #writes data in the form: id,name,price,availability,supermarketid

def filetodatabase(db_name="SSHDB.db"):
    connection = sqlite3.connect(db_name) #connecting to the DB
    cursor = connection.cursor() #tool to navigate DB


    cursor.execute("DELETE FROM products") #clearing old data to then put in updated figures
    cursor.execute("DELETE FROM supermarkets")
    cursor.execute("INSERT INTO supermarkets (supermarket_id, name) VALUES(1,'A')")
    cursor.execute("INSERT INTO supermarkets (supermarket_id, name) VALUES(2,'B')")
    cursor.execute("INSERT INTO supermarkets (supermarket_id, name) VALUES(3,'C')")

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
    returnarr = []
    for item in result:
        name = item[1]
        price = item[2]
        availability = item[3]
        store = item[4]
        returnarr.append([name,price,availability,store])
    return returnarr

def setup():
    create_database()
    filefiller()
    filetodatabase()

def add(arr, student_id):
    product_name, price, quantity, shopname = eval(arr)
    connection = sqlite3.connect("SSHDB.db") #connecting to the DB
    cursor = connection.cursor()
    query = """
        SELECT product_id FROM products WHERE product_name = ? AND supermarket_id = ?
    """
    cursor.execute(query, (product_name,shopname,))
    result = cursor.fetchall()
    if result is None:
        print("error: product not found in database")

    product_id = result[0]
    query = """
        INSERT INTO order_items (student_id, price, quantity, product_id)
        VALUES (?, ?, ?, ?) 
    """
    cursor.execute(query, (student_id, price, quantity, product_id[0],))
    connection.commit()
    connection.close()
    
def basket():
    print("basket function")
    
def studentfunc(studentno,houseno):
    connection = sqlite3.connect("SSHDB.db") #connecting to the DB
    cursor = connection.cursor() #tool to navigate DB
    query = "SELECT * FROM students where student_id = ?"
    cursor.execute(query, (studentno,))
    result = cursor.fetchall()
    if len(result) == 0:
        cursor.execute("""INSERT INTO students (student_id, student_name, household_id, email)
                    VALUES (?, ?, ?, ?)
                """, (studentno, "dummyfornow", houseno, "Example@gmail.com"))
        connection.commit()
    else:
        print("DOES WORK")
    connection.close()
    
def viewbasket(household_id):
    connection = sqlite3.connect("SSHDB.db") #connecting to the DB
    cursor = connection.cursor()
    query = """SELECT 
    students.student_id,
    products.product_name,
    products.price,
    supermarkets.name AS shop_name
FROM 
    students
JOIN 
    order_items ON students.student_id = order_items.student_id
JOIN 
    products ON order_items.product_id = products.product_id
JOIN 
    supermarkets ON products.supermarket_id = supermarkets.supermarket_id
WHERE 
    students.household_id = ?;
"""
    cursor.execute(query, (household_id,))
    results = cursor.fetchall()
    print(results)
    basket = [item for row in results for item in row]
    connection.close()
    return basket

def findfunction(client_message, conn):
    command, rest = client_message.split(',',1)
    
    try:
        if command == "selectfromdatabase":
            name, shop = rest.split(',',1)
            basket = selectfromdatabase(name,int(shop))
            response = json.dumps(basket)
            conn.sendall(response.encode())
        if command == "studentfunc":
            stno, hno = rest.split(',',1)
            studentfunc(stno,hno)
        if command == 'add':
            array, sid = rest.split('!',1)
            add(array,sid)
        if command == 'viewbasket':
            stdt_id, hh_id = rest.split('!',1)
            basket = viewbasket(hh_id)
            response = json.dumps(basket)
            conn.sendall(response.encode())
    except:
        print("function not found")

shared_data = {"updates": []}
lock = threading.Lock()

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    try:
        while True:
            data = conn.recv(1024)  # Receive data from the client
            if not data:
                break
            message = data.decode()
            print(f"Received from {addr}: {message}")
            findfunction(message,conn)
            # Update shared data with thread-safe access
            with lock:
                shared_data["updates"].append((addr, message))
            conn.sendall(f"Message received: {message}".encode())
    except ConnectionResetError:
        print(f"Connection with {addr} closed unexpectedly.")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def start_server():
    host = '127.0.0.1'
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)  # Allow up to 5 queued connections
    print(f"Server listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

if __name__ == "__main__":
    setup()
    start_server()
