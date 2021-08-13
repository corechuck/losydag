import os
import pytest

from owlready2 import get_ontology, sync_reasoner_pellet, onto_path
from core_classes.Constraints import extend_core as extend_constraints


# def prepare_constraint_for_test():
#     schema_iri = "http://corechuck.com/modeling/dependent_onto"
#     onto = get_ontology(schema_iri)
#     onto.load(only_local=True)
#
#     core = onto.imported_ontologies[0]  # <- core classes are in wrong ontology
#     extend_constraints(core)
#
#     sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
#
#     return onto, core


def test_not_picks_restricts_generation(prepared_core):
    list_constraint_under_test = prepared_core.ListConstraint()
    list_constraint_under_test.has_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD']
    list_constraint_under_test.not_picks = ['xD', 'moo', '1']

    result = dict()
    for i in range(100):
        assert list_constraint_under_test.generate(result) in ['foo', 'baa', '-3.14']


def test_not_matching_regexes_restricts_generation(prepared_core):
    list_constraint_under_test = prepared_core.ListConstraint()
    list_constraint_under_test.has_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD']
    list_constraint_under_test.not_matching_regexes = [".oo"]

    result = dict()
    for i in range(100):
        assert list_constraint_under_test.generate(result) in ['1', 'baa', '-3.14', 'xD']


def test_not_matching_regexes_with_picks_restricts_generation_for_regex(prepared_core):
    regex_constraint_under_test = prepared_core.RegexConstraint()
    regex_constraint_under_test.has_regex_format = "TT_[abc]_[4567]"
    regex_constraint_under_test.not_picks = ['TT_b_7', 'TT_c_4', 'TT_c_5']
    regex_constraint_under_test.not_matching_regexes = ["TT_a.*"]

    result = dict()
    for i in range(100):
        assert regex_constraint_under_test.generate(result) in \
               ['TT_b_4', 'TT_b_5', 'TT_b_6', 'TT_c_6', 'TT_c_7']
