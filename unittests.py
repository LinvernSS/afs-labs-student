import unittest
from api import split_params, get_recipes
import json
import os


class UnitTests(unittest.TestCase):
    def test_split_params(self):
        with self.assertRaises(TypeError) as cm:
            split_params()
        with self.assertRaises(TypeError) as cm:
            split_params(1)
        with self.assertRaises(AttributeError) as cm:
            split_params([[]])
        with self.assertRaises(AttributeError) as cm:
            split_params([['Food']])
        self.assertEqual(split_params(''), [])
        self.assertEqual(split_params('Food'), [['F'], ['o'], ['o'], ['d']])
        self.assertEqual(split_params([]), [])
        self.assertEqual(split_params(['']), [[]])
        self.assertEqual(split_params(['Organic Food', 'Fresh Food', 'Food (Frozen)', 'Pre-Washed Food']),
                         [['Food'], ['Food'], ['Food'], ['Food']])
        self.assertEqual(split_params(['Blackberries']), [['Blackberries']])

    def test_get_recipes(self):
        with self.assertRaises(TypeError) as cm:
            get_recipes()
        with self.assertRaises(TypeError) as cm:
            get_recipes(1)
        with self.assertRaises(TypeError) as cm:
            get_recipes([1])
        with self.assertRaises(TypeError) as cm:
            get_recipes([[1]])
        self.assertEqual(get_recipes([]), [])
        self.assertEqual(get_recipes([['']]), [])
        self.assertIn('Pickled Blackberries', json.dumps(get_recipes([['Blackberries']])))


if __name__ == "__main__":
    log_file = os.environ['LOG_FILE_NAME']
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)
