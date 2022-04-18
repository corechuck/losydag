from random import random

from owlready2 import Thing
import string
import rstr

from utils.context import ExtensionContext
from utils.utils import DataTypeIssueException


def extend_core(context: ExtensionContext):
    _core = context.core
    _compound_keys_tracker = dict()
    _generation_formatter = GenerationTrackingFormatter(_compound_keys_tracker)

    class ValueDependency(Thing):
        namespace = _core
        can_handle_string_to_string = True
        outbound_data_type = None

        def is_ready(self, _local_dict):
            """ This should tell if refferenced data is prepared and this can be generated. """
            if not self.is_externally_dependent():
                return self._is_local_dependency_ready(_local_dict)
            else:
                return self.is_depending_on_realization.has_realized_constraints

        def is_externally_dependent(self):
            return (
                    self.is_depending_on_column is not None and
                    self.is_depending_on_column.is_part_of_table.name !=
                    self.is_constraining_column.is_part_of_table.name
            )

        def is_external_dependency_ready(self):
            if not self.is_externally_dependent():
                print("WARN: You sure? checking external dependency readiness for internal dependency !")
            return self.is_depending_on_realization.has_realized_constraints

        def get_referred_table(self):
            if not self.is_externally_dependent():
                return None
            else:
                return self.is_depending_on_column.is_part_of_table

        def generate(self, local_dict):
            self._assert_column_has_data_type()
            self.outbound_data_type = self._get_constrained_data_type()
            generated_value = self._generate(local_dict)
            self._assert_proposed_value_is_valid(generated_value)
            return self.outbound_data_type.convert_to_string(generated_value)

        def _generate(self, _local_dict):
            if isinstance(self, _core.Negation):
                # Technically its true that if you have negated dependency for column A, and you put None/Null there
                # Then value is no longer a representation of anything else.
                return None

            self._assert_dependent_column_has_data_type()

            from_column_name = self.is_depending_on_column.plain_name
            if self.is_externally_dependent():
                if not self.is_depending_on_realization.has_realized_constraints:
                    raise Exception(f"ERROR: Dependency {self.name} not ready. "
                                    "That should never happen. Between isReady and generate something changed.")

                from_value = self.is_depending_on_realization._return_dict[from_column_name]
            else:  # is local
                if not self._is_local_dependency_ready(_local_dict):
                    raise Exception(f"ERROR: Dependency {self.name} not ready. "
                                    "That should never happen. Between isReady and generate something changed.")
                from_value = _local_dict[from_column_name]

            converting_data_type = self.is_depending_on_column.has_data_type
            if isinstance(converting_data_type, _core.Varchar):
                if isinstance(self.is_constraining_column.has_data_type, _core.Varchar):
                    if not self.can_handle_string_to_string:
                        raise DataTypeIssueException(
                            "ERROR: Cannot generate dependent value, because "
                            "from column and to column are strings for {self.name} ")
                else:
                    converting_data_type = self.is_constraining_column.has_data_type

            if converting_data_type.is_value_valid(from_value):
                dependent_numeric_value = converting_data_type.parse_if_needed(from_value)
            else:
                raise DataTypeIssueException(
                    f"ERROR: Dependent value '{from_value}' cannot be converted by data type {converting_data_type} "
                    f"for dependency {self.name}.")

            data_type_defined_column = self.is_constraining_column
            if isinstance(self.is_constraining_column.has_data_type, _core.Varchar):
                data_type_defined_column = self.is_depending_on_column

            self.outbound_data_type = data_type_defined_column.has_data_type
            return self._generate_dependency(
                _local_dict, from_column_name, dependent_numeric_value, data_type_defined_column)

        def _generate_dependency(
                self, _local_dict, from_column_name, dependent_parsed_value, data_type_defined_column):
            return dependent_parsed_value

        def _is_local_dependency_ready(self, _local_dict):
            col_name = self.is_depending_on_column.plain_name
            return col_name in _local_dict and _local_dict[col_name] is not None

        def set_missing_realization_definition(self, _table_to_def_dict):
            needed_table_name = self.is_depending_on_column.is_part_of_table.name
            can_use = needed_table_name in _table_to_def_dict
            if can_use:
                self.is_depending_on_realization = _table_to_def_dict[needed_table_name]
            return can_use

        def _assert_dependent_column_has_data_type(self):
            if self.is_depending_on_column is not None and self.is_depending_on_column.has_data_type is None:
                raise DataTypeIssueException(
                    f"Column {self.is_depending_on_column.name} has not defined data type")

    class FormatDependency(ValueDependency):
        namespace = _core
        can_handle_string_to_string = False

        def _is_local_dependency_ready(self, _local_dict):
            checking_dict = CheckingDictFormatter()
            checking_dict.format(self.has_format_definition, **_local_dict)
            return checking_dict.has_all_values_ready

        def _generate(self, _local_dict):
            _generation_formatter.set_increment(self)
            resolved_format = _generation_formatter.format(self.has_format_definition, **_local_dict)
            # return rstr.xeger(resolved_format)
            return resolved_format

    class SmallerThenDependency(ValueDependency):
        namespace = _core
        can_handle_string_to_string = False

        def _generate_dependency(
                self, _local_dict, from_column_name, dependent_parsed_value, data_type_defined_column):
            converted_range = _core.RangeConstraint(
                f"range_from_external_dependency_of_{from_column_name}_{round(random() * 100000)}",
                right_boundary=dependent_parsed_value,
                is_right_open=True,
                is_constraining_column=data_type_defined_column)
            generated_value = converted_range._generate()
            return generated_value

    class SmallerOrEqualThenDependency(ValueDependency):
        namespace = _core
        can_handle_string_to_string = False

        def _generate_dependency(
                self, _local_dict, from_column_name, dependent_parsed_value, data_type_defined_column):
            converted_range = _core.RangeConstraint(
                f"range_from_external_dependency_of_{from_column_name}_{round(random() * 100000)}",
                right_boundary=dependent_parsed_value,
                is_constraining_column=data_type_defined_column)
            generated_value = converted_range._generate()
            return generated_value

    class GreaterThenDependency(ValueDependency):
        namespace = _core
        can_handle_string_to_string = False

        def _generate_dependency(
                self, _local_dict, from_column_name, dependent_parsed_value, data_type_defined_column):
            converted_range = _core.RangeConstraint(
                f"range_from_external_dependency_of_{from_column_name}_{round(random() * 100000)}",
                left_boundary=dependent_parsed_value,
                is_left_open=True,
                is_constraining_column=data_type_defined_column)
            generated_value = converted_range._generate()
            return generated_value

    class GreaterOrEqualThenDependency(ValueDependency):
        namespace = _core
        can_handle_string_to_string = False

        def _generate_dependency(
                self, _local_dict, from_column_name, dependent_parsed_value, data_type_defined_column):
            converted_range = _core.RangeConstraint(
                f"range_from_external_dependency_of_{from_column_name}_{round(random() * 100000)}",
                left_boundary=dependent_parsed_value,
                is_constraining_column=data_type_defined_column)
            generated_value = converted_range._generate()
            return generated_value


