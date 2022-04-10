from datetime import datetime

import pytest
from owlready2 import get_ontology, sync_reasoner_pellet

from generation_request.syntax_parser import GenerationRequestSyntaxParser


# 1. Command line run of query
# 2. Parser to respect Generate command statement
# 3.

@pytest.fixture(scope="session")
def parsed_query_2(prepared_core):
    schema_iri = "http://corechuck.com/modeling/dependent_onto"

    onto = get_ontology(schema_iri)
    onto.load(only_local=True)
    sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)

    parser = GenerationRequestSyntaxParser(onto)
    query_group = parser.parse_request_from_file(
        "source/tests/query_language/test_queries/query2_flat_all.grs")
    return query_group


def get_line_constraint(group, line_number):
    expected_line_constraint = f"constraint_from_line_{line_number}"
    for constraint in group.has_constraints:
        if constraint.name == expected_line_constraint:
            return constraint
    return None


def test_smaller_then_is_parsed(prepared_core, parsed_query_2):
    found_line_constraint = get_line_constraint(parsed_query_2, 5)
    assert found_line_constraint.has_right_boundary.has_boundary_value == 0.1
    assert isinstance(found_line_constraint.has_right_boundary, prepared_core.OpenRangeBoundary)


def test_smaller_equal_then_is_parsed(prepared_core, parsed_query_2):
    found_line_constraint = get_line_constraint(parsed_query_2, 6)
    assert found_line_constraint.has_right_boundary.has_boundary_value == 0.2
    assert isinstance(found_line_constraint.has_right_boundary, prepared_core.ClosedRangeBoundary)


def test_great_then_is_parsed(prepared_core, parsed_query_2):
    found_line_constraint = get_line_constraint(parsed_query_2, 7)
    assert found_line_constraint.has_left_boundary.has_boundary_value == 0.3
    assert isinstance(found_line_constraint.has_left_boundary, prepared_core.ClosedRangeBoundary)


def test_great_equal_then_is_parsed(prepared_core, parsed_query_2):
    found_line_constraint = get_line_constraint(parsed_query_2, 8)
    assert found_line_constraint.has_left_boundary.has_boundary_value == 0.4
    assert isinstance(found_line_constraint.has_left_boundary, prepared_core.OpenRangeBoundary)


def test_smaller_then_date_is_parsed(prepared_core, parsed_query_2):
    found_line_constraint = get_line_constraint(parsed_query_2, 9)
    assert found_line_constraint.has_left_boundary.has_boundary_value == datetime.strptime("1990-02-14", '%Y-%m-%d')
    assert isinstance(found_line_constraint.has_left_boundary, prepared_core.OpenRangeBoundary)


def test_great_equal_then_date_is_parsed(prepared_core, parsed_query_2):
    found_line_constraint = get_line_constraint(parsed_query_2, 10)
    assert found_line_constraint.has_right_boundary.has_boundary_value == datetime.strptime("1990-02-15", '%Y-%m-%d')
    assert isinstance(found_line_constraint.has_right_boundary, prepared_core.ClosedRangeBoundary)


