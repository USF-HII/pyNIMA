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
        self.assertEqual(call_nima("DR3","DR3","DR3","DR3","DR3","DR3"), "0") #A1
        self.assertEqual(call_nima("DR3","DR3","DR3","DR3","NA","NA"), "0") #A1M, A2-A1B1M
        self.assertEqual(call_nima("DR4","DR4","DR4","DR4","DR4","DR4"), "0") #C3
        self.assertEqual(call_nima("DR4","DR4","DR4","DR4","NA","NA"), "0") #C3M, C2-A2B2M

        #Child homozygous
        #Mother homozygous same
        #Father heterozgous
        self.assertEqual(call_nima("DR3","DR3","DR3","DR3","DR3","DR4"), "0") #A2-A1B1
        self.assertEqual(call_nima("DR4","DR4","DR4","DR4","DR3","DR4"), "0") #C2-A2B2

        #
        #Child heterozygous, mother homozygous
        #

        #Child heterozygous
        #Mother homozygous
        #Father homozygous (or missing)
        self.assertEqual(call_nima("DR3","DR4","DR3","DR3","DR4","DR4"), "0") #A3
        self.assertEqual(call_nima("DR3","DR4","DR3","DR3","NA","NA"), "0") #A3M, A2-A2B2M
        self.assertEqual(call_nima("DR3","DR4","DR4","DR4","DR3","DR3"), "0") #C1
        self.assertEqual(call_nima("DR3","DR4","DR4","DR4","NA","NA"), "0") #C1M, C2-A1B1M

        #Child heterozygous
        #Mother homozygous
        #Father heterozgous
        self.assertEqual(call_nima("DR3","DR4","DR3","DR3","DR3","DR4"), "0") #A2-A2B2
        self.assertEqual(call_nima("DR3","DR4","DR4","DR4","DR3","DR4"), "0") #C2-A1B1


        #
        #Child homozygous, mother heterozygous
        #

        #Child homozygous
        #Mother heterozygous
        #Father homozgous (or missing)
        self.assertEqual(call_nima("DR3","DR3","DR3","DR4","DR3","DR3"), "DR4") #B1-A1A2
        self.assertEqual(call_nima("DR4","DR4","DR3","DR4","DR4","DR4"), "DR3") #B3-B1B2
        self.assertEqual(call_nima("DR3","DR3","DR3","DR4","NA","NA"), "DR4") #B1-A1A2M, B2-A1M
        self.assertEqual(call_nima("DR4","DR4","DR3","DR4","NA","NA"), "DR3") #B2-B2M, B3-B1B2M

        #Child homozygous
        #Mother heterozygous
        #Father heterozygous
        self.assertEqual(call_nima("DR3","DR3","DR3","DR4","DR3","DR4"), "DR4") #B2-A1
        self.assertEqual(call_nima("DR4","DR4","DR3","DR4","DR3","DR4"), "DR3") #B2-B2

        #
        #Child and mother heterozygous
        #

        #Child heterozygous
        #Mother heterozygous
        #Father homozygous (or missing)
        self.assertEqual(call_nima("DR3","DR4","DR3","DR4","DR3","DR3"), "0") #B1-B1B2
        self.assertEqual(call_nima("DR3","DR4","DR3","DR4","DR4","DR4"), "0") #B3-A1A2
        self.assertEqual(call_nima("DR3","DR4","DR3","DR4","NA","NA"), "0") #B1-B1B2M, B2-A2B1M, B3-A1A2M


        #Child heterozygous
        #Mother heterozygous
        #Father heterozygous
        self.assertEqual(call_nima("DR3","DR4","DR3","DR4","DR3","DR4"), "0") #B2-A2B1


        #
        #Other scenarios
        #

        self.assertEqual(call_nima("DR3","DR3","DR4","DR4","DR3","DR3"), "MEND_ERR")
        self.assertEqual(call_nima("DR3","DR3","DR4","DR4","NA","NA"), "MEND_ERR")

if __name__ == '__main__':
    unittest.main()
