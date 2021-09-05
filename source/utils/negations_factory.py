from datetime import datetime
from random import random

from owlready2 import sync_reasoner_pellet

from core_classes.Constraints import MAX_RANGE, MIN_RANGE


def prepare_negation(_core):
    def negate(constraint_or_constraint_group):
        if isinstance(constraint_or_constraint_group, _core.RangeConstraint):
            return _negate_range_constraint(constraint_or_constraint_group, _core)
        if isinstance(constraint_or_constraint_group, _core.Constraint):
            return _negate_basic_constraint(constraint_or_constraint_group, _core)
        if isinstance(constraint_or_constraint_group, _core.ConstraintGroup):
            return _negate_constraint_group(constraint_or_constraint_group, _core)

        return None
    return negate


def _negate_range_constraint(range_constraint, _core):
    container_group = _core.ConstraintGroup(f"temp_{round(random() * 100000)}")
    container_group.is_a.append(_core.OrGroup)
    container_group.has_constraints = list()

    if range_constraint.has_max_range < MAX_RANGE:
        negated_part_constraint = _core.RangeConstraint(f"temp_{round(random() * 100000)}")
        negated_part_constraint.is_constraining_column = range_constraint.is_constraining_column
        negated_part_constraint.has_min_range = range_constraint.has_max_range
        negated_part_constraint.not_picks = []
        if range_constraint.has_max_range not in range_constraint.not_picks:
            negated_part_constraint.not_picks = [range_constraint.has_max_range]
        container_group.has_constraints.append(negated_part_constraint)

    if range_constraint.has_min_range > MIN_RANGE:
        negated_part_constraint = _core.RangeConstraint(f"temp_{round(random() * 100000)}")
        negated_part_constraint.is_constraining_column = range_constraint.is_constraining_column
        negated_part_constraint.has_max_range = range_constraint.has_min_range
        negated_part_constraint.not_picks = []
        if range_constraint.has_min_range not in range_constraint.not_picks:
            negated_part_constraint.not_picks = [range_constraint.has_min_range]
        container_group.has_constraints.append(negated_part_constraint)

    contained_in_range_not_picks_list = \
        [v for v in range_constraint.not_picks if range_constraint.has_min_range < v < range_constraint.has_max_range]
    if len(contained_in_range_not_picks_list) > 0:
        negated_part_constraint_internal = _core.ListConstraint(f"temp_{round(random()*100000)}")
        negated_part_constraint_internal.is_constraining_column = range_constraint.is_constraining_column
        negated_part_constraint_internal.has_picks = contained_in_range_not_picks_list
        container_group.has_constraints.append(negated_part_constraint_internal)

    container_group.unify_constraints()
    # sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    return container_group


def _negate_basic_constraint(constraint, _core):
    container_group = _core.ConstraintGroup(f"temp_{round(random()*100000)}")
    container_group.is_a.append(_core.OrGroup)
    container_group.has_constraints = list()

    # has_picks -> not_picks
    if len(constraint.has_picks) > 0:
        negated_part_constraint = _core.Constraint(f"temp_{round(random()*100000)}")
        negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        negated_part_constraint.not_picks = constraint.has_picks.copy()
        container_group.has_constraints.append(negated_part_constraint)

    # not_picks -> has_picks
    if len(constraint.not_picks) > 0:
        negated_part_constraint = _core.ListConstraint(f"temp_{round(random()*100000)}")
        negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        negated_part_constraint.has_picks = constraint.not_picks.copy()
        container_group.has_constraints.append(negated_part_constraint)

    # not_matching_regexes -> multiple(RegexConstraint.has_regex_format)
    if len(constraint.not_matching_regexes) > 0:
        for not_matching_regex in constraint.not_matching_regexes:
            negated_part_constraint = _core.RegexConstraint(f"temp_{round(random()*100000)}")
            negated_part_constraint.is_constraining_column = constraint.is_constraining_column
            negated_part_constraint.has_regex_format = not_matching_regex
            container_group.has_constraints.append(negated_part_constraint)

    # has_regex_format -> not_matching_regexes
    if constraint.has_regex_format:
        negated_part_constraint = _core.Constraint(f"temp_{round(random()*100000)}")
        negated_part_constraint.is_constraining_column = constraint.is_constraining_column
        negated_part_constraint.not_matching_regexes = list()
        negated_part_constraint.not_matching_regexes.append(constraint.has_regex_format)
        container_group.has_constraints.append(negated_part_constraint)

    container_group.unify_constraints()
    # sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    return container_group


def _negate_constraint_group(constraint_group, _core):
    negate = prepare_negation(_core)
    container_group = _core.ConstraintGroup(f"temp_{round(random() * 100000)}")
    container_group.has_constraints = list()

    if isinstance(constraint_group, _core.OrGroup):
        container_group.is_a.append(_core.AndGroup)
    else:
        container_group.is_a.append(_core.OrGroup)

    for constraint in constraint_group.has_constraints:
        negated_constraint = negate(constraint)
        both_or_groups = isinstance(container_group, _core.OrGroup) and isinstance(negated_constraint, _core.OrGroup)
        both_and_groups = isinstance(container_group, _core.AndGroup) and (
                isinstance(negated_constraint, _core.AndGroup) or not isinstance(negated_constraint, _core.OrGroup)
        )
        negated_group_has_single_constaraint = len(negated_constraint.has_constraints) == 1
        if both_or_groups or both_and_groups or negated_group_has_single_constaraint:
            container_group.has_constraints.extend(negated_constraint.has_constraints)
        else:
            container_group.has_constraints.append(negated_constraint)

    container_group.unify_constraints()
    return container_group

