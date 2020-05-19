from ..Data import Data
import itertools


class Constraint(Data):
    """Standard class for storing and verifying constraints for judgments"""
    def check_judgment(self, judgment):
        """Given a judgment in list form (e.g. [1, 1, 0]) return true or false
        if valid according to the data"""
        raise NotImplementedError(
            "'check_judgment' not implemented for current constraint class %s"
            % type(self).__name__)

        def get_var_amount(self):
            raise NotImplementedError()

    def generate_all_valid_judgments(self):
        """Generate all valid judgments according to the given constraint"""
        self.check_initialised()
        var_amount = self.get_var_amount()
        if var_amount == -1:
            self.throw_error(
                "The amount of judgment variables has not been set"
                "; A constraint should have a var_amount "
                "attribute")
        for judgment in map(list, itertools.product([0, 1],
                                                    repeat=var_amount)):
            if self.check_judgment(judgment):
                yield judgment.copy()
