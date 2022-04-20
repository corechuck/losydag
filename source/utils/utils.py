import string

from owlready2 import OwlReadyInconsistentOntologyError

_verbal = False


def _merge_groups_left_prio(group1, group2):
    """ Left prio means that if group1 and group2 has constraint for same column,
    left-group1 will be taken and group2 not"""

    new_overwritten_list = group1.has_constraints.copy()

    for other_constraint in group2.has_constraints:
        if other_constraint.is_constraining_column.name \
                not in group1.names_of_constrained_columns():
            new_overwritten_list.append(other_constraint)
        
    return new_overwritten_list


def _supervise_constraint_generation(__internal_generation_function_with_leftovers, comment):
    not_ready_constraints = list()
    last_not_ready_constraints = -1
    loop_count = 0
    while True:
        not_ready_constraints = list()
        loop_count += 1
        if _verbal:
            print(f"DEBUG: Supervised generation for {comment}. Try number {loop_count}")
        __internal_generation_function_with_leftovers(not_ready_constraints)

        if last_not_ready_constraints == len(not_ready_constraints):
            raise Exception(f"ERROR: Could not resolve dependencies {not_ready_constraints}")
        
        if len(not_ready_constraints) == 0:
            break
        last_not_ready_constraints = len(not_ready_constraints)
        if _verbal: print(f"DEBUG: Supervised generation. Not resolved dependencies {not_ready_constraints}")

    return True


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


class MergingException(Exception):
    pass


class ValueGenerationException(Exception):
    pass


class NotUnifiedConstraintsException(Exception):
    pass


class DataTypeIssueException(Exception):
    pass


class RealizationDefinitionException(Exception):
    pass


class QueryMissformatException(Exception):
    pass
