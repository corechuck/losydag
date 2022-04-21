import rstr
import re
import random
import datetime
import math
import utils.context
from owlready2 import Thing, destroy_entity
from utils.utils import MergingException, ValueGenerationException, DataTypeIssueException

if not utils.context.core_context\
        or not utils.context.core_context.core\
        or not utils.context.core_context.value_generation_supervisor:
    raise Exception("Cannot import Constraints without initialized utils.context.core_context")

_core = utils.context.core_context.core


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
        self._assert_column_has_data_type()
        generated_value = self._generate(local_dict)
        self._assert_proposed_value_is_valid(generated_value)
        return self._get_constrained_data_type().convert_to_string(generated_value)

    def has_more_relevant_options(self):
        return len(self.partition_relevant_value_options) > 0

    def does_value_match_constraint(self, value_under_question):
        return False

    def is_ready(self, _local_dict):
        return True

    def _get_constrained_data_type(self):
        try:
            if self.is_constraining_column is None:
                return None
        except AttributeError:
            return None
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
            return round((random.random() - 0.5) * expanded_scale) / expanded_precision

        return "#non-value"

    def _assert_column_is_set(self):
        if not self.is_constraining_column:
            raise DataTypeIssueException(f"ERROR: Range Constraint {self.name} need to have set column.")

    def _assert_column_has_data_type(self):
        self._assert_column_is_set()
        if self._get_constrained_data_type() is None:
            raise DataTypeIssueException(
                f"Column {self.is_constraining_column.name} has not defined data type")

    def _assert_proposed_value_is_valid(self, value):
        self._assert_column_has_data_type()
        if not self._get_constrained_data_type().is_value_valid(value):
            raise DataTypeIssueException(
                f"ERROR: Boundary value {value} is not valid for "
                f"data type {self._get_constrained_data_type().name} for constraint {self.name}.")

    def is_constraining_same_column_as(self, _other_constraint: "Constraint"):
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

    def _merge_with(self, right_constraint: "Constraint"):
        self.not_picks.extend(right_constraint.not_picks)
        self.not_matching_regexes.extend(right_constraint.not_matching_regexes)
        return self

    def merge_with(self, right_constraint: "Constraint"):
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

    def toggle_restriction(self, with_name: str = None):
        """ This is a wierd name. This method will make restriction or return internal constraint."""
        if not self.my_restrictor:
            self.my_restrictor = _core.RestrictiveConstraint(name=with_name, restricting_constraint=self)
            self.my_restrictor.is_assigned_to_realization_definition = self.is_assigned_to_realization_definition
        return self.my_restrictor


class RestrictiveConstraint(Constraint):

    def __init__(self, name=None, namespace=None, restricting_constraint=None, **kwargs):
        super().__init__(name=name, namespace=namespace, **kwargs)
        self.restriction_definition = restricting_constraint

    def does_value_match_constraint(self, value_under_question):
        return self.restriction_definition.does_value_match_constraint(value_under_question)

    def toggle_restriction(self, yagni: str = None):
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
        return self  # Keep list as type

    def prepare_relevant_partition_values(self):
        self.partition_relevant_value_options = self.has_picks.copy()

    def _parse_has_pick_to_floats(self):
        parsed_list = []
        for pick in self.has_picks:
            try:
                parsed_list.append(float(pick))
            except ValueError:
                pass
        return parsed_list

    def does_value_match_constraint(self, value_under_question):
        plain_compare = value_under_question in self.has_picks
        if plain_compare:
            return True
        try:
            float_value_under_question = float(value_under_question)
        except ValueError:
            return plain_compare
        floated_picks = self._parse_has_pick_to_floats()
        if len(floated_picks) == 0:
            return plain_compare
        return float_value_under_question in floated_picks


