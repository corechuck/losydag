import rstr
import random
from owlready2 import Thing
#from SyntheticExceptions import GenerationTypeException


def extend_core(_core):

    class Constraint(Thing):
        namespace = _core

        # def __init__(self):
        #     pass
        
        def generate(self):
            child_value = self._generate()
            return f"Child value: {child_value}"
            
        def _generate(self):
            return ""

        def _get_constrained_data_type(self):
            return self.isConstrainingColumn.hasDataType


    class RegexConstraint(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            if isinstance(self._get_constrained_data_type(), _core.Varchar):
                return rstr.xeger(self.hasRegexFormat)

            if isinstance(self._get_constrained_data_type(), _core.Date):
                return rstr.xeger(self.hasRegexFormat)

            if isinstance(self._get_constrained_data_type(), _core.Number):
                generated_number_str = rstr.xeger(self.hasRegexFormat)
                if not generated_number_str.isnumeric():
                    raise Exception(
                        "Regex Constraint could not generate number from {self.hasRegexFormat}")
                return generated_number_str

            if isinstance(self._get_constrained_data_type(), _core.Number):
                return str(True)


    class ListConstraint(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            amount_of_picks = len(self.hasPicks)
            chosen_pick = random.randint(1, amount_of_picks-1)
            return self.hasPicks[chosen_pick]


    class RangeConstriant(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            
            if isinstance(self._get_constrained_data_type(), _core.Decimal):
                chosen_number = random.randint(int(self.hasMinRange), int(self.hasMaxRange))
                return chosen_number

            #return rstr.xeger(r"Rng__\w{1,7}")

