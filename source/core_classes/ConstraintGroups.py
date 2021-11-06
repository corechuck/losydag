from collections import defaultdict

import rstr
import random
from owlready2 import Thing, sync_reasoner_pellet


from utils.negations_factory import prepare_negation
from utils.utils import _supervise_constraint_generation, _merge_groups_left_prio, ExtensionContext


def extend_core(context: ExtensionContext):
    _core = context.core
    _value_generation_supervisor = context.value_generation_supervisor

    class ConstraintGroup(Thing):
        namespace = context.core

        def __init__(self, name=None, namespace=None):
            super().__init__(name=name, namespace=namespace)
            if not isinstance(self, _core.OrGroup):
                self.is_a.append(_core.AndGroup)
        
        def fulfill_constraints(self):
            list_of_constraints = self.has_constraints
            return f"{self.name} has {len(list_of_constraints)} constraints."

        def compliment_with(self, _other_constraint_group):
            self.has_constraints = _merge_groups_left_prio(self, _other_constraint_group)
            
        def merge_with_override(self, _other_constraint_group):
            self.has_constraints = _merge_groups_left_prio(_other_constraint_group, self)

        def names_of_constrained_columns(self):
            return [const.is_constraining_column.name for const in self.has_constraints]

        def has_dependencies(self):
            return list(filter(lambda cons: isinstance(cons, _core.ValueDependency), self.has_constraints))

        def is_having_external_dependencies(self):
            return any(map(lambda const: const.is_externally_dependent(), self.has_dependencies()))

        def _is_constraining_single_table(self):
            return self.constraints_table() is not None

        def constraints_table(self):
            if len(self.is_constraining_tables) > 1:
                return None

            if len(self.is_constraining_tables) == 0:
                columns = [c.is_constraining_column for c in self.has_constraints]
                tables = []
                for col in columns:
                    if col.is_part_of_table not in tables:
                        tables.append(col.is_part_of_table)
                if len(tables) == 1:
                    return tables[0]
                return None

            return self.is_constraining_tables[0]

        def unify_constraints(self):
            if isinstance(self, _core.OrGroup):
                return

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

        def prepare_relevant_partition_values(self):
            for constraint in self.has_constraints:
                constraint.prepare_relevant_partition_values()

        def make_realizable_list_of_constraints_random(self):
            if isinstance(self, _core.OrGroup):
                main_constraint = random.choice(self.has_constraints)
                returned_list, meta = self.make_realizable_list_of_constraints_for(main_constraint)
                return returned_list, f"{main_constraint.name}, meta"
            else:
                return self.make_realizable_list_of_constraints_for(None)

        # Do I need it ?
        def make_realizable_list_of_constraints_for(self, main_constraint_or_constraint_group):
            """ Well if this is an Or group then main constraint can be a constraint but also a group, so applying or to
            the whole group is not that easy then, some pieces of below coe then can be used. """
            self.checking_logical_operators()

            if isinstance(self, _core.AndGroup):
                return self._make_realizable_from_and_group(None)
            elif isinstance(self, _core.OrGroup):
                return self._make_realizable_from_or_group(main_constraint_or_constraint_group)
            else:
                raise Exception(
                    "ERROR: Well someone added new operator to groups. You have to decide what happens here.")

        def _make_realizable_from_or_group(self, main_constraint_or_constraint_group):
            if not isinstance(self, _core.OrGroup):
                raise Exception("ERROR: Calling a function only for OR groups.")

            aggregated_meta_info = ""
            anded_constraint_list = list()
            negate = prepare_negation(_core)

            for constraint in self.has_constraints:
                if constraint == main_constraint_or_constraint_group:
                    anded_constraint_list.append(main_constraint_or_constraint_group)
                else:
                    negation_result_group = negate(constraint)
                    if isinstance(negation_result_group, _core.OrGroup):
                        self.contains_constraint_groups.append(negation_result_group)
                    else:
                        anded_constraint_list.extend(negation_result_group.has_constraints)

            for child_constraint_group in self.contains_constraint_groups:
                if child_constraint_group != main_constraint_or_constraint_group:
                    processing_group = negate(child_constraint_group)
                else:
                    processing_group = child_constraint_group

                random_main_constraint = random.choice(processing_group.has_constraints)
                aggregated_meta_info = f"{aggregated_meta_info}, chosen {random_main_constraint.name}"
                child_result, meta_info = \
                    processing_group.make_realizable_list_of_constraints_for(random_main_constraint)
                if meta_info:
                    aggregated_meta_info = f"{aggregated_meta_info}, {meta_info}"
                anded_constraint_list.extend(child_result)

            return anded_constraint_list, aggregated_meta_info

        def _make_realizable_from_and_group(self, not_needed_constraint_for_and_group):
            if not isinstance(self, _core.AndGroup):
                raise Exception("ERROR: Calling a function only for AND groups.")
            anded_constraint_list = self.has_constraints.copy()
            aggregated_meta_info = ""
            for child_constraint_group in self.contains_constraint_groups:
                random_main_constraint = random.choice(child_constraint_group.has_constraints)
                aggregated_meta_info = f"{aggregated_meta_info}, chosen {random_main_constraint.name}"
                child_result, meta_info = \
                    child_constraint_group.make_realizable_list_of_constraints_for(random_main_constraint)
                anded_constraint_list.extend(child_result)
            return anded_constraint_list, aggregated_meta_info

    class RealizationDefinition(Thing):
        namespace = _core
        _return_dict = dict()
        has_realized_constraints = False
        original_constraints = None

        def __init__(self, name=None, namespace=None):
            super().__init__(name=name, namespace=namespace)

        def prepare_for_realization(self):
            self._prepare_return_dict()
            self.compliment_with_min_reqs()

        def compliment_with_min_reqs(self):
            if len(self.has_constraints) > 0:
                self.original_constraints = self.has_constraints.copy()  # this should NOT be here
                # that should use something like has_work_constraints
                self.compliment_with(self.constraints_table().has_min_reqs)

        def is_ready(self):
            part_list = []
            for const in self.has_dependencies():
                if const.is_externally_dependent():
                    part_list.append(const.is_external_dependency_ready())
            return all(part_list)

        def get_referred_tables(self):
            li = set()
            for c in self.has_dependencies():
                ref_table = c.get_referred_table()
                if ref_table:
                    li.add(ref_table)
            return li

        def prepare_external_dependencies_with_single_realization_definition(self, _table_to_def_dict):
            for dependency in self.has_dependencies():
                has_been_set = True
                if dependency.is_externally_dependent() and not dependency.is_depending_on_realization:
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

            self.prepare_for_realization()

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
            if len(self._return_dict) > 0 or self.constraints_table() is None:
                return
            self._return_dict = dict()
            self._fulfilled_constraints = list()
            for column in self.constraints_table().has_columns:
                self._return_dict[column.plain_name] = None

        def _try_generating_for_all_constraints(self, not_ready_accumulator):
            for constraint in self.has_constraints:
                if not constraint.is_ready(self._return_dict):
                    if constraint.is_externally_dependent():
                        raise Exception("ERROR: should not be here yet !! External dependencies" 
                                        "should be ready before calling this.")
                    not_ready_accumulator.append(constraint)
                    continue

                if self._return_dict[constraint.is_constraining_column.plain_name] is None:
                    # self._return_dict[constraint.is_constraining_column.plain_name] = (
                    #     constraint.generate(self._return_dict)
                    # )
                    self._return_dict[constraint.is_constraining_column.plain_name] = (
                        _value_generation_supervisor.generate(
                            constraint, self.get_sibling_restrictive_constraints(constraint), self._return_dict)
                    )
                    self._fulfilled_constraints.append(constraint.name)

                elif constraint.name not in self._fulfilled_constraints:
                    raise Exception(f"ERROR: Multiple constraints defined for column "
                                    f"{constraint.is_constraining_column.name}. Try unification of constraints.")

        def get_sibling_restrictive_constraints(self, constraint):
            return [
                restrictive_constraint
                for restrictive_constraint in self.has_restricting_constraints
                if restrictive_constraint.is_constraining_column.plain_name ==
                constraint.is_constraining_column.plain_name
            ]

        def prepare_relevant_partition_values(self):
            for constraint in self.original_constraints:
                constraint.prepare_relevant_partition_values()

        def has_more_relevant_options(self):
            return any([constraint.has_more_relevant_options() for constraint in self.has_constraints])

        def convert_to_positive_cases(self):
            # 1. Break down OR groups with not second branches -> list of groups with negated recursively groups
            # 2. Merge groups
            # 3. Convert to Realization cases
            # 4. Return
            # prepare_relevant_partition_values
            pass

        def convert_to_negative_cases(self):
            # 1. for each constraint negate it and make new group out of it recursively
            # 2. Merge groups
            # 3. Convert to Realization cases
            # 4. Return
            pass
