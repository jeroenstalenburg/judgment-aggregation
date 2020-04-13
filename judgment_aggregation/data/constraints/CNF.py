from .Constraint import Constraint
# import sympy as sp
import numpy as np
# import sympy.logic.boolalg as ba
# from sympy import var


class CNF(Constraint):
    def reset(self):
        self.lines = 0
        self.clauses_loaded = 0
        self.var_amount = 0
        self.clause_amount = 0
        self.clauses = []
        # self.boolean_expression = ba.BooleanTrue
        # self.boolean_vars = []
        self.p_initialised = False

    def __str__(self):
        return ("JA CNF constraint object {\n  Clauses: %s\n}" % self.clauses)

    def initialise_data(self, var_amount, clause_amount):
        """Initialise the data for the class for future use"""
        self.clauses_loaded = 0
        self.var_amount = var_amount
        self.clause_amount = clause_amount
        self.clauses = [[]] * clause_amount
        # self.boolean_expression = ba.BooleanTrue
        # self.boolean_vars = [var(str(i + 1)) for i in range(var_amount)]
        self.p_initialised = True

    def load_p_line(self, *args):
        if self.p_initialised:
            self.throw_error("May not redefine amount of issues and "
                             "voters in the middle of a cnf file")
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

    def load_a_line(self, *args):
        try:
            clause = list(map(int, args))
        except ValueError:
            self.throw_error("'a' line should consist of only integers")
        if clause[-1] != 0:
            self.throw_error("'a' line should end with a 0")
        self.add_clause(clause[:-1])

    def add_clause(self, clause):
        """"""
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
        # sp_clause = self.boolean_vars[clause[0] - 1]
        # for c in clause[1:]:
        #     sp_clause = sp_clause | self.boolean_vars[c - 1]
        # self.boolean_expression = self.boolean_expression & sp_clause
        self.clauses_loaded += 1

    def check_agenda(self, agenda):
        def check_clause(clause):
            for index in clause:
                if (index < 0) ^ agenda[abs(index) - 1]:
                    return True
            return False

        for clause in self.clauses:
            if not check_clause(clause):
                return False
        return True

    def merge_data(self, other):
        pass
