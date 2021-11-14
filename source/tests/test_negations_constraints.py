"""
1. negation of generic constraint - not in  => listConstraint
2. negation of generic constraint - single not_in_regex => Regex constraint
3. negation of generic constraint - multiple not_in_regex => OR_Group with multiple RegexConstraints
4. negation of generic constraint - non empty not_in and non empty not_in_regex => or_group with List and regex constraint

1. negation of RegexConstraint - generic not_in_regex

1. negation of ListConstraint - generic not in list

1. negation of RangeConstraint r - or_group with two ranges from MIN to r.has_min, and from r.has_max to MAX
2. negation of RangeConstraint - which has_min <= MIN   >>  only group with rangeConst from r.has_max to MAX
3. negation of RangeConstraint - which has_max >= MIN   >>  only group with rangeConst from MIN to r.has_min
4. open/close boundaries
5. Range with not_picks and not_matches_regexes

"""
from datetime import datetime
from random import random

import pytest

from core_classes.Constraints import MAX_RANGE as CONSTRAINTS_MAX_RANGE, MIN_RANGE as CONSTRAINTS_MIN_RANGE
from utils.invertion_factory import ConstraintInverter

""" TODO: Empty generic negation what will give you? """


@pytest.fixture()
def invert(prepared_core):
    inverter = ConstraintInverter(prepared_core)
    return inverter.invert


