import copy
from random import random

# Invert negation to compliment set
# negate != invert that class is actually inversion factory
from owlready2 import sync_reasoner_pellet


class ConstraintInverter:
    core = None
    
    def __init__(self, _core):
        self.core = _core

    def invert(self, constraint_or_constraint_group):
        if isinstance(constraint_or_constraint_group, self.core.ValueDependency):
            return self._invert_dependency_constraint(constraint_or_constraint_group)
        if isinstance(constraint_or_constraint_group, self.core.RangeConstraint):
            return self._invert_range_constraint(constraint_or_constraint_group)
        if isinstance(constraint_or_constraint_group, self.core.Constraint):
            return self._invert_basic_constraint(constraint_or_constraint_group)
        if isinstance(constraint_or_constraint_group, self.core.ConstraintGroup):
            return self._invert_constraint_group(constraint_or_constraint_group)

        return None

    def _invert_dependency_constraint(self, dependency):
        container_group = self.core.ConstraintGroup(f"temp_{round(random() * 100000)}")
        container_group.change_to_or_operator()
        #container_group.is_a.append(self.core.OrGroup)
        container_group.has_constraints = []

        inverted_dependency = None
        if isinstance(dependency, self.core.GreaterOrEqualThenDependency):
            inverted_dependency = self.core.SmallerThenDependency()

        elif isinstance(dependency, self.core.SmallerThenDependency):
            inverted_dependency = self.core.GreaterOrEqualThenDependency()

        elif isinstance(dependency, self.core.SmallerOrEqualThenDependency):
            inverted_dependency = self.core.GreaterThenDependency()

        elif isinstance(dependency, self.core.GreaterThenDependency):
            inverted_dependency = self.core.SmallerOrEqualThenDependency()

        elif isinstance(dependency, self.core.EqualToDependency):
            inverted_dependency = self.core.EqualToDependency()
            if not isinstance(dependency, self.core.Negation):
                inverted_dependency.is_a.append(self.core.Negation)

        elif isinstance(dependency, self.core.FormatDependency):
            inverted_dependency = self.core.FormatDependency()
            if not isinstance(dependency, self.core.Negation):
                inverted_dependency.is_a.append(self.core.Negation)

        container_group.has_constraints.append(inverted_dependency)

        inverted_dependency.is_constraining_column = dependency.is_constraining_column
        if dependency.is_depending_on_column:
            inverted_dependency.is_depending_on_column = dependency.is_depending_on_column

        if dependency.has_format_definition:
            inverted_dependency.has_format_definition = dependency.has_format_definition

        # sync_reasoner_pellet(infer_property_values=True)

        return container_group

    def _invert_range_constraint(self, range_constraint):
        container_group = self.core.ConstraintGroup(f"temp_{round(random() * 100000)}")
        container_group.change_to_or_operator()
        #container_group.is_a.append(self.core.OrGroup)
        container_group.has_constraints = list()

        if range_constraint.right_limit() < range_constraint.get_maximum_value_for_data_type():
            negated_right_part_constraint = self.core.RangeConstraint(f"temp_{round(random() * 100000)}")
            negated_right_part_constraint.is_constraining_column = range_constraint.is_constraining_column
            negated_right_part_constraint.set_left_boundary(
                range_constraint.right_limit(),
                is_open=isinstance(range_constraint.has_right_boundary, self.core.ClosedRangeBoundary)
            )
            container_group.has_constraints.append(negated_right_part_constraint)

        if range_constraint.left_limit() > range_constraint.get_minimum_value_for_data_type():
            negated_left_part_constraint = self.core.RangeConstraint(f"temp_{round(random() * 100000)}")
            negated_left_part_constraint.is_constraining_column = range_constraint.is_constraining_column
            negated_left_part_constraint.set_right_boundary(
                range_constraint.left_limit(),
                is_open=isinstance(range_constraint.has_left_boundary, self.core.ClosedRangeBoundary)
            )
            container_group.has_constraints.append(negated_left_part_constraint)

        return container_group

    def _invert_basic_constraint(self, constraint):
        container_group = self.core.ConstraintGroup(f"temp_{round(random()*100000)}")
        container_group.change_to_or_operator()
        #container_group.is_a.append(self.core.OrGroup)

        inverted_constraint = constraint.toggle_restriction()
        container_group.has_constraints = [inverted_constraint]
        return container_group

    def _invert_constraint_group(self, constraint_group):

        container_group = self.core.ConstraintGroup(f"temp_{round(random() * 100000)}")
        container_group.has_constraints = list()

        if isinstance(constraint_group, self.core.OrGroup):
            container_group.is_a.append(self.core.AndGroup)
        else:
            container_group.is_a.append(self.core.OrGroup)

        for constraint in constraint_group.has_constraints:
            negated_constraint = self.invert(constraint)
            both_or_groups = isinstance(container_group, self.core.OrGroup) and \
                             isinstance(negated_constraint, self.core.OrGroup)
            both_and_groups = isinstance(container_group, self.core.AndGroup) and \
                              isinstance(negated_constraint, self.core.AndGroup)

            negated_group_has_single_constraint = len(negated_constraint.has_constraints) == 1
            if both_or_groups or both_and_groups:
                if not negated_group_has_single_constraint:
                    container_group.has_constraints.extend(negated_constraint.has_constraints)
                else:
                    container_group.has_constraints.append(negated_constraint.has_constraints[0])
            else:
                if not negated_group_has_single_constraint:
                    container_group.contains_constraint_groups.append(negated_constraint)
                else:
                    container_group.has_constraints.append(negated_constraint.has_constraints[0])

        container_group.unify_constraints()
        return container_group

