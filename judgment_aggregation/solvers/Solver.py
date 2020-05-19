import numpy as np
from ..JAError import JAError


class Solver:
    def __init__(self, scenario=None):
        if scenario is not None:
            self.set_scenario(scenario)

    def set_scenario(self, scenario):
        """Set the scenario for the solver."""
        self.scenario = scenario
        self.answers = []
        self.score_vector = np.array([])

    def solve(self,
              procedure='Kemeny',
              score_fun=None,
              init_fun=None,
              quota=0.5):
        """Solve the scenario, store the answers in self.answers and return
        True when a solution (not necessarily consistent) has been found"""
        if procedure == "quota" or procedure == "majority":
            return self.standard_solve(procedure, quota)
        else:
            raise NotImplementedError()

    def standard_solve(self, procedure, quota=0.5):
        """Solve for the two standard procedures, quota and majority
        (these procedures do not require """
        if procedure == "quota":
            return self.get_quota_rule_judgment(quota)
        elif procedure == "majority":
            return self.get_majority_judgment()

    def get_score_function(self, procedure):
        """Get the correct python score function depending on the given
        procedure"""
        if procedure == 'Kemeny' or procedure == 'Slater':
            return lambda judgment: np.sum(self.score_vector * judgment)
        else:
            raise JAError("No score function given and/or "
                          "given procedure '%s' is not a "
                          "valid procedure" % procedure)

    def get_init_function(self, procedure):
        """Get the correct python init function depending on the given
        procedure"""
        if procedure == 'Kemeny':
            return self.kemeny_init
        elif procedure == 'Slater':
            return self.slater_init
        else:
            raise JAError("No init function given and/or "
                          "given procedure '%s' is not a "
                          "valid procedure" % procedure)

    def kemeny_init(self):
        """Set the score vector to be the correct score vector for the
        Kemeny procedure"""
        judgments, judges_per_judgment = self.scenario.get_judgments()
        self.score_vector = -(np.array(judgments).T @ judges_per_judgment
                              ) + np.sum(judges_per_judgment) / 2

    def slater_init(self):
        """Set the score vector to be the correct score vector for the
        Kemeny procedure"""
        judgments, judges_per_judgment = self.scenario.get_judgments()
        self.score_vector = -np.array(self.get_majority_judgment()) + 0.5

    def get_quota_rule_judgment(self, quota):
        """Get the judgment according to the quota rule for the current scenario.
        The quota rule states that a variable/issue is true when at least
        _quota_ judges think it is true.
        If proportional_quota is True, then _quota_ is expected to be a
        proportion between 0 and 1 of the judges to be True."""
        judgments, judges_per_judgment = self.scenario.get_judgments()
        if type(quota) == float:
            quota = quota * np.sum(judges_per_judgment)
        return list(
            map(int,
                np.array(judgments).T @ judges_per_judgment >= quota))

    def get_majority_judgment(self):
        """Get the majority judgment for the current scenario.
        The majority rule is the same as the quota rule with 50% needed for a
        variable/issue to be True."""
        return self.get_quota_rule_judgment(0.5)

    def get_answers(self):
        """Return the found answers."""
        return self.answers

    def generate_answers(self):
        """Generate the answers found by the solve function."""
        for answer in self.get_answers():
            yield answer
