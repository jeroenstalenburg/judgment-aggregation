from unittest import TestCase
from ..data.Scenario import Scenario


class TestScenario(TestCase):
    def test_creating_scenario(self):
        s = Scenario()
        s.load_file("kemenyslaterdiff.ja")
        s.solve('ASP')
        self.assertEqual(s.collective_judgments, [[0, 1, 1, 0, 0, 0, 1, 1]])
