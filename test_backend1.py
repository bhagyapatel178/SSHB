import unittest 
from unittest.mock import patch
import io
import os 
import sqlite3
from SSH_backend import create_database, fileclear, filefiller, filetodatabase, selectfromdatabase


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

if __name__ == "__main__":
    unittest.main()