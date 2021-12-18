import rstr
import re
import random
import datetime
import math
from owlready2 import Thing, destroy_entity

from utils.utils import MergingException
from utils.context import ExtensionContext

MAX_RANGE = 999999999
MIN_RANGE = -999999999


def extend_core(context: ExtensionContext):
    _core = context.core

    class Constraint(Thing):
        namespace = _core
        TRIES_COUNT = 500
        my_restrictor = None

        def __init__(self, name=None, namespace=None, **kwargs):
            super().__init__(name=name, namespace=namespace, **kwargs)
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
            return False

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

        def toggle_restriction(self):
            """ This is a wierd name. This method will make restriction or return internal constraint."""
            if not self.my_restrictor:
                self.my_restrictor = _core.RestrictiveConstraint(restricting_constraint=self)
            return self.my_restrictor

    class RestrictiveConstraint(Constraint):

        def __init__(self, name=None, namespace=None, restricting_constraint=None,  **kwargs):
            super().__init__(name=name, namespace=namespace, **kwargs)
            self.restriction_definition = restricting_constraint

        def does_value_match_constraint(self, value_under_question):
            return self.restriction_definition.does_value_match_constraint(value_under_question)

        def toggle_restriction(self):
            return self.restriction_definition

        @property
        def restricting_column(self):
            return self.restricting_columns[0]

    class ListConstraint(Constraint):
        namespace = _core

        def _generate(self, __yagni):
            return random.choice(self.has_picks)

        def _merge_with(self, right_constraint):
            if right_constraint.is_list:
                self.has_picks = list(set(self.has_picks) & set(right_constraint.has_picks))

            # 2. Merge with Range > check if parseable to float/double/decimal
            if right_constraint.is_range:
                self.has_picks = [pick for pick in self.has_picks if right_constraint.does_value_match_constraint(pick)]

            # 3. Merge with regex > check if list elements follow regex > remove
            if right_constraint.is_regex:
                self.has_picks = [pick for pick in self.has_picks if right_constraint.does_value_match_constraint(pick)]

            if len(self.has_picks) == 0:
                raise MergingException(
                    f"ERROR: Merging {self.name} with {right_constraint.name} resulted in empty pick list.")

            super()._merge_with(right_constraint)
            # destroy_entity(right_constraint)
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
                if not right_constraint.does_value_match_constraint(questioned_value):
                    raise MergingException(f"ERROR: {self.name} regex is not compatible {right_constraint.name}")
                else:
                    print(f"WARNING: Merging regex with regex with passed sanity check, keeping only {self.name}.")

            if right_constraint.is_list:
                raise MergingException("ERROR: You should not merge list to regex!")

            if right_constraint.is_range:
                raise MergingException("ERROR: Not implemented")

            super()._merge_with(right_constraint)
            #destroy_entity(right_constraint)
            return self

        def prepare_relevant_partition_values(self):
            print("INFO: Cannot prepare partition relevant data for regex constraint.")
            self.partition_relevant_value_options = [self._generate(None)]

        def does_value_match_constraint(self, value_under_question):
            return re.search(self.has_regex_format, value_under_question) is not None

    class RangeConstraint(Constraint):
        namespace = _core
        precision = 5
        scale = 2

        def __init__(self, name, namespace=None,
                     left_boundary=None, right_boundary=None, is_left_open=False, is_right_open=False, **kwargs):
            super().__init__(name=name, namespace=namespace, **kwargs)

            if self._get_constrained_data_type() is not None:
                self.precision = self._get_constrained_data_type().has_precision
                self.scale = self._get_constrained_data_type().has_scale

            if self.has_left_boundary is None and left_boundary is None:
                self.set_left_boundary(self._get_minimum_left_boundary_for_type(), is_left_open)
            if self.has_right_boundary is None and right_boundary is None:
                self.set_right_boundary(self._get_maximum_right_boundary_for_type(), is_right_open)

        def set_left_boundary(self, value, is_open=False):
            if is_open:
                self.has_left_boundary = _core.OpenRangeBoundary()
            else:
                self.has_left_boundary = _core.ClosedRangeBoundary()

            self.has_left_boundary.has_boundary_value = value

        def set_right_boundary(self, value, is_open=False):
            if is_open:
                self.has_right_boundary = _core.OpenRangeBoundary()
            else:
                self.has_right_boundary = _core.ClosedRangeBoundary()

            self.has_right_boundary.has_boundary_value = value

        def _prepare_min_max(self):
            pass
            # if self.has_left_boundary is None:
            #     self.set_left_boundary(MIN_RANGE)
            # if self.has_right_boundary is None:
            #     self.set_right_boundary(MAX_RANGE)

            # if self._get_constrained_data_type() is None:
            #     return
            #
            # self.precision = self._get_constrained_data_type().has_precision
            # self.scale = self._get_constrained_data_type().has_scale
            #
            # if self.has_left_boundary is None:
            #     self.set_left_boundary(self._get_minimum_left_boundary_for_type())
            # if self.has_right_boundary is None:
            #     self.set_right_boundary(self._get_maximum_right_boundary_for_type())

        def _get_minimum_left_boundary_for_type(self):
            return sum(math.pow(10, d)*9 for d in range(1, self.precision))*-1 / math.pow(10, self.scale)

        def _get_maximum_right_boundary_for_type(self):
            return sum(math.pow(10, d)*9 for d in range(1, self.precision)) / math.pow(10, self.scale)

        def _get_minimum_viable_value(self):
            min_viable = self.has_left_boundary.has_boundary_value
            if isinstance(self.has_left_boundary, _core.OpenRangeBoundary):
                min_viable += (1 / math.pow(10, self.scale))
            return min_viable
        # todo: TESTS for those boundary conditions !!!!!

        def _get_maximum_viable_value(self):
            max_viable = self.has_right_boundary.has_boundary_value
            if isinstance(self.has_right_boundary, _core.OpenRangeBoundary):
                max_viable -= (1 / math.pow(10, self.scale))
            return max_viable

        def _generate(self, __yagni=None):
            self.__assert_range_boundaries_are_valid()
            self._prepare_min_max()

            if type(self._get_constrained_data_type()) == _core.Date:
                raise Exception(f"ERROR: No range for dates (yet) :| sorry.")

            if type(self._get_constrained_data_type()) == _core.Varchar:
                raise Exception(f"ERROR: No range for strings/varchars :| sorry.")

            if type(self._get_constrained_data_type()) == _core.Decimal:
                self.precision = self._get_constrained_data_type().has_precision
                self.scale = self._get_constrained_data_type().has_scale
                # for decimal we can do some check if max range is greater then scale - precision for decimals.

            if self._get_minimum_viable_value() <= self._get_minimum_left_boundary_for_type():
                raise Exception(f"ERROR: Chosen left value outside of decimal precision "
                                f"for column {self.is_constraining_column.name}")

            if self._get_maximum_viable_value() >= self._get_maximum_right_boundary_for_type():
                raise Exception(f"ERROR: Chosen right value outside of decimal precision "
                                f"for column {self.is_constraining_column.name}")

            scaleless_min_viable_value = self.__get_minimum_viable_value() * math.pow(10, self.scale)
            scaleless_max_viable_value = self.__get_maximum_viable_value() * math.pow(10, self.scale)

            chosen_number = random.randint(scaleless_min_viable_value, scaleless_max_viable_value)
            return chosen_number / math.pow(10, self.scale)

        @property
        def left_boundary(self):
            return self.has_left_boundary.has_boundary_value

        @property
        def right_boundary(self):
            return self.has_right_boundary.has_boundary_value

        def _merge_with(self, right_constraint):
            self._prepare_min_max()
            if right_constraint.is_regex:
                raise MergingException("ERROR: Cannot merge regex with range in deterministic fashion.")

            if right_constraint.is_list:
                raise Exception("ERROR: You should not merge list to range!")

            if not right_constraint.is_range:
                raise Exception("ERROR: Right constraint of unknown type.")

            if self.has_left_boundary.has_boundary_value < right_constraint.has_left_boundary.has_boundary_value:
                self.has_left_boundary = right_constraint.has_left_boundary

            if (self.has_left_boundary.has_boundary_value ==
                right_constraint.has_left_boundary.has_boundary_value) and \
               not isinstance(self.has_left_boundary, _core.ClosedRangeBoundary) and \
               isinstance(right_constraint.has_left_boundary, _core.ClosedRangeBoundary):
                self.has_left_boundary = right_constraint.has_left_boundary

            if right_constraint.has_right_boundary.has_boundary_value < self.has_right_boundary.has_boundary_value:
                self.has_right_boundary = right_constraint.has_right_boundary

            if (self.has_right_boundary.has_boundary_value ==
                    right_constraint.has_right_boundary.has_boundary_value) and \
               not isinstance(self.has_right_boundary, _core.ClosedRangeBoundary) and \
               isinstance(right_constraint.has_right_boundary, _core.ClosedRangeBoundary):
                self.has_right_boundary = right_constraint.has_right_boundary

            self.__assert_range_boundaries_are_valid()

            super()._merge_with(right_constraint)
            return self

        def __assert_range_boundaries_are_valid(self):
            if self.has_left_boundary.has_boundary_value > self.has_right_boundary.has_boundary_value:
                raise Exception(f"ERROR: Left boundary is greater then right for Range {self.name}.")

            if self.has_left_boundary.has_boundary_value == self.has_right_boundary.has_boundary_value and \
               (
                    not isinstance(self.has_left_boundary, _core.ClosedRangeBoundary) or
                    not isinstance(self.has_right_boundary, _core.ClosedRangeBoundary)
               ):
                raise Exception(f"ERROR: Left boundary is equal to right for Range {self.name}.")

        def prepare_relevant_partition_values(self):
            self.__assert_range_boundaries_are_valid()

            self.partition_relevant_value_options = [
                self.__get_minimum_viable_value(),
                self.__generate_not_boundary_value(),
                self.__get_maximum_viable_value()
            ]
            if self.self.has_left_boundary.has_boundary_value != MIN_RANGE:
                self.partition_relevant_value_options.append(MIN_RANGE)
            if self.self.has_right_boundary.has_boundary_value != MAX_RANGE:
                self.partition_relevant_value_options.append(MAX_RANGE)

        def __generate_not_boundary_value(self):
            loop = 0
            while loop < 100:
                loop += 1
                chosen_number = self._generate()

                _is_meeting_left = False
                if isinstance(self.has_left_boundary, _core.ClosedRangeBoundary):
                    _is_meeting_left = self.has_left_boundary.has_boundary_value < chosen_number
                else:
                    _is_meeting_left = self.__get_minimum_viable_value() < chosen_number

                _is_meeting_left = ( self.has_left_boundary.has_boundary_value < chosen_number)

                _is_meeting_right = False
                if isinstance(self.has_right_boundary, _core.ClosedRangeBoundary):
                    _is_meeting_right = chosen_number < self.has_right_boundary.has_boundary_value
                else:
                    _is_meeting_right = chosen_number < self.__get_maximum_viable_value()

                if _is_meeting_left and _is_meeting_right:
                    return chosen_number

            raise Exception(f"ERROR: {self.name} could not generate non boundary value.")

        def does_value_match_constraint(self, _value_under_question):
            self._prepare_min_max()
            try:
                number_value = float(_value_under_question)
            except ValueError:
                return False

            _is_meeting_left = False
            if isinstance(self.has_left_boundary, _core.ClosedRangeBoundary):
                _is_meeting_left = self.has_left_boundary.has_boundary_value <= number_value
            else:
                _is_meeting_left = self.has_left_boundary.has_boundary_value < number_value

            _is_meeting_right = False
            if isinstance(self.has_right_boundary, _core.ClosedRangeBoundary):
                _is_meeting_right = number_value <= self.has_right_boundary.has_boundary_value
            else:
                _is_meeting_right = number_value < self.has_right_boundary.has_boundary_value

            return _is_meeting_left and _is_meeting_right