class RegexConstraint(Constraint):
    namespace = _core

    def _generate(self, __yagni):
        generated_value = rstr.xeger(self.has_regex_format)
        return generated_value
        # if self.is_constraining_column is None:
        #     return generated_value

        # if isinstance(self._get_constrained_data_type(), _core.Date):
        #     # to do check if generated is date !!
        #     return generated_value
        #
        # if isinstance(self._get_constrained_data_type(), _core.Decimal):
        #     if not generated_value.isnumeric():
        #         raise Exception(
        #             f"Regex Constraint could not generate number from {self.has_regex_format}")
        #     return generated_value

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

    def __init__(self, name, namespace=None, left_boundary=None, right_boundary=None,
                 is_left_open=False, is_right_open=False, is_constraining_column=None, **kwargs):
        super().__init__(name=name, namespace=namespace, **kwargs)

        if is_constraining_column is not None:
            self.is_constraining_column = is_constraining_column

        # if self._get_constrained_data_type() is not None:
        #     self.precision = self._get_constrained_data_type().has_precision
        #     self.scale = self._get_constrained_data_type().has_scale
        if not self._get_constrained_data_type():
            return

        if not self._has_defined_left_boundary() and left_boundary is not None:
            self.set_left_boundary(left_boundary, is_left_open)

        if not self._has_defined_right_boundary() and right_boundary is not None:
            self.set_right_boundary(right_boundary, is_right_open)

        self._prepare_min_max()

    def _has_defined_left_boundary(self):
        return "has_left_boundary" in [p.get_name() for p in self.get_properties()]

    def _has_defined_right_boundary(self):
        return "has_right_boundary" in [p.get_name() for p in self.get_properties()]

    def _assert_proposed_boundary_value_is_valid(self, value, boundary_value):
        self._assert_column_has_data_type()
        try:
            self._assert_proposed_value_is_valid(value)
        except DataTypeIssueException as internal_error:
            raise DataTypeIssueException(
                f"ERROR: {boundary_value} boundary value {value} is not valid for "
                f"data type {self._get_constrained_data_type().name} for constraint {self.name}.") \
                from internal_error

    def get_maximum_value_for_data_type(self):
        self._assert_column_has_data_type()
        return self._get_constrained_data_type().get_maximum_value()

    def get_minimum_value_for_data_type(self):
        self._assert_column_has_data_type()
        return self._get_constrained_data_type().get_minimum_value()

    def set_left_boundary(self, value, is_open=False):
        self._assert_proposed_boundary_value_is_valid(value, "Proposed left value")
        if is_open:
            self.has_left_boundary = _core.OpenRangeBoundary()
        else:
            self.has_left_boundary = _core.ClosedRangeBoundary()

        self.has_left_boundary.has_boundary_value = \
            self._get_constrained_data_type().parse_if_needed(value)

    def set_right_boundary(self, value, is_open=False):
        self._assert_proposed_boundary_value_is_valid(value, "Proposed right value")
        if is_open:
            self.has_right_boundary = _core.OpenRangeBoundary()
        else:
            self.has_right_boundary = _core.ClosedRangeBoundary()

        self.has_right_boundary.has_boundary_value = \
            self._get_constrained_data_type().parse_if_needed(value)

    def _prepare_min_max(self):
        self._assert_column_has_data_type()

        if not self._has_defined_left_boundary():
            self.set_left_boundary(self._get_constrained_data_type().get_minimum_value())
        if not self._has_defined_right_boundary():
            self.set_right_boundary(self._get_constrained_data_type().get_maximum_value())

    def _assert_range_boundaries_are_valid(self):
        if self.has_left_boundary is None:
            raise Exception(f"ERROR: Left boundary is not defined for Range {self.name}. You set min and max?")
        if self.has_left_boundary is None or self.has_right_boundary is None:
            raise Exception(f"ERROR: Right boundary is not defined for Range {self.name}. You set min and max?")

        if self.has_left_boundary.has_boundary_value > self.has_right_boundary.has_boundary_value:
            raise Exception(f"ERROR: Left boundary is greater then right for Range {self.name}.")

        self._assert_proposed_boundary_value_is_valid(self.has_right_boundary.has_boundary_value, "Right")
        self._assert_proposed_boundary_value_is_valid(self.has_left_boundary.has_boundary_value, "Left")

        if self.has_left_boundary.has_boundary_value == self.has_right_boundary.has_boundary_value and \
                (
                        not isinstance(self.has_left_boundary, _core.ClosedRangeBoundary) or
                        not isinstance(self.has_right_boundary, _core.ClosedRangeBoundary)
                ):
            raise Exception(f"ERROR: Left boundary is equal to right for Range {self.name}.")

    def _get_minimum_viable_value(self):
        min_viable = self.has_left_boundary.has_boundary_value
        if isinstance(self.has_left_boundary, _core.OpenRangeBoundary):
            min_viable += self._get_constrained_data_type().get_minimal_increment_value()
        return min_viable

    def _get_maximum_viable_value(self):
        max_viable = self.has_right_boundary.has_boundary_value
        if isinstance(self.has_right_boundary, _core.OpenRangeBoundary):
            max_viable -= self._get_constrained_data_type().get_minimal_increment_value()
        return max_viable

    def _generate(self, __yagni=None):
        self._prepare_min_max()
        self._assert_range_boundaries_are_valid()

        if self._get_minimum_viable_value() < self._get_constrained_data_type().get_minimum_value():
            raise Exception(f"ERROR: Set left limit outside of precision "
                            f"for column {self.is_constraining_column.name}")

        if self._get_maximum_viable_value() > self._get_constrained_data_type().get_maximum_value():
            raise Exception(f"ERROR: Set right limit outside of decimal precision "
                            f"for column {self.is_constraining_column.name}")
        return self._get_constrained_data_type().generate_for_closed_range(
            self._get_minimum_viable_value(), self._get_maximum_viable_value())

    def left_limit(self):
        self._prepare_min_max()
        return self.has_left_boundary.has_boundary_value

    def right_limit(self):
        self._prepare_min_max()
        return self.has_right_boundary.has_boundary_value

    def _merge_with(self, right_constraint):
        self._prepare_min_max()
        if right_constraint.is_regex:
            raise MergingException("ERROR: Cannot merge regex with range in deterministic fashion.")

        if right_constraint.is_list:
            raise Exception("ERROR: You should not merge list to range!")

        if not right_constraint.is_range:
            raise Exception("ERROR: Right constraint of unknown type.")

        if (right_constraint.has_left_boundary and
            self.has_left_boundary.has_boundary_value < right_constraint.has_left_boundary.has_boundary_value
        ):
            self.has_left_boundary = right_constraint.has_left_boundary

        if (right_constraint.has_right_boundary
            and self.has_left_boundary.has_boundary_value == right_constraint.has_left_boundary.has_boundary_value
            and not isinstance(self.has_left_boundary, _core.ClosedRangeBoundary)
            and isinstance(right_constraint.has_left_boundary, _core.ClosedRangeBoundary)
        ):
            self.has_left_boundary = right_constraint.has_left_boundary

        if (right_constraint.has_right_boundary and
            right_constraint.has_right_boundary.has_boundary_value < self.has_right_boundary.has_boundary_value
        ):
            self.has_right_boundary = right_constraint.has_right_boundary

        if (right_constraint.has_right_boundary
            and self.has_right_boundary.has_boundary_value == right_constraint.has_right_boundary.has_boundary_value
            and not isinstance(self.has_right_boundary, _core.ClosedRangeBoundary)
            and isinstance(right_constraint.has_right_boundary, _core.ClosedRangeBoundary)
        ):
            self.has_right_boundary = right_constraint.has_right_boundary

        self._assert_range_boundaries_are_valid()

        super()._merge_with(right_constraint)
        return self

    def prepare_relevant_partition_values(self):
        self._assert_range_boundaries_are_valid()

        min_value = self._get_minimum_viable_value()
        max_value = self._get_maximum_viable_value()
        non_boundary_value = None
        try:
            non_boundary_value = self.__generate_not_boundary_value()
        except ValueGenerationException:
            pass

        self.partition_relevant_value_options = [self._get_minimum_viable_value()]
        if non_boundary_value:
            self.partition_relevant_value_options.append(non_boundary_value)
        if max_value > min_value:
            self.partition_relevant_value_options.append(max_value)

    def __generate_not_boundary_value(self):
        loop = 0
        while loop < 100:
            loop += 1
            chosen_number = self._generate()

            _is_meeting_left = False
            if isinstance(self.has_left_boundary, _core.ClosedRangeBoundary):
                _is_meeting_left = self.has_left_boundary.has_boundary_value < chosen_number
            else:
                _is_meeting_left = self._get_minimum_viable_value() < chosen_number

            _is_meeting_left = (self.has_left_boundary.has_boundary_value < chosen_number)

            _is_meeting_right = False
            if isinstance(self.has_right_boundary, _core.ClosedRangeBoundary):
                _is_meeting_right = chosen_number < self.has_right_boundary.has_boundary_value
            else:
                _is_meeting_right = chosen_number < self._get_maximum_viable_value()

            if _is_meeting_left and _is_meeting_right:
                return chosen_number

        raise ValueGenerationException(f"ERROR: {self.name} could not generate non boundary value.")

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
