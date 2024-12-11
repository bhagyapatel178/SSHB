import unittest 
from unittest.mock import patch, MagicMock 
import io
import os 
import sqlite3
from SSH_backend1 import create_database, fileclear, filefiller, filetodatabase, selectfromdatabase, viewbasket 


class TestBackendFunction(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_SSHDB_test.db"
        create_database(self.test_db)
        filefiller()
        filetodatabase(self.test_db)
        self.connection = sqlite3.connect(self.test_db)

    def tearDown(self):
        self.connection.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_tables_created(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]
        expected_tables = ["households", "order_items", "products", "students", "supermarkets"]
        self.assertCountEqual(tables, expected_tables, "All tables should be created")


    def test_file_filler(self):
        """Test if API.txt is filled with dummy data."""
        filefiller()
        with open("API.txt", "r") as file:
            lines = file.readlines()
        self.assertGreater(len(lines), 0, "API.txt should contain data")
        for line in lines:
            self.assertRegex(line, r"^\d+,.+,\d+\.\d{2},[01],\d+$", "Each line should match the expected format")

    def test_file_to_database(self):
        """Test if data from the file is inserted into the database."""
        filefiller()  # Fill API.txt with data
        filetodatabase(self.test_db)  # Insert data into the database
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        self.assertGreater(product_count, 0, "Products table should contain data after filetodatabase")

    
    def test_selectfromdatabase_getall(self):
        """Test if all products are retrieved when productname='getall'."""
        connection = sqlite3.connect(self.test_db)
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM products;")
        total_products = cursor.fetchone()[0]
        connection.close()

        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
           selectfromdatabase("getall", 0)  
           printed_output = fake_stdout.getvalue()

        printed_lines = printed_output.strip().split("\n")

        self.assertEqual(len(printed_lines), total_products)

class TestViewBasket(unittest.TestCase):
    @patch("sqlite3.connect")  # Mock sqlite3.connect
    def test_viewbasket(self, mock_connect):
        # Define mock data to be returned by the database query
        mock_results = [
            (1, "Apple", 1.5, "SuperMart"),
            (2, "Banana", 0.8, "QuickShop"),
        ]

        # Set up mock connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_results
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Call the function with a test household_id
        household_id = 123
        basket = viewbasket(household_id)

        # Assert the query was executed with the correct parameter
        mock_cursor.execute.assert_called_once_with(
            """SELECT 
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
""",
            (household_id,),
        )

        # Assert the basket contains the correct flattened results
        expected_basket = [1, "Apple", 1.5, "SuperMart", 2, "Banana", 0.8, "QuickShop"]
        self.assertEqual(basket, expected_basket)

        # Assert that the connection is closed
        mock_connection.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()