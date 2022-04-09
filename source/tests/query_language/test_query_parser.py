from owlready2 import get_ontology, sync_reasoner_pellet

from generation_request.syntax_parser import GenerationRequestSyntaxParser


def test_parser_reads_query_from_files(prepared_core):
    schema_iri = "http://corechuck.com/modeling/dependent_onto"

    onto = get_ontology(schema_iri)
    onto.load(only_local=True)
    sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)

    parser = GenerationRequestSyntaxParser(onto)
    realization_case = parser.parse_request_from_file("source/tests/query_language/test_queries/query1.grs")
    assert realization_case

