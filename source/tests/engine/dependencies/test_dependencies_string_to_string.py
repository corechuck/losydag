import pytest
from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError

from LosydagGenerator import LosydagGenerator


def test_string_for_greater_then_dependency(
        prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterThenDependency(name="great_adventure_dependency_2", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[1]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table2_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_string_for_greater_then_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_2", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    with pytest.raises(Exception):
        generator.realize_fresh("test_realization_case_2")


def test_string_for_smaller_then_dependency(
        prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.SmallerThenDependency(name="great_adventure_dependency_4a", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[1]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def4a", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_string_for_smaller_then_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_4a", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    with pytest.raises(Exception):
        generator.realize_fresh("test_realization_case_4a")