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
            return self.is_constraining_column.has_data_type


    class RegexConstraint(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            if isinstance(self._get_constrained_data_type(), _core.Varchar):
                return rstr.xeger(self.has_regex_format)

            if isinstance(self._get_constrained_data_type(), _core.Date):
                return rstr.xeger(self.has_regex_format)

            if isinstance(self._get_constrained_data_type(), _core.Number):
                generated_number_str = rstr.xeger(self.has_regex_format)
                if not generated_number_str.isnumeric():
                    raise Exception(
                        "Regex Constraint could not generate number from {self.has_regex_format}")
                return generated_number_str

            if isinstance(self._get_constrained_data_type(), _core.Number):
                return str(True)


    class ListConstraint(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            amount_of_picks = len(self.has_picks)
            chosen_pick = random.randint(1, amount_of_picks-1)
            return self.has_picks[chosen_pick]


    class RangeConstriant(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            
            if isinstance(self._get_constrained_data_type(), _core.Decimal):
                chosen_number = random.randint(int(self.has_min_range), int(self.has_max_range))
                return chosen_number

            #return rstr.xeger(r"Rng__\w{1,7}")

