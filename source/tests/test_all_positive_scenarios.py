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


@pytest.fixture(scope="session")
def realized_case_positive():
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    loaded_onto = get_ontology("http://corechuck.com/modeling/dependent_onto")
    loaded_onto.load(only_local=True)
    generator: LosydagGenerator = LosydagGenerator(loaded_onto)
    realized_cases = generator.generate_all_positive_datasets_from_generic_group("RealizationCase.Check1")
    return realized_cases


# def test_generated_data_have_all_needed_tables(realized_case_positive):
#     assert realized_case_positive is not None


def test_positive_breadown_3_levels_deep(prepared_core, list_constraint_under_test, min_range_constraint_under_test,
                                         max_range_constraint_under_test, regex_constraint_under_test,
                                         actual_range_constraint_under_test):
    group_1 = prepared_core.ConstraintGroup("group_root")
    group_2 = prepared_core.ConstraintGroup("group_child")
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)
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
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)

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
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)

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
    group_1.is_a.append(prepared_core.OrGroup)
    group_1.is_a.remove(prepared_core.AndGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)

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
    group_1.is_a.append(prepared_core.OrGroup)
    group_1.is_a.remove(prepared_core.AndGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)
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
    group_1.is_a.append(prepared_core.OrGroup)
    group_1.is_a.remove(prepared_core.AndGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)
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
    group_1.is_a.append(prepared_core.OrGroup)
    group_1.is_a.remove(prepared_core.AndGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)
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
    group_1.is_a.append(prepared_core.OrGroup)
    group_1.is_a.remove(prepared_core.AndGroup)
    group_2 = prepared_core.ConstraintGroup(f"group_child{addition}")
    group_2.is_a.append(prepared_core.OrGroup)
    group_2.is_a.remove(prepared_core.AndGroup)
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

# def test_that_equal_external_dependency_are_equal(realized_case):
#     assert realized_case['Table.Ref_01'][0]['Col0_id'] == (
#         realized_case['Table.Test3'][0]['Col2_property1_number']
#     )
#
#
# def test_that_id_column_format_is_valid(realized_case):
#     """this may fail as //w sometimes becomes "_" and break format, todo: adjust //w to not have '_' """
#     parts = realized_case['Table.Test1'][0]['Col0_id'].split("_")
#     assert not parts[0].isnumeric()
#     assert len(parts[1]) > 0
#     assert parts[2].isnumeric()
#
#
# def test_column_follows_list_constraint(realized_case):
#     assert realized_case['Table.Test1'][0]['Col1_n'] in ["32", "14"]
#
#
# def test_that_column_has_date_simple(realized_case):
#     date = datetime.strptime(realized_case['Table.Test1'][0]['Col2_d'], '%Y-%m-%d')
#     assert date
#
#
# def test_that_unconstrained_column_produce_none(realized_case):
#     assert realized_case['Table.Test1'][0]['Col4_not_constrained'] is None
#
#
# def test_that_for_table2_two_entries_has_been_generated(realized_case):
#     assert len(realized_case['Table.Test2']) == 2
#
#
# def test_autoincrements(realized_case):
#     parts_01 = realized_case['Table.Test2'][0]['Col0_id'].split("_")
#     parts_02 = realized_case['Table.Test2'][1]['Col0_id'].split("_")
#     assert abs(int(parts_01[1]) - int(parts_02[1])) == 1
#     assert int(parts_01[1]) != int(parts_02[1])
#
#
# def test_all_realizations_follow_its_own_internal_dependency(realized_case):
#
#     tab2_r1 = realized_case['Table.Test2'][0]
#     tab2_r2 = realized_case['Table.Test2'][1]
#
#     assert tab2_r1["Col3_text"]+"_copy" == tab2_r1["Col4_formatted"]
#     assert tab2_r2["Col3_text"]+"_copy" == tab2_r2["Col4_formatted"]
#
#     assert tab2_r1["Col3_text"]+"_copy" != tab2_r2["Col3_text"]
#     assert tab2_r1["Col4_formatted"]+"_copy" != tab2_r2["Col4_formatted"]
#
#
# def test_min_requirement_overridden_by_custom_from_realization_definition(realized_case):
#     assert realized_case['Table.Test1'][0]['Col3_text'] in ["Tree", "Rock"]
#
#
# def test_generic_constraint_was_merged_with_minimum_requirement_for_given_column(realized_case):
#     """ TODO: Implement that feature """
#     pytest.skip("TODO: Implement that feature: https://github.com/corechuck/losydag/issues/11")
#
#
# def test_all_realizations_have_been_overridden(realized_case):
#     assert realized_case['Table.Test2'][0]['Col3_text'] not in ["London", "Tokio", "Paris"]
#     assert realized_case['Table.Test2'][1]['Col3_text'] not in ["London", "Tokio", "Paris"]


"""
test that generated data has:
    id follows format DONE
    Column.Test1.Col1_n is 32 or 14 DONE
    Column.Test1.Col2_d should be date DONE
    Column.Test1.Col4_not_constrained is a number
    two entries in Table.Test2 DONE
    two entries ids have different autoincrements DONE
    both Table2 entries have col4 == col3 DONE
    Column.Test1.Col3_text has tree or rock not DONE
    All sets of Table.Test2 not have in Column.Test2.Col3_text "London" and "Tokio" and "Paris DONE
    
    Realization.Test2.first_colors Column.Test2.Col3_text has 
    Should be one more Table that is not in result 

Other generation of just Table2. where Test.Col3_text have "London" and "Tokio" and "Paris 
    it needs better conversion from Min_Req to Realization def. Move Req_Min to be subclass of RealizationDef


"""
