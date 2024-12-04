import unittest 
import os 
import sqlite3
from SSH_backend1 import create_database, fileclear, filefiller, filetodatabase, selectfromdatabase


class TestDatabaseSetup(unittest.TestCase):
    def setUp(self):
        self.test_db = "test_SSHDB_test.db"
        create_database(self.test_db)
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

    

if __name__ == "__main__":
    unittest.main()