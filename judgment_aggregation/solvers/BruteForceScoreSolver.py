from .Solver import Solver
import itertools
import math


class BruteForceScoreSolver(Solver):
    def generate_all_valid_agendas(self):
        """Generate all valid agendas according to the current scenario."""
        var_amount = (self.scenario.auxiliary_amount +
                      self.scenario.issue_amount)
        if self.scenario.collective_constraints == []:
            return map(list, itertools.product([0, 1], repeat=var_amount))
        else:
            first_constraint = self.scenario.collective_constraints[0]
            for agenda in first_constraint.generate_all_valid_agendas():
                valid = True
                for constraint in self.scenario.collective_constraints[1:]:
                    if not constraint.check_agenda(agenda):
                        valid = False
                        break
                if valid:
                    yield agenda

    def solve(self, procedure='Kemeny', score_fun=None, init_fun=None):
        """Solve the judgment aggregation scenario using the given procedure.
        Returns true if at least one answer has been found."""
        self.answers = []
        best_score = math.inf
        if score_fun is None:
            score_fun = self.get_score_function(procedure)
        if init_fun is None:
            init_fun = self.get_init_function(procedure)
        init_fun()
        for agenda in self.generate_all_valid_agendas():
            agenda_score = score_fun(agenda[:self.scenario.issue_amount])
            if agenda_score > best_score:
                continue
            elif agenda_score < best_score:
                best_score = agenda_score
                self.answers = [agenda.copy()]
            else:
                self.answers.append(agenda.copy())
        return self.answers != []
