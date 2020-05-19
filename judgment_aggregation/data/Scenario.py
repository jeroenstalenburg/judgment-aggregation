from .Data import Data
from .constraints.CNF import CNF
from .constraints.Constraint import Constraint
from .ScenarioVisualizer import ScenarioVisualizer
from ..solvers import solvers


class Scenario(Data):
    def reset(self):
        self.lines = 0
        self.judgments_loaded = 0
        self.issue_amount = 0
        self.auxiliary_amount = 0
        self.judgment_amount = 0
        self.judge_amount = 0
        self.issues = []
        self.individual_judgments = []
        self.collective_judgments = []
        self.judges_per_judgment = []
        self.individual_constraints = []
        self.collective_constraints = []
        self.p_initialised = False

    def __str__(self):
        return (
            "JA data object {\n  Issues: %s\n"
            "  Voters, Judgments: %s \n}" %
            (self.issues,
             list(zip(self.judges_per_judgment, self.individual_judgments))))

    def initialise_data(self,
                        issue_amount,
                        judgment_amount,
                        auxiliary_amount=0):
        """Initialise the data for the class for future use"""
        self.issue_amount = issue_amount
        self.judgment_amount = judgment_amount
        self.auxiliary_amount = auxiliary_amount
        self.judge_amount = 0
        self.judgments_loaded = 0
        self.issues = [''] * self.issue_amount
        self.individual_judgments = [[]] * self.judgment_amount
        self.judges_per_judgment = [0] * self.judgment_amount
        self.p_initialised = True

    def solve(self,
              solver='BruteForce',
              procedure='Kemeny',
              score_fun=None,
              init_fun=None,
              quota=0.5):
        solver_object = solvers[solver](self)
        solver_object.solve(procedure='Kemeny',
                            score_fun=None,
                            init_fun=None,
                            quota=0.5)
        self.collective_judgments = solver_object.get_answers()

    def load_p_line(self, *args):
        if self.p_initialised:
            self.throw_error("May not redefine amount of issues and "
                             "judges in the middle of a ja file")
        if args[0] != "ja":
            self.throw_error("The given file is not a scenario file")
        if len(args) == 4:
            self.initialise_data(int(args[1]), int(args[2], int(args[3])))
        elif len(args) == 3:
            self.initialise_data(int(args[1]), int(args[2]))
        else:
            self.throw_error("Expected two or three arguments after 'p ja'")

    def load_n_line(self, *args):
        try:
            self.add_issue_name(args[1], int(args[0]))
        except ValueError as e:
            self.throw_error("'%s' not a number" % args[0])

    def load_i_line(self, *args):
        """Load a 'i' line; 'i' lines are for setting the constraint files
        for either the judge judgments or the collective judgment.
        i <in/out> <constraint type> <file>"""
        if (len(args) != 3):
            self.throw_error("'i' lines should have the form "
                             "'i <in/out> <constraint type> <file>'")
        if (not (args[0] == 'in' or args[0] == 'out' or args[0] == 'in/out')):
            self.throw_error("Second argument of 'i' line should be 'in', "
                             "'out' or 'in/out'")
        if (args[1] == 'cnf'):
            con = CNF(self.path)
            con.load_file(args[2])
            self.add_constraint(con, args[0])
        else:
            self.throw_error("Invalid constraint type '%s'" % args[1])

    def load_v_line(self, *args):
        """Load a 'v' line; 'v' lines are for setting the judgment
        of a single judge.
        v 1 1 0 1"""
        self.load_vm_line(1, *args)

    def load_vm_line(self, *args):
        """Load a 'vm' line; 'vm' lines are for setting the judgment
        of multiple judge.
        vm <judge amount> 1 1 0 1"""
        try:
            judges = int(args[0])
        except ValueError:
            self.throw_error("Amount of judges '%s' needs to be an integer" %
                             args[0])
        try:
            judgment = list(map(lambda x: bool(int(x)), args[1:]))
        except ValueError:
            self.throw_error(
                "Judgments in ja files should be encoded in 0's and 1's; "
                "This is not the case")
        self.add_judgment(judgment, judges)

    def add_issue_name(self, name, index=None):
        """"""
        self.check_initialised()
        if index is None:
            self.issues.append(name)
            self.issue_amount += 1
        else:
            self.issues[index - 1] = name

    def add_constraint(self, constraint, binding="in/out"):
        """Add a constraint to the scenario; the given constraint has to
        be of the constraint class or its subclasses.
        The binding parameter is used to tell if the constraint is for the
        judge judgment's or/and for the collective judgment's"""
        if not isinstance(constraint, Constraint):
            self.throw_error(
                "Given constraint object with class '%s' is not from the "
                "constraint class or one of its subclasses" % type(constraint))
        if binding == "in/out":
            self.add_individual_constraint(constraint)
            self.add_collective_constraint(constraint)
        elif binding == "in":
            self.add_individual_constraint(constraint)
        elif binding == "out":
            self.add_collective_constraint(constraint)
        else:
            self.throw_error("Constraint binding should be equal to "
                             "'in', 'out', or 'in/out'")

    def add_individual_constraint(self, constraint):
        """Add a constraint for the individual judgments"""
        var_amount = constraint.get_var_amount()
        if self.issue_amount != var_amount:
            self.throw_error("Individual constraints should have the same "
                             "amount of variables as the scenario has issues")
        self.individual_constraints.append(constraint)

    def add_collective_constraint(self, constraint):
        """Add a constraint for the resultant, collective judgments"""
        var_amount = constraint.get_var_amount()
        if self.auxiliary_amount + self.issue_amount != var_amount:
            self.throw_error("Collective constraint should have the same "
                             "amount of variables as the scenario has "
                             "issues and auxiliary variables")
        self.collective_constraints.append(constraint)

    def add_judgment(self, judgment, judge_amount=1):
        """Add a judgment to the scenario."""
        self.check_initialised()
        if (not all([a == 1 or a == 0 for a in judgment])):
            self.throw_error("Judgment should consist of only 0's, 1's or "
                             "booleans")
        if (self.judgments_loaded >= self.judgment_amount):
            self.throw_error("May not add more judgments than specified while "
                             "initialising the object")
        if (len(judgment) < self.issue_amount):
            self.throw_error(
                "Judgment should have an opinion about every issue; "
                "The length of the judgment is too low")
        if (len(judgment) > self.issue_amount):
            self.throw_error(
                "Judgment should not have more opinions than there are on the "
                "judgment; The length of the judgment is too high")
        for constraint in self.individual_constraints:
            if not constraint.check_judgment(judgment):
                self.throw_error("Judgment '%s' is not valid according to the "
                                 "individual constraints of this scenario" %
                                 judgment)
        self.individual_judgments[self.judgments_loaded] = judgment
        self.judges_per_judgment[self.judgments_loaded] = judge_amount
        self.judgments_loaded += 1
        self.judge_amount += judge_amount

    def get_judgments(self, also_get_judge_amounts=True):
        """Return all judgments of the current scenario.
        if also_get_judge_amounts is true, then returned is the tuple:
        (judgments, judge amounts)"""
        if also_get_judge_amounts:
            return self.individual_judgments, self.judges_per_judgment
        else:
            return self.individual_judgments

    def get_issue_names(self):
        """Get the names of the issues in the current scenario."""
        return self.issues

    def get_collective_judgments(self):
        """Get the collective judgments of the current scenario."""
        return self.collective_judgments

    def plot_table(self, ax):
        vis = ScenarioVisualizer(self, show_majority=True)
        vis.plot_data(ax)
