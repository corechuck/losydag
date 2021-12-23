from random import random

# Invert negation to compliment set
# negate != invert that class is actually inversion factory

class ConstraintRestrictor:
    core = None

    def __init__(self, _core):
        self.core = _core


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
        container_group.is_a.append(self.core.OrGroup)
        container_group.has_constraints = [dependency]

        if isinstance(dependency, self.core.GreaterOrEqualThenDependency):
            dependency.is_a.append(self.core.SmallerThenDependency)
            dependency.is_a.remove(self.core.GreaterOrEqualThenDependency)

        elif isinstance(dependency, self.core.SmallerThenDependency):
            dependency.is_a.append(self.core.GreaterOrEqualThenDependency)
            dependency.is_a.remove(self.core.SmallerThenDependency)

        elif isinstance(dependency, self.core.SmallerOrEqualThenDependency):
            dependency.is_a.append(self.core.GreaterThenDependency)
            dependency.is_a.remove(self.core.SmallerOrEqualThenDependency)

        elif isinstance(dependency, self.core.GreaterThenDependency):
            dependency.is_a.append(self.core.SmallerOrEqualThenDependency)
            dependency.is_a.remove(self.core.GreaterThenDependency)

        elif not isinstance(dependency, self.core.Negation):
            dependency.is_a.append(self.core.Negation)
        else:
            dependency.is_a.remove(self.core.Negation)

        return container_group

    def _invert_range_constraint(self, range_constraint):
        container_group = self.core.ConstraintGroup(f"temp_{round(random() * 100000)}")
        container_group.is_a.append(self.core.OrGroup)
        container_group.has_constraints = list()

        if range_constraint.right_limit < range_constraint.get_maximum_value_for_data_type():
            negated_right_part_constraint = self.core.RangeConstraint(f"temp_{round(random() * 100000)}")
            negated_right_part_constraint.is_constraining_column = range_constraint.is_constraining_column
            negated_right_part_constraint.set_left_boundary(
                range_constraint.right_limit,
                is_open=isinstance(range_constraint.has_right_boundary, self.core.ClosedRangeBoundary)
            )
            container_group.has_constraints.append(negated_right_part_constraint)

        if range_constraint.left_limit > range_constraint.get_minimum_value_for_data_type():
            negated_left_part_constraint = self.core.RangeConstraint(f"temp_{round(random() * 100000)}")
            negated_left_part_constraint.is_constraining_column = range_constraint.is_constraining_column
            negated_left_part_constraint.set_right_boundary(
                range_constraint.left_limit,
                is_open=isinstance(range_constraint.has_left_boundary, self.core.ClosedRangeBoundary)
            )
            container_group.has_constraints.append(negated_left_part_constraint)

        # contained_in_range_not_picks_list = \
        #     [v for v in range_constraint.not_picks if range_constraint.has_min_range < v < range_constraint.has_max_range]
        # if len(contained_in_range_not_picks_list) > 0:
        #     negated_part_constraint_internal = self.core.ListConstraint(f"temp_{round(random()*100000)}")
        #     negated_part_constraint_internal.is_constraining_column = range_constraint.is_constraining_column
        #     negated_part_constraint_internal.has_picks = contained_in_range_not_picks_list
        #     container_group.has_constraints.append(negated_part_constraint_internal)

        #container_group.unify_constraints()
        # sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        return container_group

    def _invert_basic_constraint(self, constraint):
        container_group = self.core.ConstraintGroup(f"temp_{round(random()*100000)}")
        container_group.is_a.append(self.core.OrGroup)

        inverted_constraint = constraint.toggle_restriction()
        container_group.has_constraints = [inverted_constraint]

        # # has_picks -> not_picks
        # if len(constraint.has_picks) > 0:
        #     negated_part_constraint = self.core.Constraint(f"temp_{round(random()*100000)}")
        #     negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        #     negated_part_constraint.not_picks = constraint.has_picks.copy()
        #     container_group.has_constraints.append(negated_part_constraint)
        #
        # # not_picks -> has_picks
        # if len(constraint.not_picks) > 0:
        #     negated_part_constraint = self.core.ListConstraint(f"temp_{round(random()*100000)}")
        #     negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        #     negated_part_constraint.has_picks = constraint.not_picks.copy()
        #     container_group.has_constraints.append(negated_part_constraint)
        #
        # # not_matching_regexes -> multiple(RegexConstraint.has_regex_format)
        # if len(constraint.not_matching_regexes) > 0:
        #     for not_matching_regex in constraint.not_matching_regexes:
        #         negated_part_constraint = self.core.RegexConstraint(f"temp_{round(random()*100000)}")
        #         negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        #         negated_part_constraint.has_regex_format = not_matching_regex
        #         container_group.has_constraints.append(negated_part_constraint)
        #
        # # has_regex_format -> not_matching_regexes
        # if constraint.has_regex_format:
        #     negated_part_constraint = self.core.Constraint(f"temp_{round(random()*100000)}")
        #     negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        #     negated_part_constraint.not_matching_regexes = list()
        #     negated_part_constraint.not_matching_regexes.append(constraint.has_regex_format)
        #     container_group.has_constraints.append(negated_part_constraint)
        #
        # container_group.unify_constraints()
        # sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
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
            both_or_groups = isinstance(container_group, self.core.OrGroup) and isinstance(negated_constraint, self.core.OrGroup)
            both_and_groups = isinstance(container_group, self.core.AndGroup) and (
                    isinstance(negated_constraint, self.core.AndGroup) or not isinstance(negated_constraint, self.core.OrGroup)
            )
            negated_group_has_single_constaraint = len(negated_constraint.has_constraints) == 1
            if both_or_groups or both_and_groups or negated_group_has_single_constaraint:
                container_group.has_constraints.extend(negated_constraint.has_constraints)
            else:
                container_group.has_constraints.append(negated_constraint)

        container_group.unify_constraints()
        return container_group

