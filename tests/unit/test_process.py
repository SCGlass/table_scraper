import unittest
import pandas as pd
from process import PortCleaner

class TestPortCleaner(unittest.TestCase):

    def setUp(self):
        # Load test data from CSV for testing
        self.test_data = pd.read("tests/unit/se_sweden.csv")
        self.port_cleaner = PortCleaner(self.test_data)

    def test_format_table(self):
        formatted_data = PortCleaner.format_table(self.test_data)

        # check column names
        expected_columns = ["Country_code",
                            "Location_code",
                            "Name",
                            "NameWoDiacritics",
                            "Status",
                            "Latitude",
                            "Longitude"]
        self.assertEqual(list(formatted_data.columns), expected_columns)