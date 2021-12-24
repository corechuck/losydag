import pytest
from owlready2 import get_ontology, sync_reasoner_pellet

from LosydagGenerator import LosydagGenerator


def test_greater_then_or_equal_dependency(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.GreaterOrEqualThenDependency(name="great_adventure_dependency_1", namespace=test_ontology)
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

    greater_then_dependency_under_test = \
        prepared_core.GreaterThenDependency(name="great_adventure_dependency_2", namespace=test_ontology)
    greater_then_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    greater_then_dependency_under_test.is_depending_on_column = prepared_table.has_columns[2]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table2_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_2", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_2")

    assert realized_case
    assert float(realized_case["internal_test_table_02"][0]['column_03']) > \
           float(realized_case["internal_test_table_01"][0]['column_03'])


def test_greater_then_dependency_for_string(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_dependency_under_test = \
        prepared_core.GreaterThenDependency(name="great_adventure_dependency_2", namespace=test_ontology)
    greater_then_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table2_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [greater_then_dependency_under_test]
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

    smaller_then_or_equal_dependency_under_test = \
        prepared_core.SmallerOrEqualThenDependency(name="great_andventure_dependency_3", namespace=test_ontology)
    smaller_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    smaller_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table3_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [smaller_then_or_equal_dependency_under_test]
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

    smaller_then_dependency_under_test = \
        prepared_core.SmallerThenDependency(name="great_adventure_dependency_4", namespace=test_ontology)
    smaller_then_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    smaller_then_dependency_under_test.is_depending_on_column = prepared_table.has_columns[2]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def4", namespace=test_ontology)
    table_2_realization_def.has_constraints = [smaller_then_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_4", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_4")

    assert realized_case
    assert float(realized_case["internal_test_table_02"][0]['column_03']) < \
           float(realized_case["internal_test_table_01"][0]['column_03'])


def test_smaller_then_dependency_for_string(prepared_core, prepared_table, prepared_table_2):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    smaller_then_dependency_under_test = \
        prepared_core.SmallerThenDependency(name="great_adventure_dependency_4a", namespace=test_ontology)
    smaller_then_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    smaller_then_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def4a", namespace=test_ontology)
    table_2_realization_def.has_constraints = [smaller_then_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_4a", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    with pytest.raises(Exception, match=r"^ERROR: .*"):
        generator.realize_fresh("test_realization_case_4a")


def test_format_dependency_for_string(prepared_core, prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    format_dependency_under_test = \
        prepared_core.FormatDependency(name="great_adventure_dependency_5", namespace=test_ontology)
    format_dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    format_dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def5", namespace=test_ontology)
    table_2_realization_def.has_constraints = [format_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_5", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_5")

    assert realized_case
    col_1_value = realized_case["internal_test_table_01"][0]['column_01']
    col_3_value = realized_case["internal_test_table_01"][0]['column_03']

    assert realized_case["internal_test_table_01"][0]['column_02'] == f"test_format_{col_1_value}_{col_3_value}"


def test_negated_format_dependency_for_string(prepared_core, prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    format_dependency_under_test = \
        prepared_core.FormatDependency(name="great_adventure_dependency_6", namespace=test_ontology)
    format_dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    format_dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    format_dependency_under_test.is_a.append(prepared_core.Negation)

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def6", namespace=test_ontology)
    table_2_realization_def.has_constraints = [format_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_6", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_6")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_02'] == 'None'


def test_negated_equal_dependency_for_string(prepared_core, prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    format_dependency_under_test = \
        prepared_core.EqualToDependency(name="great_adventure_dependency_7", namespace=test_ontology)
    format_dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    format_dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    format_dependency_under_test.is_a.append(prepared_core.Negation)

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def7", namespace=test_ontology)
    table_2_realization_def.has_constraints = [format_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_7", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_7")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_02'] == 'None'


def test_negated_value_dependency_for_string(prepared_core, prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    format_dependency_under_test = \
        prepared_core.ValueDependency(name="great_adventure_dependency_8", namespace=test_ontology)
    format_dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    format_dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    format_dependency_under_test.is_a.append(prepared_core.Negation)

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def8", namespace=test_ontology)
    table_2_realization_def.has_constraints = [format_dependency_under_test]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_8", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_8")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_02'] == 'None'

# test order of value dependencies, when dependency constraints col2 and formats values in later columns
# it will have to get into second try of fulfilling constraints, therefore idenftifies that somehting has already
# fulfilled constraint for later columns.
