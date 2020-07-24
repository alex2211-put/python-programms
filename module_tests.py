import unittest


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ('string',  1.5)
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = (-1,  -10,  -100)
        for x in cases:
            with self.subTest(x=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        for x, b in (0, (0, )), (1, (1, )):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), b)

    def test_simple_numbers(self):
        for x, b in (3, (3, )), (13, (13, )), (29, (29, )):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), b)

    def test_two_simple_multipliers(self):
        for x, b in (6, (2, 3)), (26, (2, 13)), (121, (11, 11)):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), b)

    def test_many_multipliers(self):
        for x, t in (1001, (7, 11, 13)), (9699690, (2, 3, 5, 7, 11, 13, 17, 19)):
            with self.subTest(x=x):
                self.assertEqual(factorize(x), t)
