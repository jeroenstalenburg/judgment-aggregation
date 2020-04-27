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

    def solve(self, procedure=None, score_fun=None):
        """Solve the scenario, store the answers in self.answers and return
        True when a solution (not necessarily consistent) has been found"""
        raise NotImplementedError()

    def get_score_function(self, procedure):
        """Get the correct python score function depending on the given
        procedure"""
        if procedure == 'Kemeny' or procedure == 'Slater':
            return lambda agenda: np.sum(self.score_vector * agenda)
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
        agendas, voters_per_agenda = self.scenario.get_agendas()
        print(np.array(agendas).T @ voters_per_agenda)
        self.score_vector = -(np.array(agendas).T @ voters_per_agenda
                              ) + np.sum(voters_per_agenda) / 2

    def slater_init(self):
        """Set the score vector to be the correct score vector for the
        Kemeny procedure"""
        agendas, voters_per_agenda = self.scenario.get_agendas()
        self.score_vector = -np.array(self.get_majority_agenda()) + 0.5

    def get_quota_rule_agenda(self, quota, proportional_quota=False):
        """Get the agenda according to the quota rule for the current scenario.
        The quota rule states that a variable/issue is true when at least
        _quota_ voters think it is true.
        If proportional_quota is True, then _quota_ is expected to be a
        proportion between 0 and 1 of the voters to be True."""
        agendas, voters_per_agenda = self.scenario.get_agendas()
        if proportional_quota:
            quota = quota * np.sum(voters_per_agenda)
        return list(map(int, np.array(agendas).T @ voters_per_agenda >= quota))

    def get_majority_agenda(self):
        """Get the majority agenda for the current scenario.
        The majority rule is the same as the quota rule with 50% needed for a
        variable/issue to be True."""
        return self.get_quota_rule_agenda(0.5, proportional_quota=True)

    def get_answers(self):
        """Return the found answers."""
        return self.answers

    def generate_answers(self):
        """Generate the answers found by the solve function."""
        for answer in self.get_answers():
            yield answer
