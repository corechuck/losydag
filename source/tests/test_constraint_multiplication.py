import unittest

from utils.sentence_processing import MultiplicationSupervisor


def test_multiplication_with_and_to_and(
        prepared_core, list_constraint_under_test, max_range_constraint_under_test, min_range_constraint_under_test,
        regex_constraint_under_test):
    left_group = prepared_core.ConstraintGroup("left_group_1")
    left_group.has_constraints = [list_constraint_under_test, max_range_constraint_under_test]

    right_group = prepared_core.ConstraintGroup("right_group_1")
    right_group.has_constraints = [min_range_constraint_under_test, regex_constraint_under_test]

    multiplicator = MultiplicationSupervisor(prepared_core)
    actual_sets = multiplicator.multiply_groups(left_group, right_group)

    assert actual_sets
    assert len(actual_sets) == 1


def test_multiplication_with_and_to_or(
        prepared_core, list_constraint_under_test, max_range_constraint_under_test, min_range_constraint_under_test,
        regex_constraint_under_test):
    left_group = prepared_core.ConstraintGroup("left_group_2")
    left_group.has_constraints = [list_constraint_under_test, max_range_constraint_under_test]

    right_group = prepared_core.ConstraintGroup("right_group_2")
    right_group.is_a.append(prepared_core.OrGroup)
    right_group.has_constraints = [min_range_constraint_under_test, regex_constraint_under_test]

    multiplicator = MultiplicationSupervisor(prepared_core)
    actual_sets = multiplicator.multiply_groups(left_group, right_group)

    assert actual_sets
    assert len(actual_sets) == 2
    assert len(actual_sets[0]) == 3
    assert len(actual_sets[1]) == 3


def test_multiplication_with_or_to_and(
        prepared_core, list_constraint_under_test, max_range_constraint_under_test, min_range_constraint_under_test,
        regex_constraint_under_test):
    left_group = prepared_core.ConstraintGroup("left_group_3")
    left_group.is_a.append(prepared_core.OrGroup)
    left_group.has_constraints = [list_constraint_under_test, max_range_constraint_under_test]

    right_group = prepared_core.ConstraintGroup("right_group_3")
    right_group.has_constraints = [min_range_constraint_under_test, regex_constraint_under_test]

    multiplicator = MultiplicationSupervisor(prepared_core)
    actual_sets = multiplicator.multiply_groups(left_group, right_group)

    assert actual_sets
    assert len(actual_sets) == 2
    assert len(actual_sets[0]) == 3
    assert len(actual_sets[1]) == 3


def test_multiplication_with_or_to_or_left_single(
        prepared_core, list_constraint_under_test, min_range_constraint_under_test,
        regex_constraint_under_test):
    left_group = prepared_core.ConstraintGroup("left_group_4")
    left_group.is_a.append(prepared_core.OrGroup)
    left_group.has_constraints = [list_constraint_under_test]

    right_group = prepared_core.ConstraintGroup("right_group_4")
    right_group.is_a.append(prepared_core.OrGroup)
    right_group.has_constraints = [min_range_constraint_under_test, regex_constraint_under_test]

    multiplicator = MultiplicationSupervisor(prepared_core)
    actual_sets = multiplicator.multiply_groups(left_group, right_group)

    assert actual_sets
    assert len(actual_sets) == 2


def test_multiplication_with_or_to_or(
        prepared_core, list_constraint_under_test, max_range_constraint_under_test, min_range_constraint_under_test,
        regex_constraint_under_test):
    left_group = prepared_core.ConstraintGroup("left_group_5")
    left_group.is_a.append(prepared_core.OrGroup)
    left_group.has_constraints = [list_constraint_under_test, max_range_constraint_under_test]

    right_group = prepared_core.ConstraintGroup("right_group_5")
    right_group.is_a.append(prepared_core.OrGroup)
    right_group.has_constraints = [min_range_constraint_under_test, regex_constraint_under_test]

    multiplicator = MultiplicationSupervisor(prepared_core)
    actual_sets = multiplicator.multiply_groups(left_group, right_group)

    assert actual_sets
    assert len(actual_sets) == 4
    assert len(actual_sets[0]) == 2
    assert len(actual_sets[1]) == 2
    assert len(actual_sets[2]) == 2
    assert len(actual_sets[3]) == 2
