from ..Data import Data
from numpy import unpackbits


class Constraint(Data):
    def check_agenda(self, agenda):
        """"""
        raise NotImplementedError(
            "'check_agenda' not implemented for current constraint class %s" %
            type(self).__name__)

    def generate_all_valid_agendas(self):
        """"""
        self.check_initialised()
        if getattr(self, 'var_amount', -1) == -1:
            self.throw_error("The amount of agenda variables has not been set")
        agenda = [1] * self.var_amount
        powers = [2**i for i in range(self.var_amount)][::-1]
        for i in range(2**self.var_amount):
            for power, index in zip(powers, range(self.var_amount)):
                if i % power == 0:
                    agenda[index] ^= 1
            if self.check_agenda(agenda):
                yield agenda.copy()
