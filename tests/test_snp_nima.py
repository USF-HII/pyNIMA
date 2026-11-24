#!/usr/env/bin python

import unittest
from pynima.core import call_nima

class TestStringMethods(unittest.TestCase):
    def test(self):

        #
        #Child and mother homozygous
        #

        #Child homozygous
        #Mother homozygous same
        #Father homozygous same (or missing)
        self.assertEqual(call_nima("C","C","C","C","C","C"), "0") #A1
        self.assertEqual(call_nima("C","C","C","C","NA","NA"), "0") #A1M, A2-A1B1M
        self.assertEqual(call_nima("T","T","T","T","T","T"), "0") #C3
        self.assertEqual(call_nima("T","T","T","T","NA","NA"), "0") #C3M, C2-A2B2M

        #Child homozygous
        #Mother homozygous same
        #Father heterozgous
        self.assertEqual(call_nima("C","C","C","C","C","T"), "0") #A2-A1B1
        self.assertEqual(call_nima("T","T","T","T","C","T"), "0") #C2-A2B2

        #
        #Child heterozygous, mother homozygous
        #

        #Child heterozygous
        #Mother homozygous
        #Father homozygous (or missing)
        self.assertEqual(call_nima("C","T","C","C","T","T"), "0") #A3
        self.assertEqual(call_nima("C","T","C","C","NA","NA"), "0") #A3M, A2-A2B2M
        self.assertEqual(call_nima("C","T","T","T","C","C"), "0") #C1
        self.assertEqual(call_nima("C","T","T","T","NA","NA"), "0") #C1M, C2-A1B1M

        #Child heterozygous
        #Mother homozygous
        #Father heterozgous
        self.assertEqual(call_nima("C","T","C","C","C","T"), "0") #A2-A2B2
        self.assertEqual(call_nima("C","T","T","T","C","T"), "0") #C2-A1B1


        #
        #Child homozygous, mother heterozygous
        #

        #Child homozygous
        #Mother heterozygous
        #Father homozgous (or missing)
        self.assertEqual(call_nima("C","C","C","T","C","C"), "T") #B1-A1A2
        self.assertEqual(call_nima("T","T","C","T","T","T"), "C") #B3-B1B2
        self.assertEqual(call_nima("C","C","C","T","NA","NA"), "T") #B1-A1A2M, B2-A1M
        self.assertEqual(call_nima("T","T","C","T","NA","NA"), "C") #B2-B2M, B3-B1B2M

        #Child homozygous
        #Mother heterozygous
        #Father heterozygous
        self.assertEqual(call_nima("C","C","C","T","C","T"), "T") #B2-A1
        self.assertEqual(call_nima("T","T","C","T","C","T"), "C") #B2-B2

        #
        #Child and mother heterozygous
        #

        #Child heterozygous
        #Mother heterozygous
        #Father homozygous (or missing)
        self.assertEqual(call_nima("C","T","C","T","C","C"), "0") #B1-B1B2
        self.assertEqual(call_nima("C","T","C","T","T","T"), "0") #B3-A1A2
        self.assertEqual(call_nima("C","T","C","T","NA","NA"), "0") #B1-B1B2M, B2-A2B1M, B3-A1A2M


        #Child heterozygous
        #Mother heterozygous
        #Father heterozygous
        self.assertEqual(call_nima("C","T","C","T","C","T"), "0") #B2-A2B1


        #
        #Other scenarios
        #

        self.assertEqual(call_nima("C","C","T","T","C","C"), "MEND_ERR")
        self.assertEqual(call_nima("C","C","T","T","NA","NA"), "MEND_ERR")

if __name__ == '__main__':
    unittest.main()
