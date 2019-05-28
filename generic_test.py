"""
Tests for the 'generic' module
"""
import unittest

import generic

class TestGenericTypes(unittest.TestCase):
    def test_int(self):
        """
        Test fixture for generic.Int
        """
        a = generic.Int(0, 10)
        b = generic.Int(0, 10)
        c = a.crossover(b)
        self.assertTrue(isinstance(c, generic.Int))
        self.assertTrue(c.low < c.generate() < c.high)
        d = c.mutation()
        self.assertTrue(isinstance(d, generic.Int))
        self.assertTrue(d.low < d.generate() < d.high)

    def test_float(self):
        """
        Test fixture for generic.Float
        """
        a = generic.Float(-10, 10)
        b = generic.Float(-10, 10)
        c = a.crossover(b)
        self.assertTrue(isinstance(c, generic.Float))
        self.assertTrue(c.low < c.generate() < c.high)
        d = c.mutation()
        self.assertTrue(isinstance(d, generic.Float))
        self.assertTrue(d.low < d.generate() < d.high)

    def test_string(self):
        """
        Test fixture for generic.Float
        """
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        symbols = '{}()[].,:;+-*/&|<>=~$'
        a = generic.String(1,10,ascii_lowercase)
        b = generic.String(1,10,ascii_uppercase)
        c = a.crossover(b)
        self.assertTrue(isinstance(c, generic.String))
        self.assertTrue(c.low <= len(c.generate()) <= c.high)
        d = c.mutation()
        self.assertTrue(isinstance(d, generic.String))
        self.assertTrue(d.low <= len(d.generate()) <= d.high)

    #TODO(@anuartb, @azamat7) add more tests for Dict, String

if __name__ == '__main__':
    unittest.main()