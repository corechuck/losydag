import rstr
import re
import random
import datetime
import math
from owlready2 import Thing, destroy_entity

from utils.utils import ExtensionContext

MAX_RANGE = 999999999
MIN_RANGE = -999999999


def extend_core(context: ExtensionContext):
    _core = context.core

    class Constraint(Thing):
        namespace = _core
        TRIES_COUNT = 500

        def __init__(self, name=None, namespace=None, **kargs):
            super().__init__(name=name, namespace=namespace, **kargs)
            self.not_picks = list()
            self.not_matching_regexes = list()
            self.partition_relevant_value_options = list()

        def generate(self, local_dict):
            return str(self._generate(local_dict))

        # def generate(self, local_dict):
        #     tries = 0
        #     tried_values = list()
        #
        #     while True:
        #         tries += 1
        #         if self.has_more_relevant_options():
        #             random.shuffle(self.partition_relevant_value_options)
        #             generated_value = self.partition_relevant_value_options.pop()
        #         else:
        #             generated_value = str(self._generate(local_dict))
        #
        #         if (
        #                 generated_value not in self.not_picks and
        #                 not self.__is_value_matching_prohibited_regexes(str(generated_value))
        #         ):
        #             return generated_value
        #         else:
        #             tried_values.append(generated_value)
        #
        #             if tries >= self.TRIES_COUNT:
        #                 print(f"INFO: Tried values {tried_values}")
        #                 raise Exception(f"ERROR: Could not generate value that met constrained in {self}")
        #
        #     return "#non-value-002"

        def has_more_relevant_options(self):
            return len(self.partition_relevant_value_options) > 0

        # def __is_value_matching_any_not_constraint(self, value, list_of_not_constraint):
        #     return any(constraint.does_value_match_constraint(value) for constraint in list_of_not_constraint)

        def does_value_match_constraint(self, value_under_question):
            return not value_under_question

        def __is_value_matching_prohibited_regexes(self, question_value):
            partial_checks = [pat for pat in self.not_matching_regexes if re.search(pat, question_value)]
            return len(self.not_matching_regexes) > 0 and len(partial_checks) > 0

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

        @property
        def is_list(self):
            return type(self) == _core.ListConstraint

        @property
        def is_range(self):
            return type(self) == _core.RangeConstraint

        @property
        def is_regex(self):
            return type(self) == _core.RegexConstraint

        @property
        def is_dependency(self):
            return isinstance(self, _core.ValueDependency)

        @property
        def is_generic_constraint(self):
            return type(self) == _core.Constraint
            # # I hate it ... is there any better way to know if you are this class in inheritence but child class?
            # return isinstance(self, _core.Constraint) and not isinstance(self, _core.ListConstraint) and \
            #        not isinstance(self, _core.RangeConstraint) and not isinstance(self, _core.RegexConstraint) and \
            #        not isinstance(self, _core.ValueDependency)

        def _merge_with(self, right_constraint):
            # print(f"WARNING: Requested merging {self.name} with {right_constraint.name} without reasoning types.")
            self.not_picks.extend(right_constraint.not_picks)
            self.not_matching_regexes.extend(right_constraint.not_matching_regexes)
            return self

        def merge_with(self, right_constraint):
            left_constraint = self

            if self.is_dependency or right_constraint.is_dependency:
                raise Exception("ERROR: Cannot merge Value Dependency.")

            if left_constraint.is_generic_constraint and not right_constraint.is_generic_constraint:
                left_constraint = right_constraint
                right_constraint = self

            if left_constraint.is_range and right_constraint.is_list:
                left_constraint = right_constraint
                right_constraint = self

            if left_constraint.is_regex and right_constraint.is_list:
                left_constraint = right_constraint
                right_constraint = self

            return left_constraint._merge_with(right_constraint)

        def prepare_relevant_partition_values(self):
            self.partition_relevant_value_options = []

    class ListConstraint(Constraint):
        namespace = _core

        def _generate(self, __yagni):
            return random.choice(self.has_picks)

        def _merge_with(self, right_constraint):
            if right_constraint.is_list:
                self.has_picks = list(set(self.has_picks) & set(right_constraint.has_picks))

            # 2. Merge with Range > check if parseable to float/double/decimal
            if right_constraint.is_range:
                self.has_picks = [pick for pick in self.has_picks if right_constraint.is_meeting_constraint(pick)]

            # 3. Merge with regex > check if list elements follow regex > remove
            if right_constraint.is_regex:
                self.has_picks = [pick for pick in self.has_picks if right_constraint.is_meeting_constraint(pick)]

            super()._merge_with(right_constraint)
            destroy_entity(right_constraint)
            return self  # Keep list as type

        def prepare_relevant_partition_values(self):
            self.partition_relevant_value_options = self.has_picks.copy()

        def does_value_match_constraint(self, value_under_question):
            return value_under_question in self.has_picks

    class RegexConstraint(Constraint):
        namespace = _core

        def _generate(self, __yagni):
            generated_value = rstr.xeger(self.has_regex_format)
            if self.is_constraining_column is None:
                return generated_value

            if isinstance(self._get_constrained_data_type(), _core.Date):
                # to do check if generated is date !!
                return generated_value

            if isinstance(self._get_constrained_data_type(), _core.Decimal):
                if not generated_value.isnumeric():
                    raise Exception(
                        f"Regex Constraint could not generate number from {self.has_regex_format}")
                return generated_value

            return generated_value

        def _merge_with(self, right_constraint):
            if right_constraint.is_regex:
                questioned_value = self._generate(None)
                if not right_constraint._is_meeting_constraint(questioned_value):
                    raise Exception(f"ERROR: {self.name} regex is not compatible {right_constraint.name}")
                else:
                    print(f"WARNING: Merging regex with regex with passed sanity check, keeping only {self.name}.")

            if right_constraint.is_list:
                raise Exception("ERROR: You should not merge list to regex!")

            if right_constraint.is_range:
                raise Exception("ERROR: Not implemented")

            super()._merge_with(right_constraint)
            destroy_entity(right_constraint)
            return self

        def is_meeting_constraint(self, value):
            return re.search(self.has_regex_format, value) is not None

        def prepare_relevant_partition_values(self):
            print("INFO: Cannot prepare partition relevant data for regex constraint.")
            self.partition_relevant_value_options = self._generate(None)

        def does_value_match_constraint(self, value_under_question):
            return re.search(self.has_regex_format, value_under_question)


    class RangeConstraint(Constraint):
        namespace = _core

        def __init__(self, name, namespace=None, **kargs):
            super().__init__(name=name, namespace=namespace, **kargs)
            self._prepare_min_max()

        def _prepare_min_max(self):
            if self.has_min_range is None:
                self.has_min_range = MIN_RANGE
            if self.has_max_range is None:
                self.has_max_range = MAX_RANGE

        def _generate(self, __yagni=None):
            if self.has_min_range > self.has_max_range:
                raise Exception(f"ERROR: {self.name} has min greater then higher.")

            self._prepare_min_max()

            if type(self._get_constrained_data_type()) == _core.Date:
                raise Exception(f"ERROR: No range for dates (yet) :| sorry.")

            if type(self._get_constrained_data_type()) == _core.Varchar:
                raise Exception(f"ERROR: No range for strings/varchars :| sorry.")

            # if type(self._get_constrained_data_type()) == _core.Decimal:
                # for decimal we can do some check if max range is greater then scale - precision for decimals.

            chosen_number = random.randint(int(self.has_min_range), int(self.has_max_range))
            return chosen_number

        def _merge_with(self, right_constraint):
            self._prepare_min_max()
            if right_constraint.is_regex:
                raise Exception("ERROR: Not implemented")

            if right_constraint.is_list:
                raise Exception("ERROR: You should not merge list to range!")

            if right_constraint.is_range:
                self.has_min_range = max(self.has_min_range, right_constraint.has_min_range)
                self.has_max_range = min(self.has_max_range, right_constraint.has_max_range)
                if self.has_min_range > self.has_max_range:
                    raise Exception(f"ERROR: Ranges {self.name} and {right_constraint.name} are not intersecting.")

            super()._merge_with(right_constraint)
            destroy_entity(right_constraint)
            return self

        def is_meeting_constraint(self, value):
            self._prepare_min_max()
            try:
                number_value = int(value)
            except:
                return False
            return self.has_min_range <= number_value <= self.has_max_range

        def prepare_relevant_partition_values(self):
            if self.has_min_range > self.has_max_range:
                raise Exception(f"ERROR: {self.name} has min greater then higher.")

            if self.has_min_range == self.has_max_range:
                raise Exception(f"ERROR: {self.name} min and max equal, cannot prepare partitions.")

            self.partition_relevant_value_options = [self.__generate_not_boundary_value()]
            if self.has_min_range != MIN_RANGE:
                self.partition_relevant_value_options.append(MIN_RANGE)
            if self.has_max_range != MAX_RANGE:
                self.partition_relevant_value_options.append(MAX_RANGE)

        def __generate_not_boundary_value(self):
            loop = 0
            while loop < 100:
                loop +=1
                chosen_number = random.randint(int(self.has_min_range), int(self.has_max_range))
                if chosen_number != self.has_min_range and chosen_number != self.has_max_range:
                    return chosen_number

            raise Exception(f"ERROR: {self.name} could not generate non boundary value.")

        def does_value_match_constraint(self, value_under_question):
            return self.has_min_range <= value_under_question <= self.has_max_range