def test_negation_of_generic_constraint_not_in(prepared_core, invert, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_{round(random()*100000)}")
    list_const.is_constraining_column = prepared_column
    list_const.not_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']

    actual_negation_group = invert(list_const)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    assert id(list_const.not_picks) != id(actual_negation_group.has_constraints[0].has_picks)
    for vv in list_const.has_picks:
        assert vv in actual_negation_group.has_constraints[0].has_picks


def test_negation_of_generic_constraint_single_not_in_regex(prepared_core, invert, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_a_{round(random()*100000)}")
    list_const.is_constraining_column = prepared_column

    not_list_const = prepared_core.ListConstraint(f"list_not_req_a_{round(random()*100000)}")
    not_list_const.not_matching_regexes = ['boo.*']



    actual_negation_group = invert(list_const)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    assert actual_negation_group.has_constraints[0]
    assert actual_negation_group.has_constraints[0].has_regex_format == 'boo.*'


def test_negation_of_generic_constraint_multiple_not_in_regex(prepared_core, invert, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_b_{round(random()*100000)}")
    list_const.is_constraining_column = prepared_column
    list_const.not_matching_regexes = ['boo.*', '.*foo.*']

    expected_list_of_regexes = ['boo.*', '.*foo.*']

    actual_negation_group = invert(list_const)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 2
    assert all([
        isinstance(constraint, prepared_core.RegexConstraint)
        for constraint
        in actual_negation_group.has_constraints
    ])
    for regex_constraint in actual_negation_group.has_constraints:
        assert regex_constraint.has_regex_format in expected_list_of_regexes
        expected_list_of_regexes.remove(regex_constraint.has_regex_format)
    assert len(expected_list_of_regexes) == 0


def test_negation_of_generic_constraint_multiple_types(prepared_core, invert, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_{round(random()*100000)}")
    list_const.is_constraining_column = prepared_column
    list_const.not_matching_regexes = ['boo.*']
    list_const.not_picks = ['foo', 'moo']
    is_there_list_constraint = False
    is_there_regex_constraint = False

    actual_negation_group = invert(list_const)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)

    for constraint in actual_negation_group.has_constraints:
        is_there_regex_constraint = \
            is_there_regex_constraint or isinstance(constraint, prepared_core.RegexConstraint)
        is_there_list_constraint = \
            is_there_list_constraint or isinstance(constraint, prepared_core.ListConstraint)

    assert is_there_regex_constraint
    assert is_there_list_constraint


def test_negation_of_regex_constraint(prepared_core, invert, regex_constraint_under_test):
    actual_negation_group = invert(regex_constraint_under_test)
    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.AndGroup) or \
           not isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    assert "[a-z]oo" in actual_negation_group.has_constraints[0].not_matching_regexes


def test_negation_of_regex_constraint(prepared_core, invert, list_constraint_under_test):
    actual_negation_group = invert(list_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    assert id(list_constraint_under_test.has_picks) != id(actual_negation_group.has_constraints[0].not_picks)
    assert list_constraint_under_test.has_picks == actual_negation_group.has_constraints[0].not_picks

# def min_range_constraint_under_test(prepared_core, prepared_column):


# def max_range_constraint_under_test(prepared_core, prepared_column):


def test_negation_of_range_less_or_equal_then(prepared_core, invert, max_range_constraint_under_test):
    actual_negation_group = invert(max_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.has_min_range == max_range_constraint_under_test.has_max_range
    assert actual_negated_constraint.has_max_range == CONSTRAINTS_MAX_RANGE
    assert actual_negated_constraint.not_picks
    assert len(actual_negated_constraint.not_picks) == 1
    assert actual_negated_constraint.not_picks[0] == max_range_constraint_under_test.has_max_range


def test_negation_of_range_less_then(prepared_core, invert, max_range_constraint_under_test):
    max_range_constraint_under_test.not_picks = [max_range_constraint_under_test.has_max_range]
    actual_negation_group = invert(max_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.has_min_range == max_range_constraint_under_test.has_max_range
    assert actual_negated_constraint.has_max_range == CONSTRAINTS_MAX_RANGE
    assert not hasattr(actual_negated_constraint, 'not_picks') or len(actual_negated_constraint.not_picks) == 0


def test_negation_of_range_greater_or_equal_then(prepared_core, invert, min_range_constraint_under_test):
    actual_negation_group = invert(min_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.has_max_range == min_range_constraint_under_test.has_min_range
    assert actual_negated_constraint.has_min_range == CONSTRAINTS_MIN_RANGE
    assert actual_negated_constraint.not_picks
    assert len(actual_negated_constraint.not_picks) == 1
    assert actual_negated_constraint.not_picks[0] == min_range_constraint_under_test.has_min_range


def test_negation_of_range_greater_then(prepared_core, invert, min_range_constraint_under_test):
    min_range_constraint_under_test.not_picks = [min_range_constraint_under_test.has_min_range]
    actual_negation_group = invert(min_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 1
    actual_negated_constraint = actual_negation_group.has_constraints[0]
    assert actual_negated_constraint.has_max_range == min_range_constraint_under_test.has_min_range
    assert actual_negated_constraint.has_min_range == CONSTRAINTS_MIN_RANGE
    assert not hasattr(actual_negated_constraint, 'not_picks') or len(actual_negated_constraint.not_picks) == 0


def test_negation_of_actual_range_right_open_to_or_group(prepared_core, invert, actual_range_constraint_under_test):
    """ Too spice it up it is open on right side"""
    actual_range_constraint_under_test.not_picks = [actual_range_constraint_under_test.has_max_range]
    actual_negation_group = invert(actual_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 2
    lower_range = next(c for c in actual_negation_group.has_constraints if c.has_min_range == CONSTRAINTS_MIN_RANGE)
    assert lower_range.has_max_range == actual_range_constraint_under_test.has_min_range
    assert lower_range.has_max_range in lower_range.not_picks
    higher_range = next(c for c in actual_negation_group.has_constraints if c.has_max_range == CONSTRAINTS_MAX_RANGE)
    assert higher_range.has_min_range == actual_range_constraint_under_test.has_max_range
    assert len(higher_range.not_picks) == 0


def test_negation_of_range_with_not_in_list(prepared_core, invert, actual_range_constraint_under_test):
    """ not_picks that are inside range and outside range - how broken down,
    -20 and 101 will be lost on double negation as originally semantically a range (10,40> excludes
    """
    actual_range_constraint_under_test.not_picks = [actual_range_constraint_under_test.has_min_range, 13, 34]
    actual_negation_group = invert(actual_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 3
    lower_range = next(c for c in actual_negation_group.has_constraints if c.has_min_range == CONSTRAINTS_MIN_RANGE)
    assert len(lower_range.not_picks) == 0
    higher_range = next(c for c in actual_negation_group.has_constraints if c.has_max_range == CONSTRAINTS_MAX_RANGE)
    assert len(higher_range.not_picks) == 1
    internal_to_range_picks = \
        next(c for c in actual_negation_group.has_constraints if isinstance(c, prepared_core.ListConstraint))
    assert internal_to_range_picks
    assert len(internal_to_range_picks.has_picks) == 2
    assert 13 in internal_to_range_picks.has_picks
    assert 34 in internal_to_range_picks.has_picks


def test_negation_of_range_with_not_in_list_removes_semantically_over_definitions(
        prepared_core, invert, actual_range_constraint_under_test):
    """ not_picks that are inside range and outside range - how broken down,
    -20 and 101 will be lost on double negation as originally semantically a range (10,40> excludes
    """
    actual_range_constraint_under_test.not_picks = [actual_range_constraint_under_test.has_min_range, 13, 34, -20, 101]
    actual_negation_group = invert(actual_range_constraint_under_test)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert actual_negation_group.has_constraints
    assert len(actual_negation_group.has_constraints) == 3
    internal_to_range_picks = \
        next(c for c in actual_negation_group.has_constraints if isinstance(c, prepared_core.ListConstraint))
    assert internal_to_range_picks
    assert len(internal_to_range_picks.has_picks) == 2
    assert 13 in internal_to_range_picks.has_picks
    assert 34 in internal_to_range_picks.has_picks


