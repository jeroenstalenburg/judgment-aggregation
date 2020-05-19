from unittest import TestCase

from ..solvers.ASPSolver import ASPSolver
from ..data.Scenario import Scenario


class TestBruteForceScoreSolver(TestCase):
    def test_kemeny_slater_solve(self):
        scenario = Scenario()
        scenario.load_file("kemenyslaterdiff.ja")
        solver = ASPSolver(scenario)
        solver.solve(procedure="Kemeny")
        self.assertEqual(solver.get_answers(), [[0, 1, 1, 0, 0, 0, 1, 1]])
        solver.solve(procedure="kemeny-opt1")
        self.assertEqual(solver.get_answers(), [[0, 1, 1, 0, 0, 0, 1, 1]])
        solver.solve(procedure="kemeny-opt2")
        self.assertEqual(solver.get_answers(), [[0, 1, 1, 0, 0, 0, 1, 1]])
        solver.solve(procedure="kemeny-opt3")
        self.assertEqual(solver.get_answers(), [[0, 1, 1, 0, 0, 0, 1, 1]])
        solver.solve(procedure="Slater")
        self.assertEqual(solver.get_answers(), [[1, 0, 0, 0, 0, 0, 1, 1]])
