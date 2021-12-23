"""
### GROUPS !!
negation of group ->
- change operator [ and >> or, or >> and ]
- for each constraint negate it
- negate all groups
- merge

1. let r = RangeConstraint; r' = negation of ( negated RangeConstraint r ); r = r'
2. ( two constraint and_group ) x ( how variable that group should be? just all two distinct type groups ? )
3. ( two constraint or_group  ) x ( how variable that group should be? just all two distinct type groups ? )

4. negation (and_group with one or_group <- from ontology )
5. negation (and_group with or_group which have or_group )

4. negation (or_group with one and_group <- from ontology )
5. negation (or_group with and_group which have or_group )
"""
import pytest
from utils.invertion_factory import ConstraintInverter


@pytest.fixture()
def invert(prepared_core):
    inverter = ConstraintInverter(prepared_core)
    return inverter.invert


def test_negation_of_negated_range(prepared_core, invert, actual_range_constraint_under_test):
    middle_negation_group = invert(actual_range_constraint_under_test)
    actual_negation_group = invert(middle_negation_group)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.AndGroup)
    assert len(actual_negation_group.has_constraints) == 1
    double_negated_range = actual_negation_group.has_constraints[0]
    assert double_negated_range.left_limit == actual_range_constraint_under_test.left_limit
    assert double_negated_range.right_limit == actual_range_constraint_under_test.right_limit
    assert len(double_negated_range.not_picks) == 0


def test_negation_of_negated_list(prepared_core, invert, list_constraint_under_test):
    middle_negation_group = invert(list_constraint_under_test)
    actual_negation_group = invert(middle_negation_group)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.AndGroup)
    assert len(actual_negation_group.has_constraints) == 1
    double_negated_range = actual_negation_group.has_constraints[0]
    assert double_negated_range.has_picks == list_constraint_under_test.has_picks
    assert len(double_negated_range.not_picks) == 0


def test_negation_of_negated_range_with_excluded_value(prepared_core, invert, actual_range_constraint_under_test):
    actual_range_constraint_under_test.not_picks = [33]
    middle_negation_group = invert(actual_range_constraint_under_test)
    actual_negation_group = invert(middle_negation_group)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.AndGroup)
    assert len(actual_negation_group.has_constraints) == 1
    double_negated_range = actual_negation_group.has_constraints[0]
    assert double_negated_range.left_limit == actual_range_constraint_under_test.left_limit
    assert double_negated_range.right_limit == actual_range_constraint_under_test.right_limit
    assert len(double_negated_range.not_picks) == 1
    assert 33 in double_negated_range.not_picks


def test_negation_of_group_with_range_and_list(
        prepared_core, invert, actual_range_constraint_under_test, list_constraint_under_test):
    """ This test checks if a result of negation is a group with single constraint is unpacked from its group."""
    container_group = prepared_core.ConstraintGroup()
    container_group.has_constraints = [actual_range_constraint_under_test, list_constraint_under_test]

    actual_negation_group = invert(container_group)

    assert actual_negation_group
    assert isinstance(actual_negation_group, prepared_core.OrGroup)
    assert all((isinstance(c, prepared_core.Constraint) for c in actual_negation_group.has_constraints))


# def test_negation_of_an_and_group_with_regex_and_list(
#         prepared_core, invert, list_constraint_under_test, regex_constraint_under_test):
#
#     # THIS IS AN ISSUE DUE TO SOME UNKNOWN REASON MAKING ONTOLOGY UNCONSITENT CHECK THIS
#     negated_regex = invert(regex_constraint_under_test)
#     container_group = prepared_core.ConstraintGroup()
#     container_group.has_constraints = [negated_regex, list_constraint_under_test]
#     container_group.is_a.append(prepared_core.OrGroup)
#
#     actual_negation_group = invert(container_group)
#
#     assert actual_negation_group
#     assert len(actual_negation_group.has_constraints) == 1
#     result_constraint = actual_negation_group.has_constraints[0]
#     assert result_constraint.not_picks == list_constraint_under_test.has_picks
#     assert result_constraint.has_regex_format == regex_constraint_under_test.has_regex_format


