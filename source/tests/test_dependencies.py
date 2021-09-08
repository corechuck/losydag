import pytest
from owlready2 import get_ontology, sync_reasoner_pellet

from LosydagGenerator import LosydagGenerator


def test_greater_then_or_equal_dependency(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.GreaterOrEqualThenDependency(name="great_andventure_dependency_1", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_or_equal_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_1", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_1")

    assert realized_case
    assert realized_case["internal_test_table_02"][0]['column_01'] == \
           realized_case["internal_test_table_01"][0]['column_01']


def test_greater_then_dependency(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.GreaterThenDependency(name="great_andventure_dependency_2", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[2]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table2_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_or_equal_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_2", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_2")

    assert realized_case
    assert int(realized_case["internal_test_table_02"][0]['column_03']) > \
           int(realized_case["internal_test_table_01"][0]['column_03'])


def test_greater_then_dependency_for_string(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.GreaterThenDependency(name="great_andventure_dependency_2", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table2_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_or_equal_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_2", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    with pytest.raises(Exception, match=r"^ERROR: .*"):
        generator.realize_fresh("test_realization_case_2")


def test_smaller_then_or_equal_dependency(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.SmallerOrEqualThenDependency(name="great_andventure_dependency_3", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table3_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_or_equal_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_3", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_3")

    assert realized_case
    assert realized_case["internal_test_table_02"][0]['column_01'] == \
           realized_case["internal_test_table_01"][0]['column_01']


def test_smaller_then_dependency(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.SmallerThenDependency(name="great_andventure_dependency_4", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[2]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table4_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_or_equal_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_4", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_4")

    assert realized_case
    assert int(realized_case["internal_test_table_02"][0]['column_03']) < \
           int(realized_case["internal_test_table_01"][0]['column_03'])


def test_smaller_then_dependency_for_string(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.SmallerThenDependency(name="great_andventure_dependency_4", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table4_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_or_equal_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_4", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    with pytest.raises(Exception, match=r"^ERROR: .*"):
        generator.realize_fresh("test_realization_case_4")
