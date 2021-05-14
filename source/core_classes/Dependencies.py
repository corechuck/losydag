from owlready2 import Thing
import string
import rstr

def extend_core(_core):
    _compound_keys_tracker = dict()
    _generation_formatter = GenerationTrackingFormatter(_compound_keys_tracker)

    class ValueDependency(Thing):
        namespace = _core

        def is_ready(self, _local_dict):
            "This should tell if data has already been gereated from dependent relalization."
            if not self.is_externally_dependent:
                return self._is_local_dependency_ready(_local_dict)
            else:
                return self.is_depending_on_realization.has_realized_constraints
            
            # return (
            #     self.is_depending_on_realization is not None and 
            #     self.is_depending_on_realization.has_realized_constraints
            # ) or (
            #     self.is_depending_on_realization is None and 
            #     self._is_local_dependency_ready(_local_dict)
            # )
        
        @property
        def is_externally_dependent(self):
            return (
                self.is_depending_on_column is not None and
                self.is_depending_on_column.is_part_of_table.name != 
                    self.is_constraining_column.is_part_of_table.name
            )

        def get_reffered_table(self):
            if not self.is_externally_dependent:
                return None
            else:
                return self.is_depending_on_column.is_part_of_table 
                    
        def _generate(self, _local_dict):
            if not self.is_externally_dependent:
                if not self._is_local_dependency_ready(_local_dict):
                    raise Exception(f"ERROR: Dependency {self.name} not ready. "
                        "That should never happen. Between isReady and generate something changed.")

                return _local_dict[self.is_depending_on_column.plain_name]

            if self.is_externally_dependent:
                from_column_name = self.is_depending_on_column.plain_name
                if not self.is_depending_on_realization.has_realized_constraints:
                    raise Exception(f"ERROR: Dependency {self.name} not ready. "
                        "That should never happen. Between isReady and generate something changed.")
                return self.is_depending_on_realization._return_dict[from_column_name]

        def _is_local_dependency_ready(self, _local_dict):
            col_name = self.is_depending_on_column.plain_name
            return col_name in _local_dict and _local_dict[col_name] is not None

        def set_missing_realization_definition(self, _table_to_def_dict):
            needed_table_name = self.is_depending_on_column.is_part_of_table.name
            can_use = needed_table_name in _table_to_def_dict
            if can_use:
                self.is_depending_on_realization = _table_to_def_dict[needed_table_name]
            return can_use


    class FormatDependency(Thing):
        namespace = _core

        def _is_local_dependency_ready(self, _local_dict):
            checking_dict = CheckingDictFormatter()
            checking_dict.format(self.has_format_definition, **_local_dict)
            return checking_dict.has_all_values_ready()

        def _generate(self, _local_dict):
            _generation_formatter.set_increment(self)
            resolved_format = _generation_formatter.format(self.has_format_definition, **_local_dict)
            return rstr.xeger(resolved_format)

class GenerationTrackingFormatter(string.Formatter):

    def __init__(self, _tracker):
        self.not_ready_columns = list()
        self.tracker = _tracker

    # def __format__(self, spec):
    def format_field(self, value, spec):
        intu = 0
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
        
    # def __getitem__(self, name):
    def get_field(self, field_name, args, kwargs):
        _passed_dict = kwargs  # I dont care about other for now or ever.

        if "autoincrement" == field_name:
            return self.__increment_and_return_set_column(), field_name

        return _passed_dict[field_name], field_name


class CheckingDictFormatter(string.Formatter):

    def __init__(self):
        self.not_ready_columns = list()

    # def __format__(self, spec):
    def format_field(self, value, spec):
        intu = 0
        return value

    # def __getitem__(self, name):
    def get_field(self, field_name, args, kwargs):
        _passed_dict = kwargs  # I dont care about other for now or ever.

        if "autoincrement" == field_name:
            return "0",field_name
        if field_name not in _passed_dict.keys():
            raise Exception(f"ERROR: referenced in format not existing key {field_name}")
        if _passed_dict[field_name] is None:
            self.not_ready_columns.append(field_name)
            return "~",field_name
        return _passed_dict[field_name],field_name

    def has_all_values_ready(self):
        return len(self.not_ready_columns) == 0
            
