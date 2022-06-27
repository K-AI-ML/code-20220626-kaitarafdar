import unittest
import pandas as pd
import os
from bmi_calc import BmiClassifier


class TestBmiCalc(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        self.bmi_data = 'bmi_data.json'
        self.df = pd.read_json(self.bmi_data)
        self.bmi_classifier = BmiClassifier(self.bmi_data)
        self.bmi_catergories = [
            'Overweight',
            'Moderately obese',
            'Severely obese',
            'Very severely obese'
        ]

    def test_file_exists(self):
        '''Checks if file exists.'''

        check_file = os.path.exists(self.bmi_data)
        self.assertTrue(check_file, f"File '{self.bmi_data}' does not exist.")

    def test_file_accessible(self):
        '''Checks if file is accessible.'''

        check_access = os.access(self.bmi_data, os.R_OK)
        self.assertTrue(check_access, f"File '{self.bmi_data}' not accessible.")

    def test_columns_present(self):
        '''checks that the expected columns are present'''

        self.assertIn("Gender", self.df.columns)
        self.assertIn("HeightCm", self.df.columns)
        self.assertIn("WeightKg", self.df.columns)

    def test_non_empty(self):
        """checks that table is populated"""

        self.assertNotEqual(self.df.shape[0], 0)

    def test_cat_frequency(self):
        '''Test that it can derive the correct count.'''

        bmi_categories = ['Overweight', 'Moderately obese', 'Severely obese', 'Very severely obese']
        result = self.bmi_classifier.get_category_frequency(bmi_categories)

        self.assertEqual(result, 4, "incorrect frequency")

    def test_bad_type(self):
        '''Test that it provides error message with wrong input type'''

        bmi_categories = 1
        with self.assertRaises(TypeError):
            result = self.bmi_classifier.get_category_frequency(bmi_categories)


if __name__ == '__main__':
    import timeit
    timing = timeit.timeit("BmiClassifier('bmi_data.json')", setup="from __main__ import BmiClassifier", number=100)
    print(f'App has taken {timing} seconds to run')
    unittest.main()
