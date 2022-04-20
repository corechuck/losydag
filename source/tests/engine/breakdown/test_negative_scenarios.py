import os
from datetime import datetime
import pytest
from owlready2 import get_ontology, onto_path, sync_reasoner_pellet
from LosydagGenerator import LosydagGenerator
from utils.utils import MergingException, ValueGenerationException

""" 
This test suite does not explains how a realization case has been build, for that open Protege and check ontology. This
is rather integration tests and overall generator functionality checks.
"""

onto_path.append(f"{os.getcwd()}/resources/core/")
onto_path.append(f"{os.getcwd()}/resources/development/")


def find_first_constraint_meeting(cases, filter_function):
    for case in cases:
        for constraint in case.has_constraints:
            if filter_function(constraint):
                return case, constraint
    return None, None


def test_negative_cases_for_simple_and_group_with_range_and_list(
        prepared_core, prepared_table, list_constraint_under_test, actual_range_constraint_under_test):
    addition = "_10"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    list_constraint_under_test.is_constraining_column = prepared_table.has_columns[0]
    actual_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[2]

    # that is (c1 ^ c2) -> (actual ^ list)
    group_1.has_constraints = [actual_range_constraint_under_test, list_constraint_under_test]

    negative_cases = group_1.prepare_negative_cases()
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    assert len(negative_cases) == 3
    lower_range_case, lower_end_constraint = find_first_constraint_meeting(
        negative_cases,
        lambda c: c.has_right_boundary and c.has_right_boundary.has_boundary_value ==
                  actual_range_constraint_under_test.has_left_boundary.has_boundary_value
    )
    assert lower_end_constraint
    higher_range_case, higher_end_constraint = find_first_constraint_meeting(
        negative_cases,
        lambda c: c.has_left_boundary and c.has_left_boundary.has_boundary_value ==
                  actual_range_constraint_under_test.has_right_boundary.has_boundary_value
    )
    assert higher_end_constraint
    assert lower_range_case != higher_range_case
    restricted_list_case, restrictive_const = find_first_constraint_meeting(
        negative_cases, lambda c: c.restriction_definition == list_constraint_under_test
    )
    assert restricted_list_case
    assert restrictive_const


def test_negative_cases_for_fun(
        prepared_core, prepared_table, list_constraint_under_test, min_range_constraint_under_test,
        max_range_constraint_under_test, regex_constraint_under_test, actual_range_constraint_under_test):
    addition = "_9"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)
    group_3 = prepared_core.ConstraintGroup(f"group_grandchild{addition}")

    regex_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]
    min_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[2]
    max_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[3]

    actual_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[4]

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = [min_range_constraint_under_test, max_range_constraint_under_test]
    group_3.has_constraints = [actual_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2, group_3]

    # that is (c1 ^ (c2 v c3) ^ (c4 ^ c5)) -> (list ^ (min v max) ^ (actual ^ rgx))
    negative_cases = group_1.prepare_negative_cases()
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    cases_index = 0
    for case in negative_cases:
        data = None
        cases_index += 1
        print(f"INFO: Case {cases_index} with meta: {case.meta}")
        try:
            realization_case = case.build_realization_case()
        except MergingException as e:
            print(f"Case {case.meta} resulted is empty choices")
            print(e.args[0])
            continue

        try:
            data = realization_case.realize_all_test_case_relevant_datasets()
        except ValueGenerationException:
            print(f"Could not generate value for case {case.meta}.")
            continue

        print(data)
        assert data
