from .Data import Data
from .constraints.CNF import CNF
from .constraints.Constraint import Constraint


class Scenario(Data):
    def reset(self):
        self.lines = 0
        self.agendas_loaded = 0
        self.voters = 0
        self.issue_amount = 0
        self.auxiliary_amount = 0
        self.agenda_amount = 0
        self.voter_amount = 0
        self.issues = []
        self.agendas = []
        self.voters_per_agenda = []
        self.individual_constraints = []
        self.collective_constraints = []
        self.p_initialised = False

    def __str__(self):
        return ("JA data object {\n  Issues: %s\n"
                "  Voters, Agendas: %s \n}" %
                (self.issues, list(zip(self.voters_per_agenda, self.agendas))))

    def initialise_data(self, issue_amount, agenda_amount, auxiliary_amount=0):
        """Initialise the data for the class for future use"""
        self.issue_amount = issue_amount
        self.agenda_amount = agenda_amount
        self.auxiliary_amount = auxiliary_amount
        self.voters = 0
        self.agendas_loaded = 0
        self.issues = [''] * self.issue_amount
        self.agendas = [[]] * self.agenda_amount
        self.voters_per_agenda = [0] * self.agenda_amount
        self.p_initialised = True

    def load_p_line(self, *args):
        if self.p_initialised:
            self.throw_error("May not redefine amount of issues and "
                             "voters in the middle of a ja file")
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
        for either the voter agendas or the collective agenda.
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
        """Load a 'v' line; 'v' lines are for setting the agenda
        of a single voter.
        v 1 1 0 1"""
        self.load_vm_line(1, *args)

    def load_vm_line(self, *args):
        """Load a 'vm' line; 'vm' lines are for setting the agenda
        of multiple voter.
        vm <voter amount> 1 1 0 1"""
        try:
            voters = int(args[0])
        except ValueError:
            self.throw_error("Amount of voters '%s' needs to be an integer" %
                             args[0])
        try:
            agenda = list(map(lambda x: bool(int(x)), args[1:]))
        except ValueError:
            self.throw_error(
                "Agendas in ja files should be encoded in 0's and 1's; "
                "This is not the case")
        self.add_agenda(agenda, voters)

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
        voter agenda's or/and for the collective agenda's"""
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
        """Add a constraint for the individual agendas"""
        var_amount = constraint.get_var_amount()
        if self.issue_amount != var_amount:
            self.throw_error("Individual constraints should have the same "
                             "amount of variables as the scenario has issues")
        self.collective_constraints.append(constraint)

    def add_collective_constraint(self, constraint):
        """Add a constraint for the resultant, collective agendas"""
        var_amount = constraint.get_var_amount()
        if self.auxiliary_amount + self.issue_amount != var_amount:
            self.throw_error("Collective constraint should have the same "
                             "amount of variables as the scenario has "
                             "issues and auxiliary variables")
        self.collective_constraints.append(constraint)

    def add_agenda(self, agenda, voter_amount=1):
        """Add an agenda to the scenario."""
        self.check_initialised()
        if (not all([a == 1 or a == 0 for a in agenda])):
            self.throw_error("Agenda should consist of only 0's, 1's or "
                             "booleans")
        if (self.agendas_loaded >= self.agenda_amount):
            self.throw_error("May not add more agendas than specified while "
                             "initialising the object")
        if (len(agenda) < self.issue_amount):
            self.throw_error(
                "Agenda should have an opinion about every issue; "
                "The length of the agenda is too low")
        if (len(agenda) > self.issue_amount):
            self.throw_error(
                "Agenda should not have more opinions than there are on the "
                "agenda; The length of the agenda is too high")
        for constraint in self.individual_constraints:
            if not constraint.check_agenda(agenda):
                self.throw_error("Agenda '%s' is not valid according to the "
                                 "individual constraints of this scenario" %
                                 agenda)
        self.agendas[self.agendas_loaded] = agenda
        self.voters_per_agenda[self.agendas_loaded] = voter_amount
        self.agendas_loaded += 1
        self.voters += voter_amount

    def get_agendas(self, also_get_voter_amounts=True):
        """Return all agendas of the current scenario.
        if also_get_voter_amounts is true, then returned is the tuple:
        (agendas, voter amounts)"""
        if also_get_voter_amounts:
            return self.agendas, self.voters_per_agenda
        else:
            return self.agendas
