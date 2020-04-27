from unittest import TestCase

from ..solvers.BruteForceScoreSolver import BruteForceScoreSolver
from ..data.Scenario import Scenario


class TestBruteForceScoreSolver(TestCase):
    def test_kemeny_slater_solve(self):
        scenario = Scenario()
        scenario.load_file("kemenyslaterdiff.ja")
        solver = BruteForceScoreSolver(scenario)
        solver.solve(procedure="Kemeny")
        self.assertEqual(solver.get_answers(), [[0, 1, 1, 0, 0, 0, 1, 1]])
        solver.solve(procedure="Slater")
        self.assertEqual(solver.get_answers(), [[1, 0, 0, 0, 0, 0, 1, 1]])
