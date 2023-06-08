from owlready2 import get_ontology, sync_reasoner_pellet

from generation_request.syntax_parser import GenerationRequestSyntaxParser


# 1. Command line run of query
# 2. Parser to respect Generate command statement
# 3.


#
# def test_parser_reads_query_from_files(prepared_core):
#     pass
#
#
def test_parser_control_statement_example(prepared_core):

    schema_iri = "http://corechuck.com/modeling/dependent_onto"

    onto = get_ontology(schema_iri)
    onto.load(only_local=True)
    sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)

    parser = GenerationRequestSyntaxParser(onto)
    query_group = parser.parse_request_from_file("source/tests/query_language/test_queries/query1_and.grs")
    query_group.pick_branches_from_or_groups()
    realization_case = query_group.build_realization_case()
    data = realization_case.realize()
    assert data


def test_parser_control_statement_positive_cases(prepared_core):

    schema_iri = "http://corechuck.com/modeling/dependent_onto"

    onto = get_ontology(schema_iri)
    onto.load(only_local=True)
    sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)

    parser = GenerationRequestSyntaxParser(onto)
    query_group = parser.parse_request_from_file("source/tests/query_language/test_queries/query1_and.grs")
    cases = query_group.prepare_positive_cases()
    assert cases



