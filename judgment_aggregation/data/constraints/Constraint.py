from ..Data import Data
import itertools


class Constraint(Data):
    def check_agenda(self, agenda):
        """Given a agenda in list form (e.g. [1, 1, 0]) return true or false
        if valid according to the data"""
        raise NotImplementedError(
            "'check_agenda' not implemented for current constraint class %s" %
            type(self).__name__)

        def get_var_amount(self):
            raise NotImplementedError()

    def generate_all_valid_agendas(self):
        """Generate all valid agendas according to the given constraint"""
        self.check_initialised()
        var_amount = self.get_var_amount()
        if var_amount == -1:
            self.throw_error("The amount of agenda variables has not been set"
                             "; A constraint should have a var_amount "
                             "attribute")
        for agenda in map(list, itertools.product([0, 1], repeat=var_amount)):
            if self.check_agenda(agenda):
                yield agenda.copy()
