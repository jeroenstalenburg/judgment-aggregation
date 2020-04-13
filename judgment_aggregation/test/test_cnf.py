from unittest import TestCase

from ..data.constraints.CNF import CNF


class TestCNF(TestCase):
    def test_create_cnf(self):
        cnf = CNF()
        cnf.load_file("notall3.cnf")
        self.assertIsNotNone(cnf, "Creation of CNF constraint failed")

    def test_valid_agenda_generation(self):
        cnf = CNF()
        cnf.load_file("notall3.cnf")
        self.assertEqual(list(cnf.generate_all_valid_agendas()),
                         [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                          [1, 0, 0], [1, 0, 1], [1, 1, 0]])
