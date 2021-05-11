from owlready2 import Thing


def extend_core(_core, _data_bucket):

    class ValueDependency(Thing):
        namespace = _core

        def is_ready(self, _local_dict):
            "This should tell if data has already been gereated from dependent relalization."
            return (
                self.is_depending_on_realization is None and 
                self._is_local_dependency_ready(_local_dict)
            ) or self.is_depending_on_realization.has_realized_constraints

            # return _data_bucket[self.is_depending_on_column.is_part_of_table.name] \
            #     [self.is_depending_on_realization.name] is not None
                    
        def _generate(self, _local_dict):
            if not self._is_local_dependency_ready(_local_dict):
                print("ERROR: That should never happen. Between isReady and generate something changed.")

            return _local_dict[self.is_depending_on_column.name]

        def _is_local_dependency_ready(self, _local_dict):
            col_name = self.is_depending_on_column.name
            return col_name in _local_dict and _local_dict[col_name] is not None