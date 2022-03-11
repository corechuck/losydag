from datetime import datetime

import pytest
from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError

from LosydagGenerator import LosydagGenerator
from utils.utils import DataTypeIssueException

EXPECTED_DATE_FORMAT = "%Y-%m-%d"



def test_from_decimal_to_date_greater_dependency(
        request, prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-12-30")
    date_rng_const.set_right_boundary("2200-12-30")

    test_case_title = request.node.name
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterThenDependency(name=test_case_title, namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name=f"rd_{test_case_title}", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        with pytest.raises(DataTypeIssueException):
            generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise


def test_from_decimal_to_date_greater_or_equal_dependency(
        request, prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-12-31")
    date_rng_const.set_right_boundary("2200-12-31")

    test_case_title = request.node.name
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.GreaterOrEqualThenDependency(name=test_case_title, namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name=f"rd_{test_case_title}", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        with pytest.raises(DataTypeIssueException):
            generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise


def test_from_decimal_to_date_smaller_dependency(
        request, prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-12-31")
    date_rng_const.set_right_boundary("2200-12-31")

    test_case_title = request.node.name
    print("INFO: Generating RealizationCase.Check1 in fixture:")
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = \
        prepared_core.SmallerThenDependency(name=test_case_title, namespace=test_ontology)
    dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
    dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

    table_2_realization_def = prepared_core.RealizationDefinition(name=f"rd_{test_case_title}", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        with pytest.raises(DataTypeIssueException):
            generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise


def test_from_decimal_to_date_smaller_or_equal_dependency(
        request, prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    try:
        testing_iri = "http://corechuck.com/testing/dependency_namespace"
        test_ontology = get_ontology(testing_iri)
        test_ontology.imported_ontologies.append(prepared_core)

        dependency_under_test = \
            prepared_core.SmallerOrEqualThenDependency(name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

        table_2_realization_def = prepared_core.RealizationDefinition(name=f"rd_{test_case_title}", namespace=test_ontology)
        table_2_realization_def.has_constraints = [dependency_under_test]
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        with pytest.raises(DataTypeIssueException):
            data = generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise


def test_from_decimal_to_date_equal_dependency(
        request, prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    try:
        testing_iri = "http://corechuck.com/testing/dependency_namespace"
        test_ontology = get_ontology(testing_iri)
        test_ontology.imported_ontologies.append(prepared_core)

        dependency_under_test = \
            prepared_core.EqualToDependency(name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[3]

        table_2_realization_def = prepared_core.RealizationDefinition(
            name=f"rd_{test_case_title}", namespace=test_ontology)
        table_2_realization_def.has_constraints = [dependency_under_test]
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        with pytest.raises(DataTypeIssueException):
            data = generator.realize_fresh(f"case_{test_case_title}")
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise


# def test_from_date_to_string_greater_dependency
# def test_from_date_to_string_greater_or_equal_dependency
# def test_from_date_to_string_smaller_dependency
# def test_from_date_to_string_smaller_or_equal_dependency
# def test_from_date_to_string_equal_dependency
# def test_from_date_to_string_format_dependency

# def test_from_decimal_to_date_greater_dependency
# def test_from_decimal_to_date_greater_or_equal_dependency
# def test_from_decimal_to_date_smaller_dependency
# def test_from_decimal_to_date_smaller_or_equal_dependency
# def test_from_decimal_to_date_equal_dependency
# def test_from_decimal_to_date_format_dependency

# def test_from_decimal_to_string_greater_dependency
# def test_from_decimal_to_string_greater_or_equal_dependency
# def test_from_decimal_to_string_smaller_dependency
# def test_from_decimal_to_string_smaller_or_equal_dependency
# def test_from_decimal_to_string_equal_dependency
# def test_from_decimal_to_string_format_dependency

#      from \ to |   date | decimal | string |  bool |
# ---------------|--------|---------|--------|-------|
#          date  |      D |       # |      # |       |
#        decimal |      # |       D |      # |       |
#   valid string |      # |       # |      D |       |
# invalid string |      # |       # |      - |       |
#           bool |        |         |        |     # |

# >> means to column defines range constraint for dependency
# << means from column defines range constraint for dependency
#      from \ to |   date | decimal |  string |   bool |
# ---------------|--------|---------|---------|--------|
#          date  |    C>> |     C>> |      << |        |
#        decimal |    C>> |     c>> |      << |        |
#   valid string |    C>> |     C>> | only == |        |
# invalid string |    C>> |     C>> | only == |        |
#           bool |        |         |         |      # |


# def test_from_numeric_string_to_decimal_greater_dependency
# def test_from_numeric_string_to_decimal_greater_or_equal_dependency
# def test_from_numeric_string_to_decimal_smaller_dependency
# def test_from_numeric_string_to_decimal_smaller_or_equal_dependency
# def test_from_numeric_string_to_decimal_equal_dependency
# def test_from_numeric_string_to_decimal_format_dependency
# def test_from_non_numeric_string_to_decimal_greater_dependency
# def test_from_non_numeric_string_to_decimal_greater_or_equal_dependency
# def test_from_non_numeric_string_to_decimal_smaller_dependency
# def test_from_non_numeric_string_to_decimal_smaller_or_equal_dependency
# def test_from_non_numeric_string_to_decimal_equal_dependency
# def test_from_non_numeric_string_to_decimal_format_dependency

# def test_from_valid_string_to_date_greater_dependency
# def test_from_valid_string_to_date_greater_or_equal_dependency
# def test_from_valid_string_to_date_smaller_dependency
# def test_from_valid_string_to_date_smaller_or_equal_dependency
# def test_from_valid_string_to_date_equal_dependency
# def test_from_valid_string_to_date_format_dependency
# def test_from_invalid_string_to_date_greater_dependency
# def test_from_invalid_string_to_date_greater_or_equal_dependency
# def test_from_invalid_string_to_date_smaller_dependency
# def test_from_invalid_string_to_date_smaller_or_equal_dependency
# def test_from_invalid_string_to_date_equal_dependency
# def test_from_invalid_string_to_date_format_dependency

# -----------------------------------

# def test_booleans_for_greater_dependency:
# def test_booleans_for_greater_or_equal_dependency:
# def test_booleans_for_smaller_dependency:
# def test_booleans_for_smaller_or_equal_dependency:
# def test_booleans_for_equal_dependency:
# def test_booleans_for_format_dependency:


# test order of value dependencies, when dependency constraints col2 and formats values in later columns
# it will have to get into second try of fulfilling constraints, therefore identifies that something has already
# fulfilled constraint for later columns.
