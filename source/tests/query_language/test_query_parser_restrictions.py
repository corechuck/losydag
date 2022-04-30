import pytest
from owlready2 import destroy_entity
from generation_request.syntax_parser import GenerationRequestSyntaxParser


def get_line_constraint(group, line_number):
    expected_line_constraint = f"restriction_from_line_{line_number}"
    for constraint in group.has_constraints:
        if constraint.name == expected_line_constraint:
            return constraint
    return None


class TestingRestrictions:

    @pytest.fixture(scope="class")
    def parsed_query_4(self, prepared_core):
        parser = GenerationRequestSyntaxParser("resources/development/")
        query_group = parser.parse_request_from_file(
            "source/tests/query_language/test_queries/query4_restrictions.grs")
        yield query_group
        destroy_entity(query_group)

    def test_not_in_list_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 6
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.ListConstraint)

    def test_not_smaller_then_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 7
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RangeConstraint)

    def test_not_smaller_equal_then_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 8
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RangeConstraint)

    def test_not_greater_then_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 9
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RangeConstraint)

    def test_not_greater_equal_then_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 10
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RangeConstraint)

    def test_not_smaller_or_equal_then_date_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 11
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RangeConstraint)

    def test_not_greater_then_date_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 12
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RangeConstraint)

    def test_not_match_regex_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 13
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.RegexConstraint)

    def test_not_format_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 14
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.FormatDependency)

    def test_not_equal_dependency_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 15
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.ValueDependency)

    def test_not_equal_sign_dependency_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 16
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.ValueDependency)

    def test_not_smaller_then_dependency_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 17
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.SmallerThenDependency)

    def test_not_smaller_or_equal_dependency_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 18
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.SmallerOrEqualThenDependency)

    def test_not_greater_then_dependency_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 19
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.GreaterThenDependency)

    def test_not_greater_or_equal_dependency_is_parsed(self, prepared_core, parsed_query_4):
        for_line_number = 20
        found_line_constraint = get_line_constraint(parsed_query_4, for_line_number)
        assert found_line_constraint
        assert found_line_constraint.restriction_definition.name == f"constraint_from_line_{for_line_number}"
        assert isinstance(found_line_constraint.restriction_definition, prepared_core.GreaterOrEqualThenDependency)


