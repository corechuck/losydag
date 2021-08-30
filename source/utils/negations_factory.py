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
            return _negate_constraint_group

        return None
    return negate


def _negate_range_constraint(range_constraint, _core):
    container_group = _core.ConstraintGroup(f"temp_{round(random() * 100000)}")
    container_group.has_constraints = list()

    if range_constraint.has_min_range == MIN_RANGE:
        negated_part_constraint = _core.RangeConstraint(f"temp_{round(random() * 100000)}")
        negated_part_constraint.is_constraining_column = range_constraint.is_constraining_column
        negated_part_constraint.has_min_range = range_constraint.has_max_range
        negated_part_constraint.not_picks = range_constraint.not_picks.copy()
        if range_constraint.has_max_range in range_constraint.not_picks:
            negated_part_constraint.not_picks.remove(range_constraint.has_max_range)
        else:
            negated_part_constraint.not_picks.append(range_constraint.has_max_range)
        container_group.has_constraints.append(negated_part_constraint)

    elif range_constraint.has_max_range == MAX_RANGE:
        negated_part_constraint = _core.RangeConstraint(f"temp_{round(random() * 100000)}")
        negated_part_constraint.is_constraining_column = range_constraint.is_constraining_column
        negated_part_constraint.has_max_range = range_constraint.has_min_range
        negated_part_constraint.not_picks = range_constraint.not_picks.copy()
        if range_constraint.has_min_range in range_constraint.not_picks:
            negated_part_constraint.not_picks.remove(range_constraint.has_min_range)
        else:
            negated_part_constraint.not_picks.append(range_constraint.has_min_range)
        container_group.has_constraints.append(negated_part_constraint)

    container_group.unify_constraints()
    # sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    return container_group


def _negate_basic_constraint(constraint, _core):
    container_group = _core.ConstraintGroup(f"temp_{round(random()*100000)}")
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
        container_group.is_a.append(_core.OrGroup)
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
    pass
