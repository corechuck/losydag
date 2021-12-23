"""

"""
from datetime import datetime
from random import random
import pytest
from owlready2 import get_ontology, sync_reasoner_pellet
from LosydagGenerator import LosydagGenerator
from utils.invertion_factory import ConstraintInverter


@pytest.fixture()
def invert(prepared_core):
    inverter = ConstraintInverter(prepared_core)
    return inverter.invert


def test_negation_of_greater_then_or_equal_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.GreaterOrEqualThenDependency(name="negated_adventure_dependency_1", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(greater_then_or_equal_dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert not isinstance(negated_dependency, prepared_core.GreaterOrEqualThenDependency)
    assert isinstance(negated_dependency, prepared_core.SmallerThenDependency)


def test_negation_greater_then_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.GreaterThenDependency(name="negated_adventure_dependency_2", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(greater_then_or_equal_dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert not isinstance(negated_dependency, prepared_core.GreaterThenDependency)
    assert isinstance(negated_dependency, prepared_core.SmallerOrEqualThenDependency)


def test_negation_smaller_then_or_equal_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.SmallerOrEqualThenDependency(name="negated_adventure_dependency_3", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(greater_then_or_equal_dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert not isinstance(negated_dependency, prepared_core.SmallerOrEqualThenDependency)
    assert isinstance(negated_dependency, prepared_core.GreaterThenDependency)


def test_negation_smaller_then_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    greater_then_or_equal_dependency_under_test = \
        prepared_core.SmallerThenDependency(name="negated_adventure_dependency_4", namespace=test_ontology)
    greater_then_or_equal_dependency_under_test.is_constraining_column = prepared_table_2.has_columns[0]
    greater_then_or_equal_dependency_under_test.is_depending_on_column = prepared_table.has_columns[0]

    negated_dependency_group = invert(greater_then_or_equal_dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert not isinstance(negated_dependency, prepared_core.SmallerThenDependency)
    assert isinstance(negated_dependency, prepared_core.GreaterOrEqualThenDependency)


def test_negation_format_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    format_dependency_under_test = \
        prepared_core.FormatDependency(name="negated_adventure_dependency_5", namespace=test_ontology)
    format_dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    format_dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    format_dependency_under_test.is_a.append(prepared_core.Negation)

    negated_dependency_group = invert(format_dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert isinstance(negated_dependency, prepared_core.FormatDependency)
    assert not isinstance(negated_dependency, prepared_core.Negation)


def test_negation_equal_dependency(prepared_core, invert, prepared_table, prepared_table_2):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    format_dependency_under_test = \
        prepared_core.EqualToDependency(name="negated_adventure_dependency_6", namespace=test_ontology)
    format_dependency_under_test.is_constraining_column = prepared_table.has_columns[1]
    format_dependency_under_test.has_format_definition = "test_format_{column_01}_{column_03}"
    # format_dependency_under_test.is_a.append(prepared_core.Negation)

    negated_dependency_group = invert(format_dependency_under_test)

    assert negated_dependency_group
    assert len(negated_dependency_group.has_constraints) == 1
    negated_dependency = negated_dependency_group.has_constraints[0]
    assert isinstance(negated_dependency, prepared_core.EqualToDependency)
    assert isinstance(negated_dependency, prepared_core.Negation)

