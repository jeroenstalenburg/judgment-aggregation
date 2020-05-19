from unittest import TestCase

from ..data.constraints.CNF import CNF


class TestCNF(TestCase):
    def test_valid_judgment_generation(self):
        cnf = CNF()
        cnf.load_file("notall3.cnf")
        counter = 0
        valids = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0],
                  [1, 0, 1], [1, 1, 0]]
        for sol in cnf.generate_all_valid_judgments():
            self.assertIn(sol, valids)
            counter += 1
        self.assertEqual(counter, 7, "not all valid solutions found")

    def test_check_judgment(self):
        cnf = CNF()
        cnf.load_file("notall3.cnf")
        self.assertFalse(cnf.check_judgment([1, 1, 1]))
        self.assertTrue(cnf.check_judgment([1, 1, 0]))

    def test_larger_file(self):
        cnf = CNF()
        cnf.load_file("large_test.cnf")
        self.assertNotEqual(list(cnf.generate_all_valid_judgments()), [])
