import unittest

from horner_calculator import evaluate_direct, evaluate_horner


class PolynomialEvaluationTests(unittest.TestCase):
    def test_textbook_example(self):
        coefficients = [2, -3, 1, -4, 7, 8]
        horner, _ = evaluate_horner(coefficients, 2)
        direct, _ = evaluate_direct(coefficients, 2)
        self.assertEqual(horner, 30)
        self.assertEqual(direct, 30)

    def test_decimal_values_match(self):
        coefficients = [0.5, -1.2, 3.4, 0, -2, 7.1]
        horner, _ = evaluate_horner(coefficients, -1.5)
        direct, _ = evaluate_direct(coefficients, -1.5)
        self.assertAlmostEqual(horner, direct, places=10)


if __name__ == "__main__":
    unittest.main()