class GenerationTrackingFormatter(string.Formatter):

    def __init__(self, _tracker):
        self.not_ready_columns = list()
        self.tracker = _tracker

    def format_field(self, value, spec):
        return value

    def set_increment(self, dependency):
        self.const_table = dependency.is_constraining_column.is_part_of_table.name
        if self.const_table not in self.tracker:
            self.tracker[self.const_table] = dict()

        self.composed_key = "__".join(map(
            lambda c: c.plain_name,
            dependency.has_composed_key_over_columns
        ))
        if self.composed_key not in self.tracker[self.const_table]:
            self.tracker[self.const_table][self.composed_key] = 0

    def __increment_and_return_set_column(self):
        self.tracker[self.const_table][self.composed_key] += 1
        return str(self.tracker[self.const_table][self.composed_key])

    def get_field(self, field_name, args, kwargs):
        _passed_dict = kwargs  # I dont care about other for now or ever.

        if "autoincrement" == field_name:
            return self.__increment_and_return_set_column(), field_name

        return _passed_dict[field_name], field_name


class CheckingDictFormatter(string.Formatter):

    def __init__(self):
        self.not_ready_columns = list()

    def format_field(self, value, spec):
        intu = 0
        return value

    def get_field(self, field_name, args, kwargs):
        _passed_dict = kwargs  # I dont care about other for now or ever.

        if "autoincrement" == field_name:
            return "0", field_name
        if field_name not in _passed_dict.keys():
            self.not_ready_columns.append(field_name)
            return "-", field_name
            # raise Exception(f"ERROR: referenced in format not existing key {field_name}")
        if _passed_dict[field_name] is None:
            self.not_ready_columns.append(field_name)
            return "~", field_name
        return _passed_dict[field_name], field_name

    @property
    def has_all_values_ready(self):
        return len(self.not_ready_columns) == 0
