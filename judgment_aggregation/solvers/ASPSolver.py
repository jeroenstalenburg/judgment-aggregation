from .Solver import Solver
from .ASPConstants import BASIC_JA_ASP, ASP_PROCEDURES


class ASPSolver(Solver):
    """Solve the scenario using ASP (Answer Set Programming).
    Implementation for the inner workings of the ASP model largely taken from:
    https://github.com/rdehaan/ja-asp"""
    def __init__(self, scenario):
        """Encode the scenario to an ASP scenario"""
        super().__init__(scenario)
        # TODO check for/transform to CNF data constraints
        constraints = self.scenario.collective_constraints
        self.encoded_scenario = BASIC_JA_ASP
        # Add all issues from the current scenario
        self.encoded_scenario += "issue(" + ";".join(
            ['i' + str(i + 1)
             for i in range(self.scenario.issue_amount)]) + ").\n"
        # Add all auxiliary issues from the current scenario
        self.encoded_scenario += "aux(" + ";".join([
            'i' + str(i + 1 + self.scenario.issue_amount)
            for i in range(self.scenario.auxiliary_amount)
        ] + ['aux_dummy']) + ").\n"
        # Add all clauses from the current scenario
        clause_strings = []
        clause_amount = 1
        for CNF in constraints:
            clause_strings += [
                "clause(" + str(c + clause_amount) + ",(" + ';'.join([
                    '-i' + str(-disj) if disj < 0 else 'i' + str(disj)
                    for disj in clause
                ]) + ")).\n" for c, clause in enumerate(CNF.clauses)
            ]
            clause_amount += CNF.clause_amount
        self.encoded_scenario += "".join(clause_strings)
        # Add individual judges (as voters) and their judgment sets (js)
        self.encoded_scenario += "voter(1..%s).\n" % self.scenario.judge_amount
        judge_counter = 1
        for judgment, judges in zip(self.scenario.individual_judgments,
                                    self.scenario.judges_per_judgment):
            self.encoded_scenario += "js(%s..%s, (" % (
                judge_counter, judge_counter - 1 + judges) + ';'.join([
                    'i' + str(iss + 1) if opin else '-i' + str(iss + 1)
                    for iss, opin in enumerate(judgment)
                ]) + ")).\n"
            judge_counter += judges

    def solve(self,
              procedure='Kemeny',
              score_fun=None,
              init_fun=None,
              quota=0.5):
        """Solve the judgment aggregation scenario using the given procedure.
        Returns true if at least one answer has been found."""
        if procedure == "quota" or procedure == "majority":
            return self.standard_solve(procedure, quota)
        import clingo
        self.answers = []
        asp_program = self.encoded_scenario

        if procedure == "Kemeny":
            procedure = "kemeny-opt1"
        if procedure == "Slater":
            procedure = "slater"
        asp_procedure = ASP_PROCEDURES[procedure]

        control = clingo.Control()
        control.add("base", [], asp_program + asp_procedure)
        control.ground([("base", [])])

        control.configuration.solve.models = 0
        with control.solve(yield_=True) as handle:
            for m in handle:
                self.answers = [[(int)(not atom.arguments[0].negative)
                                 for atom in m.symbols(atoms=True)
                                 if atom.name == "collective"]]

            handle.get()

        return self.answers != []
