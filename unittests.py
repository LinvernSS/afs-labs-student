import unittest
import flask
import api
import functions
import model
import server


class TestName(unittest.TestCase):

    def setUp(self):
        """Method to prepare the test fixture. Run BEFORE the test methods."""
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        # Connect to test database
        model.connect_to_db(server.app)

        # Create tables and add sample data
        model.db.create_all()
        model.example_data()
        self.cart = model.Product.query.filter(model.Product.product_id.in_(flask.session['cart'].keys())).all()
        pass

    def tearDown(self):
        """Method to tear down the test fixture. Run AFTER the test methods."""
        model.db.session.close()
        model.db.drop_all()
        pass

    def testAPI(self):
        self.assertEqual(api.split_params([]), [])
        self.assertEqual(api.split_params(['']), [[]])
        self.assertEqual(api.split_params(['Organic Food', 'Fresh Food', 'Food (Frozen)', 'Pre-Washed Food']),
                         [['Food'], ['Food'], ['Food'], ['Food']])
        self.assertEqual(api.split_params([item.name for item in self.cart]), [['Blackberries']])

        self.assertEqual(api.get_recipes([]), [])
        self.assertEqual(api.get_recipes([['']]), [])
        self.assertIn('Pickled Blackberries', api.get_recipes([['Blackberries']]))

    def testFunctions(self):
        self.assertEqual(functions.get_cart_weight(self.cart), 6)
        self.assertEqual(functions.get_cart_total(self.cart), 3.99)

    def testServer(self):
        result = self.client.get('/register')
        self.assertIn(b'register_img', result.data)

        result = self.client.post('/products/1', data={'productID': '1'}, follow_redirects=True)
        self.assertIn(b'Blackberries', result.data)

        result = self.client.get('/account')
        self.assertIn(b'Jane Doe', result.data)

        result = self.client.post('/cart',
                                  data={'delivery': 'delivery',
                                        'address': {'street': '1234 Main Street',
                                                    'zipcode': '31626'}},
                                  follow_redirects=True)
        self.assertIn(b'Success', result.data)

        result = self.client.post('/save-recipe',
                                  data={'url': 'http://foodandstyle.com/2012/12/20/persimmon-cosmopolitan/'},
                                  follow_redirects=True)
        self.assertIn(b'Success', result.data)

        result = self.client.get('/checkout')
        self.assertIn(b'Thank you', result.data)

        result = self.client.post('/checkout')
        self.assertIn(b'Your order has been placed!', result.data)

        result = self.client.post('/add-item', data={'product_id': 1}, follow_redirects=True)
        self.assertIn(b'Success!', result.data)

        result = self.client.post('/update-cart', data={'product_id': 1, 'qty': 3})
        self.assertIn(b'Success', result.data)


if __name__ == "__main__":
    log_file = 'log_file.txt'
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
