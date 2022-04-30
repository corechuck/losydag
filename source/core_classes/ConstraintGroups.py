from datetime import datetime
from collections import defaultdict
import random
from owlready2 import Thing, sync_reasoner_pellet
import utils.context
from utils.invertion_factory import ConstraintInverter
from utils.sentence_processing import MultiplicationSupervisor
from utils.utils import _supervise_constraint_generation, _merge_groups_left_prio, NotUnifiedConstraintsException, \
    RealizationDefinitionException


if not utils.context.core_context\
        or not utils.context.core_context.core\
        or not utils.context.core_context.value_generation_supervisor:
    raise Exception("Cannot import ConstraintGroups without initialized utils.context.core_context")

_core = utils.context.core_context.core
_value_generation_supervisor = utils.context.core_context.value_generation_supervisor


class ConstraintGroup(Thing):
    namespace = _core
    multiplicator = None
    meta = ""
    my_restriction_variations = None
    inverter = None

    def __init__(self, name=None, namespace=None):
        super().__init__(name=name, namespace=namespace)
        if not isinstance(self, _core.OrGroup):
            self.is_a.append(_core.AndGroup)
        self.multiplicator = MultiplicationSupervisor(_core)
        self.inverter = ConstraintInverter(_core)

    def fulfill_constraints(self):
        list_of_constraints = self.has_constraints
        return f"{self.name} has {len(list_of_constraints)} constraints."

    def compliment_with(self, _other_constraint_group):
        self.has_constraints = _merge_groups_left_prio(self, _other_constraint_group)

    def merge_with_override(self, _other_constraint_group):
        self.has_constraints = _merge_groups_left_prio(_other_constraint_group, self)

    def names_of_constrained_columns(self):
        return [const.is_constraining_column.name
                for const in self.has_constraints if not isinstance(const, _core.RestrictiveConstraint)]

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
            columns = list()
            tables = list()
            for cstr in self.has_constraints:
                if isinstance(cstr, _core.RestrictiveConstraint):
                    columns.append(cstr.restricting_column)
                else:
                    columns.append(cstr.is_constraining_column)
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
        restrictive_constraints = list()
        for constraint in self.has_constraints:
            if isinstance(constraint, _core.RestrictiveConstraint):
                restrictive_constraints.append(constraint)
                continue
            column_name = constraint.is_constraining_column.name
            if column_name not in column_to_merged_constraint:
                column_to_merged_constraint[column_name] = constraint
            else:
                left_constraint = column_to_merged_constraint[column_name]
                column_to_merged_constraint[column_name] = left_constraint.merge_with(constraint)
        self.has_constraints = list(column_to_merged_constraint.values())
        self.has_constraints.extend(restrictive_constraints)

    def convert_to_realization_definition(self):
        if not self._is_constraining_single_table():
            raise Exception(f"ERROR: Group {self.name} constraints more then one table. Should only one.")
        self.unify_constraints()
        self.is_a.append(_core.RealizationDefinition)
        self.compliment_with_min_reqs()

    def build_realization_case(self, groups_prefix: str = ""):
        if groups_prefix == "":
            groups_prefix = "RC"
        table_to_group_cache = dict()
        for defined_constraint in self.has_constraints:
            if defined_constraint.is_assigned_to_realization_definition:
                group_name = defined_constraint.is_assigned_to_realization_definition.name
            elif isinstance(defined_constraint, _core.RestrictiveConstraint):
                group_name = defined_constraint.restricting_column.is_part_of_table.name
            else:
                group_name = defined_constraint.is_constraining_column.is_part_of_table.name
            if group_name not in table_to_group_cache:
                table_to_group_cache[group_name] = _core.ConstraintGroup(
                    f"{groups_prefix}__{self.name}__{group_name}", namespace=self.namespace)
            table_to_group_cache[group_name].has_constraints.append(defined_constraint)

        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

        for future_realization_def in table_to_group_cache.values():
            future_realization_def.convert_to_realization_definition()

        realization_case = _core.RealizationCase(f"{groups_prefix}__{self.name}", _core)
        realization_case.contains_realizations = list(table_to_group_cache.values())
        return realization_case

    def prepare_relevant_partition_values(self):
        for constraint in self.has_constraints:
            constraint.prepare_relevant_partition_values()

    def pick_branches_from_or_groups(self):
        flatted_list_of_branch_constraints = list()
        meta_info_list = list()

        # TODO: Write TESTS !
        if isinstance(self, _core.OrGroup):
            random_main_constraint = random.choice(self.has_constraints)
            self.has_constraints.clear()
            self.has_constraints.append(random_main_constraint)
            meta_info_list.append(random_main_constraint.name)

        for group in self.contains_constraint_groups:
            if isinstance(group, _core.OrGroup):
                random_subgroup_constraint = random.choice(group.has_constraints)
                flatted_list_of_branch_constraints.append(random_subgroup_constraint)
                meta_info_list.append(random_subgroup_constraint.name)
            else:
                flatted_list_of_branch_constraints.extend(group.has_constraints)

            child_meta = group.pick_branches_from_or_groups()
            meta_info_list.extend(child_meta)

        if len(meta_info_list) > 0:
            self.has_constraints.extend(flatted_list_of_branch_constraints)
            self.unify_constraints()
        return meta_info_list

    def make_all_restricting_variations(self):
        if self.my_restriction_variations:
            return self.my_restriction_variations

        self.my_restriction_variations = list()
        if isinstance(self, _core.OrGroup):
            new_and_group = _core.ConstraintGroup()
            self.my_restriction_variations.append(new_and_group)
            new_and_group.has_constraints.extend([
                constr.toggle_restriction() for constr in self.has_constraints
            ])
        elif isinstance(self, _core.AndGroup):
            for to_be_breaking_constraint in self.has_constraints:
                new_variation_group = _core.ConstraintGroup()
                new_variation_group.meta = \
                    f"Value in {to_be_breaking_constraint.is_constraining_column.name} " \
                    f"breaking constraint sentence {self.name}"
                for under_process in self.has_constraints:
                    if under_process == to_be_breaking_constraint:
                        new_variation_group.has_constraints.append(under_process.toggle_restriction())
                    else:
                        new_variation_group.has_constraints.append(under_process)
                self.my_restriction_variations.append(new_variation_group)

        if len(self.my_restriction_variations) == 0:
            raise Exception("ERROR: 2o8340ijfos8dy")
        return self.my_restriction_variations

    def merge_my_copy_with_group(self, group_b):
        my_copy = _core.ConstraintGroup(f"{self.name}__merged_with__{group_b.name}")
        my_copy.has_constraints = list()
        my_copy.has_constraints.extend(self.has_constraints)
        my_copy.has_constraints.extend(group_b.has_constraints)
        my_copy.meta = "; ".join([self.meta, group_b.meta])
        return my_copy


    def multiply_list_of_cases_times_group(self, list_of_cases, group):
        multiplied_list = list()
        for case in list_of_cases:
            new_cases = self.multiplicator.multiply_groups(case, group)
            for idx, new_case_constraints in enumerate(new_cases):
                gr = _core.ConstraintGroup(f"M_{idx}__{case.name}__{group.name}")
                gr.has_constraints = new_case_constraints
                gr.meta = "; ".join([case.meta, group.meta])
                multiplied_list.append(gr)
        return multiplied_list


    def is_or_operator(self):
        return isinstance(self, _core.OrGroup)

    def is_and_operator(self):
        return isinstance(self, _core.AndGroup)

    def change_to_or_operator(self):
        if self.is_and_operator():
            self.is_a.append(_core.OrGroup)
            self.is_a.remove(_core.AndGroup)

    def change_to_and_operator(self):
        if self.is_or_operator():
            self.is_a.append(_core.AndGroup)
            self.is_a.remove(_core.OrGroup)

    def toggle_logical_operator(self):
        if self.is_or_operator():
            self.is_a.append(_core.AndGroup)
            self.is_a.remove(_core.OrGroup)

        if self.is_and_operator():
            self.is_a.append(_core.OrGroup)
            self.is_a.remove(_core.AndGroup)


