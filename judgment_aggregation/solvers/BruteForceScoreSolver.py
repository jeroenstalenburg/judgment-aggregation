from .Solver import Solver
import itertools
import math


class BruteForceScoreSolver(Solver):
    def generate_all_valid_judgments(self):
        """Generate all valid judgments according to the current scenario."""
        var_amount = (self.scenario.auxiliary_amount +
                      self.scenario.issue_amount)
        if self.scenario.collective_constraints == []:
            return map(list, itertools.product([0, 1], repeat=var_amount))
        else:
            first_constraint = self.scenario.collective_constraints[0]
            for judgment in first_constraint.generate_all_valid_judgments():
                valid = True
                for constraint in self.scenario.collective_constraints[1:]:
                    if not constraint.check_judgment(judgment):
                        valid = False
                        break
                if valid:
                    yield judgment

    def solve(self,
              procedure='Kemeny',
              score_fun=None,
              init_fun=None,
              quota=0.5):
        """Solve the judgment aggregation scenario using the given procedure.
        Returns true if at least one answer has been found."""
        if procedure == "quota" or procedure == "majority":
            return self.standard_solve(procedure, quota)
        self.answers = []
        best_score = math.inf
        if score_fun is None:
            score_fun = self.get_score_function(procedure)
        if init_fun is None:
            init_fun = self.get_init_function(procedure)
        init_fun()
        for judgment in self.generate_all_valid_judgments():
            judgment_score = score_fun(judgment[:self.scenario.issue_amount])
            if judgment_score > best_score:
                continue
            elif judgment_score < best_score:
                best_score = judgment_score
                self.answers = [judgment.copy()]
            else:
                self.answers.append(judgment.copy())
        return self.answers != []
