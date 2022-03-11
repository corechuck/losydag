"""

"""
from datetime import datetime
from random import random
import pytest
from owlready2 import get_ontology, sync_reasoner_pellet
from LosydagGenerator import LosydagGenerator
from utils.invertion_factory import ConstraintInverter


@pytest.fixture()
def invert(prepared_core):
    inverter = ConstraintInverter(prepared_core)
    return inverter.invert


def test_inverting_greater_then_or_equal_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterOrEqualThenDependency(name="negated_adventure_dependency_1", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert dependency_under_test != negated_dependency
    assert not isinstance(negated_dependency, prepared_core.GreaterOrEqualThenDependency)
    assert isinstance(negated_dependency, prepared_core.SmallerThenDependency)


def test_inverting_greater_then_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterThenDependency(name="negated_adventure_dependency_2", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert dependency_under_test != negated_dependency
    assert not isinstance(negated_dependency, prepared_core.GreaterThenDependency)
    assert isinstance(negated_dependency, prepared_core.SmallerOrEqualThenDependency)


def test_inverting_smaller_then_or_equal_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.SmallerOrEqualThenDependency(name="negated_adventure_dependency_3", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert dependency_under_test != negated_dependency
    assert not isinstance(negated_dependency, prepared_core.SmallerOrEqualThenDependency)
    assert isinstance(negated_dependency, prepared_core.GreaterThenDependency)


def test_inverting_smaller_then_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.SmallerThenDependency(name="negated_adventure_dependency_4", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert dependency_under_test != negated_dependency
    assert not isinstance(negated_dependency, prepared_core.SmallerThenDependency)
    assert isinstance(negated_dependency, prepared_core.GreaterOrEqualThenDependency)


def test_inverting_format_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.FormatDependency(name="negated_adventure_dependency_5", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    dependency_under_test.is_a.append(prepared_core.Negation)

    negated_dependency_group = invert(dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert isinstance(negated_dependency, prepared_core.FormatDependency)
    assert not isinstance(negated_dependency, prepared_core.Negation)


def test_inverting_equal_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.EqualToDependency(name="negated_adventure_dependency_6", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    # dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    # format_dependency_under_test.is_a.append(prepared_core.Negation)

    negated_dependency_group = invert(dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert dependency_under_test != negated_dependency
    assert isinstance(negated_dependency, prepared_core.EqualToDependency)
    assert isinstance(negated_dependency, prepared_core.Negation)


# def test_negated_format_dependency_for_string(
#         prepared_core, prepared_table, min_req_for_prepared_table):
#     pytest.fail("This is wrong test implementation.")
#     print("INFO: Generating RealizationCase.Check1 in fixture:")
#     testing_iri = "http://corechuck.com/testing/dependency_namespace"
#     test_ontology = get_ontology(testing_iri)
#     test_ontology.imported_ontologies.append(prepared_core)
#
#     dependency_under_test = \
#         prepared_core.FormatDependency(name="great_adventure_dependency_6", namespace=test_ontology)
#     dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
#     dependency_under_test.has_format_definition = "test_format_{column_02}_{column_04}"
#     dependency_under_test.is_a.append(prepared_core.Negation)
#
#     table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def6", namespace=test_ontology)
#     table_2_realization_def.has_constraints = [dependency_under_test.toggle_restriction()]
#     sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
#     table_2_realization_def.compliment_with_min_reqs()
#
#     test_realization = prepared_core.RealizationCase(name="test_realization_case_6", namespace=test_ontology)
#     test_realization.contains_realizations = [table_2_realization_def]
#
#     generator = LosydagGenerator(test_ontology)
#     realized_case = generator.realize_fresh("test_realization_case_6")
#
#     assert realized_case
#     assert realized_case["internal_test_table_01"][0]['column_07'] == 'None'
#
#
# def test_negated_equal_dependency_for_string(
#         prepared_core, prepared_table, min_req_for_prepared_table):
#     pytest.fail("This is wrong test implementation.")
#     print("INFO: Generating RealizationCase.Check1 in fixture:")
#     testing_iri = "http://corechuck.com/testing/dependency_namespace"
#     test_ontology = get_ontology(testing_iri)
#     test_ontology.imported_ontologies.append(prepared_core)
#
#     dependency_under_test = \
#         prepared_core.EqualToDependency(name="great_adventure_dependency_7", namespace=test_ontology)
#     dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
#     dependency_under_test.has_format_definition = "test_format_{column_02}_{column_04}"
#     dependency_under_test.is_a.append(prepared_core.Negation)
#
#     table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def7", namespace=test_ontology)
#     table_2_realization_def.has_constraints = [dependency_under_test]
#     sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
#     table_2_realization_def.compliment_with_min_reqs()
#
#     test_realization = prepared_core.RealizationCase(name="test_realization_case_7", namespace=test_ontology)
#     test_realization.contains_realizations = [table_2_realization_def]
#
#     generator = LosydagGenerator(test_ontology)
#     realized_case = generator.realize_fresh("test_realization_case_7")
#
#     assert realized_case
#     assert realized_case["internal_test_table_01"][0]['column_07'] == 'None'
#
#
# def test_negated_value_dependency_for_string(
#         prepared_core, prepared_table, min_req_for_prepared_table):
#     pytest.fail("This is wrong test implementation.")
#     print("INFO: Generating RealizationCase.Check1 in fixture:")
#     testing_iri = "http://corechuck.com/testing/dependency_namespace"
#     test_ontology = get_ontology(testing_iri)
#     test_ontology.imported_ontologies.append(prepared_core)
#
#     dependency_under_test = \
#         prepared_core.ValueDependency(name="great_adventure_dependency_8", namespace=test_ontology)
#     dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
#     dependency_under_test.has_format_definition = "test_format_{column_02}_{column_04}"
#     dependency_under_test.is_a.append(prepared_core.Negation)
#
#     table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def8", namespace=test_ontology)
#     table_2_realization_def.has_constraints = [dependency_under_test]
#     sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
#     table_2_realization_def.compliment_with_min_reqs()
#
#     test_realization = prepared_core.RealizationCase(name="test_realization_case_8", namespace=test_ontology)
#     test_realization.contains_realizations = [table_2_realization_def]
#
#     generator = LosydagGenerator(test_ontology)
#     realized_case = generator.realize_fresh("test_realization_case_8")
#
#     assert realized_case
#     assert realized_case["internal_test_table_01"][0]['column_07'] == 'None'
