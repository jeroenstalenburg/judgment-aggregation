from unittest import TestCase

from ..data.Scenario import Scenario


class TestScenario(TestCase):
    def test_creating_scenario(self):
        s = Scenario()
        print(s.path)
        s.load_file("notall3.ja")
        # self.assertTrue(False)