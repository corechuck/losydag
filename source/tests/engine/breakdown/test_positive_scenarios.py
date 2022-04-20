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


# @pytest.fixture(scope="session")
# def realized_case_positive():
#     print("INFO: Generating RealizationCase.Check1 in fixture:")
#     loaded_onto = get_ontology("http://corechuck.com/modeling/dependent_onto")
#     loaded_onto.load(only_local=True)
#     generator: LosydagGenerator = LosydagGenerator(loaded_onto)
#     realized_cases = generator.generate_all_positive_datasets_from_generic_group("RealizationCase.Check1")
#     return realized_cases


# def test_generated_data_have_all_needed_tables(realized_case_positive):
#     assert realized_case_positive is not None


def test_positive_breadown_3_levels_deep(prepared_core, list_constraint_under_test, min_range_constraint_under_test,
                                         max_range_constraint_under_test, regex_constraint_under_test,
                                         actual_range_constraint_under_test):
    group_1 = prepared_core.ConstraintGroup("group_root")
    group_2 = prepared_core.ConstraintGroup("group_child")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)
    group_3 = prepared_core.ConstraintGroup("group_grandchild")

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = [min_range_constraint_under_test, regex_constraint_under_test]
    group_3.has_constraints = [max_range_constraint_under_test, actual_range_constraint_under_test]

    group_1.contains_constraint_groups = [group_2]
    group_2.contains_constraint_groups = [group_3]

    result = group_1.prepare_positive_cases()
    assert result is not None
    # 4 and 5th is not broken down - I think


def test_positive_breadown_2_levels_deep(prepared_core, list_constraint_under_test, min_range_constraint_under_test,
                                         max_range_constraint_under_test, regex_constraint_under_test,
                                         actual_range_constraint_under_test):
    group_1 = prepared_core.ConstraintGroup("group_root_2")
    group_2 = prepared_core.ConstraintGroup("group_child_2")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = \
        [min_range_constraint_under_test, max_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2]

    result = group_1.prepare_positive_cases()
    assert result is not None


def test_positive_breadown_2_levels_deep_v2(prepared_core, list_constraint_under_test, min_range_constraint_under_test,
                                         max_range_constraint_under_test, regex_constraint_under_test,
                                         actual_range_constraint_under_test):
    addition = "_3"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = \
        [min_range_constraint_under_test, max_range_constraint_under_test, regex_constraint_under_test]

    group_2.contains_constraint_groups = [group_1]

    result = group_2.prepare_positive_cases()
    assert result is not None


def test_positive_breadown_2_levels_deep_v4(
        prepared_core, list_constraint_under_test, min_range_constraint_under_test,
        max_range_constraint_under_test, regex_constraint_under_test, actual_range_constraint_under_test):
    addition = "_4"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_1.change_to_or_operator()
    #group_1.is_a.append(prepared_core.OrGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)

    group_1.has_constraints = [list_constraint_under_test, actual_range_constraint_under_test]
    group_2.has_constraints = \
        [min_range_constraint_under_test, max_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2]

    result = group_1.prepare_positive_cases()
    assert result is not None
    assert len(result) == 5


def test_positive_breadown_2_levels_deep_v5(
        prepared_core, list_constraint_under_test, min_range_constraint_under_test,
        max_range_constraint_under_test, regex_constraint_under_test, actual_range_constraint_under_test):
    addition = "_5"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_1.change_to_or_operator()
    #group_1.is_a.append(prepared_core.OrGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)
    group_3 = prepared_core.ConstraintGroup(f"group_grandchild{addition}")

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = [min_range_constraint_under_test, max_range_constraint_under_test]
    group_3.has_constraints = [actual_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2, group_3]

    result = group_1.prepare_positive_cases()
    assert result is not None
    assert len(result) == 7


def test_positive_breakdown_2_generation_works(
        prepared_core, prepared_table, list_constraint_under_test, min_range_constraint_under_test,
        max_range_constraint_under_test, regex_constraint_under_test, actual_range_constraint_under_test):
    addition = "_6"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_1.change_to_or_operator()
    #group_1.is_a.append(prepared_core.OrGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)
    group_3 = prepared_core.ConstraintGroup(f"group_grandchild{addition}")

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = [min_range_constraint_under_test, max_range_constraint_under_test]
    group_3.has_constraints = [actual_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2, group_3]

    positive_cases = group_1.prepare_positive_cases()
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    cases_index = 0
    for case in positive_cases:
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
            data = realization_case.realize()
        except ValueGenerationException:
            print(f"Could not generate value for case {case.meta}.")
            continue

        print(data)
        assert data


def test_positive_breakdown_2_generation_work_sep_column(
        prepared_core, prepared_table, list_constraint_under_test, min_range_constraint_under_test,
        max_range_constraint_under_test, regex_constraint_under_test, actual_range_constraint_under_test):
    addition = "_7"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_1.change_to_or_operator()
    #group_1.is_a.append(prepared_core.OrGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)
    group_3 = prepared_core.ConstraintGroup(f"group_grandchild{addition}")

    regex_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]
    min_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]
    max_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]

    actual_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[2]

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = [min_range_constraint_under_test, max_range_constraint_under_test]
    group_3.has_constraints = [actual_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2, group_3]

    positive_cases = group_1.prepare_positive_cases()
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    cases_index = 0
    for case in positive_cases:
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
            data = realization_case.realize()
        except ValueGenerationException:
            print(f"Could not generate value for case {case.meta}.")
            continue

        print(data)
        assert data


def test_positive_breakdown_2_generation_of_all_possibilities(
        prepared_core, prepared_table, list_constraint_under_test, min_range_constraint_under_test,
        max_range_constraint_under_test, regex_constraint_under_test, actual_range_constraint_under_test):
    addition = "_8"
    group_1 = prepared_core.ConstraintGroup(f"group_root{addition}")
    group_1.change_to_or_operator()
    #group_1.is_a.append(prepared_core.OrGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.change_to_or_operator()
    #group_2.is_a.append(prepared_core.OrGroup)
    group_3 = prepared_core.ConstraintGroup(f"group_grandchild{addition}")

    regex_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]
    min_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]
    max_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[1]

    actual_range_constraint_under_test.is_constraining_column = prepared_table.has_columns[2]

    group_1.has_constraints = [list_constraint_under_test]
    group_2.has_constraints = [min_range_constraint_under_test, max_range_constraint_under_test]
    group_3.has_constraints = [actual_range_constraint_under_test, regex_constraint_under_test]

    group_1.contains_constraint_groups = [group_2, group_3]

    positive_cases = group_1.prepare_positive_cases()
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    cases_index = 0
    for case in positive_cases:
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
