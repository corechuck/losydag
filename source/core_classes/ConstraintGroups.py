from collections import defaultdict

import rstr
import random
from owlready2 import Thing, sync_reasoner_pellet
from utils.utils import _supervise_constraint_generation, _merge_groups_left_prio


def extend_core(_core):

    class ConstraintGroup(Thing):
        namespace = _core
        
        def fulfill_constraints(self):
            list_of_constraints = self.has_constraints
            return f"{self.name} has {len(list_of_constraints)} constraints."

        def compliment_with(self, _other_constraint_group):
            self.has_constraints = _merge_groups_left_prio(self, _other_constraint_group)
            
        def merge_with_override(self, _other_constraint_group):
            self.has_constraints = _merge_groups_left_prio(_other_constraint_group, self)

        @property
        def names_of_constrained_columns(self):
            return [const.is_constraining_column.name for const in self.has_constraints]

        @property
        def has_dependencies(self):
            return list(filter(lambda cons: isinstance(cons, _core.ValueDependency), self.has_constraints))

        @property
        def is_having_external_dependencies(self):
            return any(map(lambda const: const.is_externally_dependent, self.has_dependencies))

        def _is_constraining_single_table(self):
            if len(self.is_constraining_tables) == 1:
                return True

            is_same = True
            first_table_name = self.is_constraining_tables[0].name
            for suspect_table in self.is_constraining_tables:
                is_same = is_same and suspect_table.name == first_table_name

            return is_same

        @property
        def constraints_table(self):
            if len(self.is_constraining_tables) == 0:
                return None

            self._is_constraining_single_table()
            return self.is_constraining_tables[0]

        def unify_constraints(self):

            column_to_merged_constraint = dict()
            for constraint in self.has_constraints:
                column_name = constraint.is_constraining_column.name
                if column_name not in column_to_merged_constraint:
                    column_to_merged_constraint[column_name] = constraint
                else:
                    left_constraint = column_to_merged_constraint[column_name]
                    column_to_merged_constraint[column_name] = left_constraint.merge_with(constraint)
            self.has_constraints = list(column_to_merged_constraint.values())

        def convert_to_realization_definition(self):
            if not self._is_constraining_single_table():
                raise Exception(f"ERROR: Group {self.name} constraints more then one table. Should only one.")
            self.unify_constraints()
            self.is_a.append(_core.RealizationDefinition)
            self.compliment_with_min_reqs()

        def build_realization_case(self):
            table_to_group_cache = defaultdict(_core.ConstraintGroup)
            for constraint_under in self.has_constraints:
                tbl_name = constraint_under.is_constraining_column.is_part_of_table.name
                table_to_group_cache[tbl_name].has_constraints.append(constraint_under)

            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

            for future_realization_def in table_to_group_cache.values():
                future_realization_def.convert_to_realization_definition()

            realization_case = _core.RealizationCase(f"made_case_from_{self.name}", _core)
            realization_case.contains_realizations = list(table_to_group_cache.values())
            return realization_case

    class RealizationDefinition(Thing):
        namespace = _core
        _return_dict = dict()
        has_realized_constraints = False

        def __init__(self, name, namespace):
            super().__init__(name, namespace)
            self.compliment_with_min_reqs()

        def compliment_with_min_reqs(self):
            if len(self.has_constraints) > 0:
                self.compliment_with(self.constraints_table.has_min_reqs)

        @property
        def is_ready(self):
            part_list = []
            for const in self.has_dependencies:
                if const.is_externally_dependent:
                    part_list.append(const.is_external_dependency_ready)
            return all(part_list)

        def get_referred_tables(self):
            li = set()
            for c in self.has_dependencies:
                ref_table = c.get_reffered_table()
                if ref_table:
                    li.add(ref_table)
            return li

        def prepare_external_dependencies_with_single_realization_definition(self, _table_to_def_dict):
            for dependency in self.has_dependencies:
                has_been_set = True
                if dependency.is_externally_dependent and not dependency.is_depending_on_realization:
                    has_been_set = dependency.set_missing_realization_definition(_table_to_def_dict)
                if not has_been_set:
                    raise Exception(
                        f"ERROR: Constraint {dependency.name} have external dependency "
                        f"and no realization definition could be chosen from {_table_to_def_dict}. "
                        "Verify setup of this constraint.")
        
        def fulfill_constraints_renew(self):
            self._return_dict = dict()
            self.has_realized_constraints = False
            return self.fulfill_constraints()
        
        def fulfill_constraints(self):
            if self.has_realized_constraints:
                return self._return_dict

            if not self._is_constraining_single_table():
                print("ERROR: Realization def should be defined for one table." 
                      "TODO: serious exception!")

            self._prepare_return_dict()

            # Heavy lifting
            self.has_realized_constraints = (
                _supervise_constraint_generation(
                    self._try_generating_for_all_constraints, 
                    f"RD {self.name}"
                    )
            )
            return self._return_dict

        def clear_results(self):
            self.has_realized_constraints = False
            self._return_dict = dict()

        def _prepare_return_dict(self):
            if len(self._return_dict) > 0 or self.constraints_table is None:
                return
            self._return_dict = dict()
            for column in self.constraints_table.has_columns:
                self._return_dict[column.plain_name] = None

        def _try_generating_for_all_constraints(self, not_ready_accumulator):
            for constraint in self.has_constraints:
                if not constraint.is_ready(self._return_dict):
                    if constraint.is_externally_dependent:
                        raise Exception("ERROR: should not be here yet !! External dependencies" 
                                        "should be ready before calling this.")
                    not_ready_accumulator.append(constraint)
                    continue
                # print(f"DEBUG: Generating {constraint.name}")
                if self._return_dict[constraint.is_constraining_column.plain_name] is not None:
                    raise Exception(f"ERROR: Multiple constraints defined for column "
                                    f"{constraint.is_constraining_column.name}. Try unification of constraints.")
                self._return_dict[constraint.is_constraining_column.plain_name] = (
                    constraint.generate(self._return_dict)
                )
