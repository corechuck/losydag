from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError

from LosydagGenerator import LosydagGenerator


def test_decimals_for_greater_then_dependency(
        prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterThenDependency(name="great_adventure_dependency_2", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table2_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_decimals_for_greater_then_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_2", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_2")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_04']
    assert float(realized_case["internal_test_table_02"][0]['column_03']) > \
           float(realized_case["internal_test_table_01"][0]['column_04'])


def test_decimals_for_greater_then_or_equal_dependency(
        prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterOrEqualThenDependency(name="great_adventure_dependency_1", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_decimals_for_greater_then_or_equal_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_1", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_1")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_04']
    assert float(realized_case["internal_test_table_02"][0]['column_03']) >= \
           float(realized_case["internal_test_table_01"][0]['column_04'])


def test_decimals_for_smaller_then_or_equal_dependency(
        prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    # This failed occasionally
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.SmallerOrEqualThenDependency(name="great_andventure_dependency_3", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table3_def", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_decimals_for_smaller_then_or_equal_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_3", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_3")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_04']
    assert realized_case["internal_test_table_02"][0]['column_03'] <= \
           realized_case["internal_test_table_01"][0]['column_04']


def test_decimals_for_smaller_then_dependency(
        prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.SmallerThenDependency(name="great_adventure_dependency_4", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[2]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def4", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_decimals_for_smaller_then_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_4", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_4")

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_04']
    assert float(realized_case["internal_test_table_02"][0]['column_03']) < \
           float(realized_case["internal_test_table_01"][0]['column_04'])