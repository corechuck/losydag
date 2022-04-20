import pytest
from owlready2 import get_ontology, sync_reasoner_pellet, destroy_entity
from generation_request.syntax_parser import GenerationRequestSyntaxParser


def get_line_constraint(group, line_number):
    expected_line_constraint = f"constraint_from_line_{line_number}"
    for constraint in group.has_constraints:
        if constraint.name == expected_line_constraint:
            return constraint
    return None


class TestDependencies:

    @pytest.fixture(scope="class")
    def loaded_onto(self, prepared_core):
        schema_iri = "http://corechuck.com/modeling/dependent_onto"

        onto = get_ontology(schema_iri)
        onto.load(only_local=True, reload=True)
        sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)
        yield onto
        onto.destroy()

    @pytest.fixture(scope="class")
    def parsed_query_3(self, prepared_core, loaded_onto):
        parser = GenerationRequestSyntaxParser(loaded_onto)
        query_group = parser.parse_request_from_file(
            "source/tests/query_language/test_queries/query3_dependencies.grs")
        yield query_group
        destroy_entity(query_group)

    def test_format_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 6)
        assert isinstance(found_line_constraint, prepared_core.FormatDependency)
        assert found_line_constraint.has_format_definition == "Here{Col2_d}XX0000{Col3_text}"

    def test_equal_to_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 7)
        assert isinstance(found_line_constraint, prepared_core.ValueDependency)
        assert found_line_constraint.is_depending_on_realization
        assert found_line_constraint.is_constraining_column == loaded_onto.search_one(iri="*Column.Test1.Col1_n")
        assert found_line_constraint.is_depending_on_column == \
               loaded_onto.search_one(iri="*Column.Test1.Col4_not_constrained")

    def test_equal_sign_to_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 8)
        assert isinstance(found_line_constraint, prepared_core.ValueDependency)
        assert found_line_constraint.is_depending_on_realization
        assert found_line_constraint.is_constraining_column == loaded_onto.search_one(iri="*Column.Test1.Col1_n")
        assert found_line_constraint.is_depending_on_column == \
               loaded_onto.search_one(iri="*Column.Test1.Col4_not_constrained")

    def test_smaller_then_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 9)
        assert isinstance(found_line_constraint, prepared_core.SmallerThenDependency)
        assert found_line_constraint.is_depending_on_realization
        assert found_line_constraint.is_constraining_column == loaded_onto.search_one(iri="*Column.Test1.Col1_n")
        assert found_line_constraint.is_depending_on_column == \
               loaded_onto.search_one(iri="*Column.Test1.Col4_not_constrained")

    def test_smaller_then_or_equal_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 10)
        assert isinstance(found_line_constraint, prepared_core.SmallerOrEqualThenDependency)
        assert found_line_constraint.is_depending_on_realization
        assert found_line_constraint.is_constraining_column == loaded_onto.search_one(iri="*Column.Test1.Col2_d")
        assert found_line_constraint.is_depending_on_column == \
               loaded_onto.search_one(iri="*Column.Test1.Col1_n")

    def test_greater_then_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 11)
        assert isinstance(found_line_constraint, prepared_core.GreaterThenDependency)
        assert found_line_constraint.is_depending_on_realization
        assert found_line_constraint.is_constraining_column == loaded_onto.search_one(iri="*Column.Test1.Col2_d")
        assert found_line_constraint.is_depending_on_column == \
               loaded_onto.search_one(iri="*Column.Test1.Col4_not_constrained")

    def test_greater_then_or_equal_is_parsed(self, prepared_core, parsed_query_3, loaded_onto):
        found_line_constraint = get_line_constraint(parsed_query_3, 12)
        assert isinstance(found_line_constraint, prepared_core.GreaterOrEqualThenDependency)
        assert found_line_constraint.is_depending_on_realization
        assert found_line_constraint.is_constraining_column == loaded_onto.search_one(iri="*Column.Test1.Col1_n")
        assert found_line_constraint.is_depending_on_column == \
               loaded_onto.search_one(iri="*Column.Test1.Col2_d")
