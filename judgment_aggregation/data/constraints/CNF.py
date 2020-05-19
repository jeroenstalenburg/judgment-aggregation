from .Constraint import Constraint
# import sympy as sp
import pycosat as ps
import shlex


class CNF(Constraint):
    def reset(self):
        self.lines = 0
        self.clauses_loaded = 0
        self.var_amount = 0
        self.clause_amount = 0
        self.clauses = []
        # self.boolean_expression = sp.true
        self.boolean_vars = []
        self.p_initialised = False

    def __str__(self):
        return ("JA CNF constraint object {\n  Clauses: %s\n}" % self.clauses)

    def initialise_data(self, var_amount, clause_amount):
        """Initialise the data for the class for future use"""
        self.clauses_loaded = 0
        self.var_amount = var_amount
        self.clause_amount = clause_amount
        self.clauses = [[]] * clause_amount
        # self.boolean_expression = sp.true
        # self.boolean_vars = [var(str(i + 1)) for i in range(var_amount)]
        self.p_initialised = True

    def load_lines(self, iterable):
        """Load the contents of a iterable of strings, such as a file or
        list of strings. The strings need to be in the valid format
        args:
            iterable: the iterable object with the correctly formatted lines
            path: is used to resolve the location of files which may be needed
                by the scenario."""
        self.lines = 0
        for line in iterable:
            self.lines += 1
            contents = shlex.split(line.replace('\n', ''))
            if contents == []:
                continue
            if contents[0] == 'p':
                self.load_p_line(*contents[1:])
            else:
                self.load_clause_line(*contents)
        self.lines = 0
        self.finalise()

    def load_p_line(self, *args):
        if self.p_initialised:
            self.throw_error("May not redefine amount of issues and "
                             "judges in the middle of a cnf file")
        if args[0] != "cnf":
            self.throw_error("The given file is not a scenario file")
        if len(args) != 3:
            self.throw_error("Expected two arguments after 'p cnf'")
        try:
            var_amount = int(args[1])
            clause_amount = int(args[2])
        except ValueError:
            self.throw_error("'%s' and/or '%s' not a number" %
                             (args[1], args[2]))
        self.initialise_data(var_amount, clause_amount)

    def load_clause_line(self, *args):
        try:
            clause = list(map(int, args))
        except ValueError:
            self.throw_error("clause line should consist of only integers")
        if clause[-1] != 0:
            self.throw_error("clause line should end with a 0")
        self.add_clause(clause[:-1])

    def add_clause(self, clause):
        """Add a clause to the current CNF constraint"""
        self.check_initialised()
        if (not all([type(c) == int for c in clause])):
            self.throw_error("Clause must be consist of only integers")
        if (self.clauses_loaded >= self.clause_amount):
            self.throw_error("May not add more clauses than specified while "
                             "initialising the object")
        if (not all([c != 0 and abs(c) <= self.var_amount for c in clause])):
            self.throw_error("Variables referenced should be between 1 and "
                             "the amount given during initialisation (%s)" %
                             self.var_amount)
        self.clauses[self.clauses_loaded] = clause
        # sp_clause = sp.false
        # for c in clause:
        #     atom = self.boolean_vars[abs(c) - 1]
        #     if c < 0:
        #         atom = ~atom
        #     sp_clause = sp_clause | atom
        # self.boolean_expression = self.boolean_expression & sp_clause
        # self.boolean_lambda = None
        self.clauses_loaded += 1

    def check_clause(self, clause, judgment):
        """Return True if any of the elements of the clause are True."""
        for index in clause:
            if (index < 0) ^ judgment[abs(index) - 1]:
                return True
        return False

    def check_judgment(self, judgment):
        """Return True if the judgment satisfies the current costraint"""
        for clause in self.clauses:
            if not self.check_clause(clause, judgment):
                return False
        return True

    def generate_all_valid_judgments(self):
        """Generate all valid judgments according to the current constraint"""
        self.check_initialised()
        for judgment in ps.itersolve(self.clauses, vars=self.var_amount):
            yield list(map(lambda x: int(x > 0), judgment))

    def get_var_amount(self):
        """Get the var amount of the current constraint"""
        return self.var_amount
