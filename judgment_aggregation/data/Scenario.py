from .Data import Data
from .constraints.CNF import CNF
from ..JAError import JAError


class Scenario(Data):
    def reset(self):
        self.lines = 0
        self.agendas_loaded = 0
        self.voters = 0
        self.issue_amount = 0
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

    def initialise_data(self, issue_amount, agenda_amount):
        """Initialise the data for the class for future use"""
        self.issue_amount = issue_amount
        self.agenda_amount = agenda_amount
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
        if len(args) != 3:
            self.throw_error("Expected two arguments after 'p ja'")
        self.initialise_data(int(args[1]), int(args[2]))

    def add_issue_name(self, name, index=None):
        """"""
        self.check_initialised()
        if index is None:
            self.issues.append(name)
            self.issue_amount += 1
        else:
            self.issues[index - 1] = name

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

    def add_constraint(self, constraint, inout="in/out"):
        """Add a constraint to the scenario; the given constraint has to
        be of the constraint class or its subclasses.
        The inout parameter is used to tell if the constraint is for the
        voter agenda's or/and for the collective agenda's"""
        pass

    def add_agenda(self, agenda, voter_amount=1):
        """"""
        self.check_initialised()
        if (not all([a == 1 or a == 0 for a in agenda])):
            self.throw_error("Agenda should consist of only 0's, 1's or "
                             "booleans")
        if (self.agendas_loaded >= self.agenda_amount):
            self.throw_error("May not add more agendas than specified while "
                             "initialising the object")
        self.agendas[self.agendas_loaded] = agenda
        self.voters_per_agenda[self.agendas_loaded] = voter_amount
        self.agendas_loaded += 1
        self.voters += voter_amount

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
        except ValueError as e:
            self.throw_error("Amount of voters '%s' needs to be an integer" %
                             args[0])
        try:
            agenda = list(map(lambda x: bool(int(x)), args[1:]))
        except ValueError as e:
            self.throw_error(
                "Agendas in ja files should be encoded in 0's and 1's; "
                "This is not the case")
        self.add_agenda(agenda, voters)

    def merge_data(self, other):
        pass


# if __name__ == "__main__":
#     data = ScenarioData("notall3scenari.ja")
#     # data.load_from_file()
#     print(data)
#     # data.load_string("jaaaaaaaaaa\nneeeee")
