from unittest import TestCase
import os
import sys
from server import app
from model import connect_to_db, db, example_data

current = os.getcwd()
current = current.split("/")
current = "/".join(current[:-1])
sys.path.append(current)


class FlaskTests(TestCase):

    def setUp(self):
        """Before tests."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database
        connect_to_db(app)

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """For after test."""

        db.session.close()
        db.drop_all()

    def test_register(self):
        """Register test user"""

        result = self.client.post("/register",
                                  data={"first_name": "Jane",
                                        "last_name": "Doe",
                                        "email": "jane@gmail.com",
                                        "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"Registration successful!", result.data)

    def test_login(self):
        """Test login functionality"""

        login = self.client.post("/login",
                                 data={"email": "Jane@jane.com", "password": "password"},
                                 follow_redirects=True)
        self.assertIn(b"Success", login.data)
        logged_in = self.client.get("/products")
        self.assertIn(b"Account", logged_in.data)
        self.assertIn(b"Log Out", logged_in.data)

        logout = self.client.get("/logout", follow_redirects=True)
        self.assertNotIn(b"Account", logout.data)
        self.assertIn(b"Login", logout.data)

    def test_frontpage(self):
        """Test static frontpage"""

        result = self.client.get("/")

        self.assertIn(b"Enter", result.data)

    def test_all_products(self):
        """Test products listings"""

        result = self.client.get("/products")

        self.assertIn(b"Add to Cart</button>", result.data)

    def test_product_page(self):
        """Test individual product page"""

        result = self.client.get("/products/1")

        self.assertIn(b"Blackberries", result.data)

    def test_cart_page(self):
        """Test cart page"""

        result = self.client.get("/cart")

        self.assertIn(b"Shopping Cart", result.data)

    def test_locations(self):
        """Test locations page"""

        result = self.client.get("/locations")

        self.assertIn(b'<div id="map">', result.data)

    def test_search(self):
        """Test search functionality"""

        result = self.client.get("/search?terms=black")

        self.assertIn(b"Organic Blackberries", result.data)


if __name__ == "__main__":
    import unittest

    log_file = 'log_file.txt'
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
