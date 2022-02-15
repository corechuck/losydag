import pytest
from datetime import datetime
from LosydagGenerator import LosydagGenerator
from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError


def test_dates_for_format_dependency(
        request, prepared_core, prepared_table, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    try:
        testing_iri = "http://corechuck.com/testing/dependency_namespace"
        test_ontology = get_ontology(testing_iri)
        test_ontology.imported_ontologies.append(prepared_core)

        dependency_under_test = prepared_core.FormatDependency(name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
        dependency_under_test.has_format_definition = "test_format_{column_02}__{column_06}"

        table_2_realization_def = prepared_core.RealizationDefinition(
            name=f"rd_{test_case_title}", namespace=test_ontology)
        table_2_realization_def.has_constraints = [dependency_under_test]
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        realized_case = generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_02']}")
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_06']}")
    print(f"INFO: Dependent Value {realized_case['internal_test_table_01'][0]['column_07']}")
    col_2_value = realized_case["internal_test_table_01"][0]['column_02']
    col_6_value = realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_07'] == f"test_format_{col_2_value}__{col_6_value}"


def test_from_date_to_decimal_format_dependency(
        request, prepared_core, prepared_table, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    try:
        testing_iri = "http://corechuck.com/testing/dependency_namespace"
        test_ontology = get_ontology(testing_iri)
        test_ontology.imported_ontologies.append(prepared_core)

        dependency_under_test = prepared_core.FormatDependency(name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
        dependency_under_test.has_format_definition = "test_format_{column_04}__{column_06}"

        table_2_realization_def = prepared_core.RealizationDefinition(
            name=f"rd_{test_case_title}", namespace=test_ontology)
        table_2_realization_def.has_constraints = [dependency_under_test]
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        realized_case = generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_04']}")
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_06']}")
    print(f"INFO: Dependent Value {realized_case['internal_test_table_01'][0]['column_07']}")
    col_4_value = realized_case["internal_test_table_01"][0]['column_04']
    col_6_value = realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_07'] == f"test_format_{col_4_value}__{col_6_value}"


def test_from_decimal_to_date_format_dependency(
        request, prepared_core, prepared_table, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    try:
        testing_iri = "http://corechuck.com/testing/dependency_namespace"
        test_ontology = get_ontology(testing_iri)
        test_ontology.imported_ontologies.append(prepared_core)

        dependency_under_test = prepared_core.FormatDependency(name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
        dependency_under_test.has_format_definition = "test_format__{column_06}_{column_04}"

        table_2_realization_def = prepared_core.RealizationDefinition(
            name=f"rd_{test_case_title}", namespace=test_ontology)
        table_2_realization_def.has_constraints = [dependency_under_test]
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        realized_case = generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_04']}")
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_06']}")
    print(f"INFO: Dependent Value {realized_case['internal_test_table_01'][0]['column_07']}")
    col_4_value = realized_case["internal_test_table_01"][0]['column_04']
    col_6_value = realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_07'] == f"test_format__{col_6_value}_{col_4_value}"


def test_from_date_to_string_format_dependency(
        request, prepared_core, prepared_table, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    try:
        testing_iri = "http://corechuck.com/testing/dependency_namespace"
        test_ontology = get_ontology(testing_iri)
        test_ontology.imported_ontologies.append(prepared_core)

        dependency_under_test = prepared_core.FormatDependency(name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
        dependency_under_test.has_format_definition = "test_format_{column_02}__{column_06}"

        table_2_realization_def = prepared_core.RealizationDefinition(
            name=f"rd_{test_case_title}", namespace=test_ontology)
        table_2_realization_def.has_constraints = [dependency_under_test]
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        realized_case = generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_02']
    assert realized_case["internal_test_table_01"][0]['column_06']
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_02']}")
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_06']}")
    print(f"INFO: Dependent Value {realized_case['internal_test_table_01'][0]['column_07']}")
    col_2_value = realized_case["internal_test_table_01"][0]['column_02']
    col_6_value = realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_07'] == f"test_format_{col_2_value}__{col_6_value}"


def test_string_for_format_dependency(
        prepared_core, prepared_table, min_req_for_prepared_table):
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.FormatDependency(name="great_adventure_dependency_5", namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table.has_columns[6]
    dependency_under_test.has_format_definition = "test_format_{column_02}_{column_04}"

    table_2_realization_def = prepared_core.RealizationDefinition(name="table1_def5", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"test_string_for_format_dependency.owl")
        raise
    table_2_realization_def.compliment_with_min_reqs()

    test_realization = prepared_core.RealizationCase(name="test_realization_case_5", namespace=test_ontology)
    test_realization.contains_realizations = [table_2_realization_def]

    generator = LosydagGenerator(test_ontology)
    realized_case = generator.realize_fresh("test_realization_case_5")

    assert realized_case
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_02']}")
    print(f"INFO: Base Value {realized_case['internal_test_table_01'][0]['column_04']}")
    print(f"INFO: Dependent Value {realized_case['internal_test_table_01'][0]['column_07']}")
    col_2_value = realized_case["internal_test_table_01"][0]['column_02']
    col_4_value = realized_case["internal_test_table_01"][0]['column_04']

    assert col_2_value
    assert col_4_value
    assert realized_case["internal_test_table_01"][0]['column_07'] == f"test_format_{col_2_value}_{col_4_value}"