class RealizationDefinition(Thing):
    namespace = _core
    _return_dict = dict()
    has_realized_constraints = False
    original_constraints = None
    is_complimented_with_min_reqs = False

    def __init__(self, name=None, namespace=None):
        super().__init__(name=name, namespace=namespace)

    def prepare_for_realization(self):
        self._prepare_return_dict()
        self.compliment_with_min_reqs()

    def compliment_with_min_reqs(self):
        if len(self.has_constraints) > 0 and not self.is_complimented_with_min_reqs:
            self.original_constraints = self.has_constraints.copy()
            if self.constraints_table().has_min_reqs:
                self.compliment_with(self.constraints_table().has_min_reqs)
            self.is_complimented_with_min_reqs = True

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
            raise RealizationDefinitionException("ERROR: Realization def should be defined for one table.")

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
        generator_constraints = [c for c in self.has_constraints if not isinstance(c, _core.RestrictiveConstraint)]
        for constraint in generator_constraints:
            if not constraint.is_ready(self._return_dict):
                if constraint.is_externally_dependent():
                    raise Exception("ERROR: should not be here yet !! External dependencies"
                                    "should be ready before calling this.")
                not_ready_accumulator.append(constraint)
                continue

            if self._return_dict[constraint.is_constraining_column.plain_name] is None:
                self._return_dict[constraint.is_constraining_column.plain_name] = (
                    _value_generation_supervisor.generate(
                        constraint, self.get_sibling_restrictive_constraints(constraint), self._return_dict)
                )
                self._fulfilled_constraints.append(constraint.name)

            elif constraint.name not in self._fulfilled_constraints:
                raise NotUnifiedConstraintsException(f"ERROR: Multiple constraints defined for column "
                                                     f"{constraint.is_constraining_column.name}. Try unification of constraints.")

    def get_sibling_restrictive_constraints(self, constraint):
        return [
            potentially_restrictive_constraint
            for potentially_restrictive_constraint in self.has_constraints
            if isinstance(potentially_restrictive_constraint, _core.RestrictiveConstraint) and (
                    potentially_restrictive_constraint.restricting_column.plain_name ==
                    constraint.is_constraining_column.plain_name
            )
        ]

    def prepare_relevant_partition_values(self):
        for constraint in self.original_constraints:
            constraint.prepare_relevant_partition_values()

    def has_more_relevant_options(self):
        return any([constraint.has_more_relevant_options() for constraint in self.has_constraints])


