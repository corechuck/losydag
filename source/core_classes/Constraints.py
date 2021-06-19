import rstr
import re
import random
import datetime
import math
from owlready2 import Thing


def extend_core(_core):

    class Constraint(Thing):
        namespace = _core
        TRIES_COUNT = 10

        def generate(self, local_dict):
            tries = 0

            while True:
                tries += 1
                generated_value = str(self._generate(local_dict))
                if (
                        generated_value not in self.not_picks and
                        not self.__is_value_matching_prohibited_regexes(generated_value)
                ):
                    return generated_value

                elif tries >= self.TRIES_COUNT:
                    raise Exception(f"ERROR: Could not generate value that met constrained in {self}")

            return "#non-value-002"

        def __is_value_matching_prohibited_regexes(self, question_value):
            partial_checks = [re.search(pat, question_value) for pat in self.not_matching_regex]
            return len(self.not_matching_regex) > 0 and all(partial_checks)

        def is_ready(self, _local_dict):
            return True

        def _get_constrained_data_type(self):
            return self.is_constraining_column.has_data_type

        def _generate(self, _local_dict):
            if isinstance(self._get_constrained_data_type(), _core.Varchar):
                return rstr.xeger(r"[\w ]{8,16}")

            if isinstance(self._get_constrained_data_type(), _core.Date):
                return datetime.datetime.now().strftime("%x")

            if isinstance(self._get_constrained_data_type(), _core.Decimal):
                decimal_type = self._get_constrained_data_type()
                expanded_scale = math.pow(10, decimal_type.has_scale)
                expanded_precision = math.pow(10, decimal_type.has_precision)
                return round((random.random()-0.5)*expanded_scale)/expanded_precision

            return "#non-value"

        def is_constraining_same_column_as(self, _other_constraint):
            return _other_constraint.is_constraining_column.name == self.is_constraining_column.name

    class RegexConstraint(Thing):
        namespace = _core

        def _generate(self, __yagni):
            generated_value = rstr.xeger(self.has_regex_format)
            if self.is_constraining_column is None:
                return generated_value

            if isinstance(self._get_constrained_data_type(), _core.Varchar):
                return generated_value

            if isinstance(self._get_constrained_data_type(), _core.Date):
                return generated_value

            if isinstance(self._get_constrained_data_type(), _core.Decimal):
                if not generated_value.isnumeric():
                    raise Exception(
                        "Regex Constraint could not generate number from {self.has_regex_format}")
                return generated_value

            return "#non-value-001"

    class ListConstraint(Thing):
        namespace = _core

        def _generate(self, __yagni):
            # amount_of_picks = len(self.has_picks)
            #
            # chosen_pick = random.randint(0, amount_of_picks-1)
            # return self.has_picks[chosen_pick]

            return random.choice(self.has_picks)

    class RangeConstriant(Thing):
        namespace = _core

        def _generate(self, __yagni):

            if isinstance(self._get_constrained_data_type(), _core.Decimal):
                chosen_number = random.randint(int(self.has_min_range), int(self.has_max_range))
                return chosen_number

