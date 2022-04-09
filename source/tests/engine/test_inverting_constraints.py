"""
That is outdated. Not reviewed after refactor of ranges.


1. negation of generic constraint - not in  => listConstraint
2. negation of generic constraint - single not_in_regex => Regex constraint
3. negation of generic constraint - multiple not_in_regex => OR_Group with multiple RegexConstraints
4. negation of generic constraint - non empty not_in and non empty not_in_regex => or_group with List and regex constraint

1. negation of RegexConstraint - generic not_in_regex

1. negation of ListConstraint - generic not in list

1. negation of RangeConstraint r - or_group with two ranges from MIN to r.has_min, and from r.has_max to MAX
2. negation of RangeConstraint - which has_left <= MIN   >>  only group with rangeConst from r.has_max to MAX
3. negation of RangeConstraint - which has_right >= MIN   >>  only group with rangeConst from MIN to r.has_min
4. open/close boundaries
5. Range with not_picks and not_matches_regexes

"""
from random import random
from typing import Callable

import pytest
from utils.invertion_factory import ConstraintInverter

""" TODO: Empty generic negation what will give you? """


@pytest.fixture()
def invert(prepared_core) -> Callable:
    inverter = ConstraintInverter(prepared_core)
    return inverter.invert


def test_inverting_restriction(prepared_core, invert, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_{round(random()*100000)}")
    list_const.is_constraining_column = prepared_column
    list_const.has_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']

    restriction_constraint = prepared_core.RestrictiveConstraint(restricting_constraint=list_const)

    actual_negation_group = invert(restriction_constraint)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    assert list_const == actual_negation_group.has_constraints[0]


def test_inverting_list_constraint(prepared_core, invert, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_{round(random()*100000)}")
    list_const.is_constraining_column = prepared_column
    list_const.has_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']

    actual_negation_group = invert(list_const)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    restriction_const = actual_negation_group.has_constraints[0]
    assert restriction_const
    assert restriction_const.restriction_definition == list_const


def test_inverting_regex_constraint(prepared_core, invert, regex_constraint_under_test):
    actual_negation_group = invert(regex_constraint_under_test)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    restriction_const = actual_negation_group.has_constraints[0]
    assert restriction_const
    assert restriction_const.restriction_definition == regex_constraint_under_test


def test_inverting_range_with_closed_right(prepared_core, invert, max_range_constraint_under_test):
    actual_negation_group_2 = invert(max_range_constraint_under_test)

    assert actual_negation_group_2
    assert isinstance(actual_negation_group_2, prepared_core.OrGroup)
    assert actual_negation_group_2.has_constraints
    assert len(actual_negation_group_2.has_constraints) == 1
    actual_negated_constraint = actual_negation_group_2.has_constraints[0]
    assert actual_negated_constraint.left_limit() == max_range_constraint_under_test.right_limit()
    assert actual_negated_constraint.right_limit() == \
           max_range_constraint_under_test.get_maximum_value_for_data_type()
    assert isinstance(actual_negated_constraint.has_left_boundary, prepared_core.OpenRangeBoundary)
    assert not hasattr(actual_negated_constraint, 'not_picks') or len(actual_negated_constraint.not_picks) == 0


def test_inverting_range_with_open_right(prepared_core, invert, max_range_constraint_under_test):
    max_range_constraint_under_test.set_right_boundary(max_range_constraint_under_test.right_limit(), is_open=True)
    actual_negation_group = invert(max_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.left_limit() == max_range_constraint_under_test.right_limit()
    assert actual_negated_constraint.right_limit() == \
           max_range_constraint_under_test.get_maximum_value_for_data_type()
    assert isinstance(actual_negated_constraint.has_left_boundary, prepared_core.ClosedRangeBoundary)
    assert not hasattr(actual_negated_constraint, 'not_picks') or len(actual_negated_constraint.not_picks) == 0


def test_inverting_range_with_closed_left(prepared_core, invert, min_range_constraint_under_test):
    actual_negation_group = invert(min_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.right_limit() == min_range_constraint_under_test.left_limit()
    assert actual_negated_constraint.left_limit() == \
           min_range_constraint_under_test.get_minimum_value_for_data_type()
    assert isinstance(actual_negated_constraint.has_right_boundary, prepared_core.OpenRangeBoundary)
    assert not hasattr(actual_negated_constraint, 'not_picks') or len(actual_negated_constraint.not_picks) == 0


def test_inverting_range_with_open_left(prepared_core, invert, min_range_constraint_under_test):
    min_range_constraint_under_test.set_left_boundary(min_range_constraint_under_test.left_limit(), is_open=True)
    actual_negation_group = invert(min_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.right_limit() == min_range_constraint_under_test.left_limit()
    assert actual_negated_constraint.left_limit() == \
           min_range_constraint_under_test.get_minimum_value_for_data_type()
    assert isinstance(actual_negated_constraint.has_right_boundary, prepared_core.ClosedRangeBoundary)
    assert not hasattr(actual_negated_constraint, 'not_picks') or len(actual_negated_constraint.not_picks) == 0


def test_negation_of_actual_range_right_open_to_or_group(prepared_core, invert, actual_range_constraint_under_test):
    """ Too spice it up it is open on right side"""
    actual_range_constraint_under_test.set_left_boundary(actual_range_constraint_under_test.left_limit(), is_open=True)
    actual_negation_group = invert(actual_range_constraint_under_test)

    min_range = actual_range_constraint_under_test.get_minimum_value_for_data_type()
    max_range = actual_range_constraint_under_test.get_maximum_value_for_data_type()

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 2
    lower_range = next(c for c in actual_negation_group.has_constraints if c.left_limit() == min_range)
    assert lower_range.right_limit() == actual_range_constraint_under_test.left_limit()
    assert isinstance(lower_range.has_right_boundary, prepared_core.ClosedRangeBoundary)
    higher_range = next(c for c in actual_negation_group.has_constraints if c.right_limit() == max_range)
    assert higher_range.left_limit() == actual_range_constraint_under_test.right_limit()
    assert isinstance(higher_range.has_left_boundary, prepared_core.OpenRangeBoundary)
