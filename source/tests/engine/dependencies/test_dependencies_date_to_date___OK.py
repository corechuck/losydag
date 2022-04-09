import pytest
from datetime import datetime

from tests.engine.dependencies.conftest import perform_dependency_test
from utils.utils import ValueGenerationException

EXPECTED_DATE_FORMAT = "%Y-%m-%d"


def test_dates_for_greater_dependency(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-12-30")
    date_rng_const.set_right_boundary("2200-12-30")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.GreaterThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_06'] in ["2200-12-30"]
    assert realized_case["internal_test_table_02"][0]['column_04'] in ["2200-12-31"]


def test_dates_for_greater_or_equal_dependency_max_case(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-12-31")
    date_rng_const.set_right_boundary("2200-12-31")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.GreaterOrEqualThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_06'] in ["2200-12-31"]
    assert realized_case["internal_test_table_02"][0]['column_04'] in ["2200-12-31"]


def test_dates_for_greater_or_equal_dependency(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.GreaterOrEqualThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert datetime.strptime(realized_case["internal_test_table_02"][0]['column_04'], EXPECTED_DATE_FORMAT) >= \
           datetime.strptime(realized_case["internal_test_table_01"][0]['column_06'], EXPECTED_DATE_FORMAT)


def test_dates_for_smaller_dependency(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("1900-01-02")
    date_rng_const.set_right_boundary("1900-01-02")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.SmallerThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_06'] in ["1900-01-02"]
    assert realized_case["internal_test_table_02"][0]['column_04'] in ["1900-01-01"]


def test_dates_for_smaller_or_equal_dependency_min_case(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("1900-01-01")
    date_rng_const.set_right_boundary("1900-01-01")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.SmallerOrEqualThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_06'] in ["1900-01-01"]
    assert realized_case["internal_test_table_02"][0]['column_04'] in ["1900-01-01"]


def test_dates_for_smaller_or_equal_dependency(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.SmallerOrEqualThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert datetime.strptime(realized_case["internal_test_table_02"][0]['column_04'], EXPECTED_DATE_FORMAT) <= \
           datetime.strptime(realized_case["internal_test_table_01"][0]['column_06'], EXPECTED_DATE_FORMAT)


def test_dates_for_equal_dependency(
        request, prepared_core, prepared_table, prepared_table_2, min_req_for_prepared_table):
    test_case_title = request.node.name
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2000-01-01")
    date_rng_const.set_right_boundary("2100-12-31")

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.EqualToDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_02"][0]['column_04'] == \
           realized_case["internal_test_table_01"][0]['column_06']


def test_dates_from_days_to_seconds_precision(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-12-30")
    date_rng_const.set_right_boundary("2200-12-30")
    test_case_title = request.node.name

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.GreaterThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[4]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert realized_case["internal_test_table_01"][0]['column_06'] in ["2200-12-30"]
    assert prepared_table_2.has_columns[4].has_data_type.parse_if_needed(
        realized_case["internal_test_table_02"][0]['column_05']) > datetime.strptime(realized_case['internal_test_table_01'][0]['column_06'], EXPECTED_DATE_FORMAT)


def test_dates_from_seconds_to_days_precision_exception(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    prepared_table.has_columns[5].has_data_type.has_date_format = "%Y-%m-%d %H:%M:%S"

    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("1900-01-01 10:00:00")
    date_rng_const.set_right_boundary("1900-01-01 15:00:00")
    test_case_title = request.node.name

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.SmallerThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test
    with pytest.raises(ValueGenerationException):
        realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)


def test_dates_from_seconds_to_days_precision(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    prepared_table.has_columns[5].has_data_type.has_date_format = "%Y-%m-%d %H:%M:%S"

    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("1900-01-02 00:00:00")
    date_rng_const.set_right_boundary("1900-01-02 15:00:00")
    test_case_title = request.node.name

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.SmallerThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert datetime.strptime(realized_case["internal_test_table_02"][0]['column_04'], EXPECTED_DATE_FORMAT) < \
           prepared_table.has_columns[5].has_data_type.parse_if_needed(
               realized_case["internal_test_table_01"][0]['column_06'])


def test_dates_from_years_to_days_precision(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    prepared_table.has_columns[5].has_data_type.has_date_format = "%Y"

    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("1901")
    date_rng_const.set_right_boundary("1901")
    test_case_title = request.node.name

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.SmallerOrEqualThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert datetime.strptime(realized_case["internal_test_table_02"][0]['column_04'], EXPECTED_DATE_FORMAT) <= \
           prepared_table.has_columns[5].has_data_type.parse_if_needed(
               realized_case["internal_test_table_01"][0]['column_06'])


def test_dates_from_hours_to_months_precision(
        prepared_core, request, prepared_table, prepared_table_2, min_req_for_prepared_table):
    prepared_table.has_columns[5].has_data_type.has_date_format = "%Y-%m-%d %H:%M"
    prepared_table_2.has_columns[3].has_data_type.has_date_format = "%Y-%m"

    date_rng_const = prepared_table.has_min_reqs.has_constraints[2]
    date_rng_const.set_left_boundary("2200-11-12 10:00")
    date_rng_const.set_right_boundary("2200-11-30 19:00")
    test_case_title = request.node.name

    def dependency_maker(test_ontology):
        dependency_under_test = prepared_core.GreaterOrEqualThenDependency(
            name=test_case_title, namespace=test_ontology)
        dependency_under_test.is_depending_on_column = prepared_table.has_columns[5]
        dependency_under_test.is_constraining_column = prepared_table_2.has_columns[3]
        return dependency_under_test

    realized_case = perform_dependency_test(prepared_core, test_case_title, dependency_maker)

    assert realized_case
    assert realized_case["internal_test_table_01"][0]['column_06']
    assert prepared_table_2.has_columns[3].has_data_type.parse_if_needed(
        realized_case["internal_test_table_02"][0]['column_04']) >= prepared_table.has_columns[
               5].has_data_type.parse_if_needed(realized_case['internal_test_table_01'][0]['column_06'])



# def test_from_date_to_decimal_greater_dependency
# def test_from_date_to_decimal_greater_or_equal_dependency
# def test_from_date_to_decimal_smaller_dependency
# def test_from_date_to_decimal_smaller_or_equal_dependency
# def test_from_date_to_decimal_equal_dependency
# def test_from_date_to_decimal_format_dependency

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
