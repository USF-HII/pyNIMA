#!/usr/env/bin python

import unittest
from pynima.core import check_mer

class TestMer(unittest.TestCase):
    def test(self):
        # Mother data only
        self.assertEqual(check_mer("DR3", "DR4", "DR3", "DR4", "NA", "NA"), "0")
        self.assertEqual(check_mer("DR3", "DR4", "DR4", "DR4", "NA", "NA"), "0")
        self.assertEqual(check_mer("DR3", "DR3", "DR4", "DR4", "NA", "NA"), "1")
        self.assertEqual(check_mer("DR3", "DR3", "DR3", "DR4", "NA", "NA"), "0")
        self.assertEqual(check_mer("DR3", "DR3", "DR3", "NA", "NA", "NA"), "NA")

        # Father data only
        self.assertEqual(check_mer("DR3", "DR4", "NA", "NA", "DR3", "DR4"), "0")
        self.assertEqual(check_mer("DR3", "DR4", "NA", "NA", "DR4", "DR4"), "0")
        self.assertEqual(check_mer("DR3", "DR3", "NA", "NA", "DR4", "DR4"), "1")
        self.assertEqual(check_mer("DR3", "DR3", "NA", "NA", "DR3", "DR4"), "0")
        self.assertEqual(check_mer("DR3", "DR3", "NA", "NA", "DR3", "NA"), "NA")

        # Partial data from mother and father
        self.assertEqual(check_mer("DR3", "DR3", "DR3", "NA", "NA", "DR3"), "NA")

        # All information from both parents
        self.assertEqual(check_mer("DR3", "DR4", "DR3", "DR4", "DR3", "DR3"), "0")
        self.assertEqual(check_mer("DR3", "DR3", "DR3", "DR3", "DR4", "DR4"), "1")
        self.assertEqual(check_mer("DR3", "DR4", "DR3", "DR4", "DR3", "DR4"), "0")
        self.assertEqual(check_mer("DR3", "DR4", "DR3", "DR3", "DR3", "DR3"), "1")

        # NA value in child
        self.assertEqual(check_mer("NA", "DR3", "DR3", "DR4", "DR3", "DR3"), "NA")

        # NA value in both parents
        self.assertEqual(check_mer("DR3", "DR4", "NA", "NA", "DR3", "NA"), "NA")

if __name__ == '__main__':
    unittest.main()
