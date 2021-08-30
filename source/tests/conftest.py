import os
from datetime import datetime

import pytest
from _pytest.fixtures import fixture

from owlready2 import get_ontology, sync_reasoner_pellet, onto_path, destroy_entity
from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
from core_classes.SimpleExtensions import extend_core as extend_simple_types
from core_classes.Dependencies import extend_core as extend_dependencies
from core_classes.RealizationCase import extend_core as extend_realization_case


@fixture(scope="session")
def prepared_core():
    onto_path.append(f"{os.getcwd()}/resources/core/")
    onto_path.append(f"{os.getcwd()}/resources/development/")

    schema_iri = "http://corechuck.com/modeling/core_check"
    core = get_ontology(schema_iri)
    core.load(only_local=True)
    extend_constraints(core)
    extend_dependencies(core)
    extend_constraint_groups(core)
    extend_simple_types(core)
    extend_realization_case(core)
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    return core


@fixture()
def prepared_table(prepared_core):
    min_reqs = prepared_core.ConstraintGroup(f"min_req_{datetime.now()}")
    pre_table = prepared_core.Table("internal_test_table_01")
    pre_table.has_min_reqs = min_reqs
    column_1 = prepared_core.Column("Column.Internal1.column_01")
    pre_table.has_columns.append(column_1)
    column_2 = prepared_core.Column("Column.Internal1.column_02")
    pre_table.has_columns.append(column_2)
    yield pre_table
    destroy_entity(column_1)
    destroy_entity(column_2)
    destroy_entity(min_reqs)
    destroy_entity(pre_table)


@fixture()
def prepared_table_2(prepared_core):
    min_reqs = prepared_core.ConstraintGroup(f"min_req_2_{datetime.now()}")
    pre_table = prepared_core.Table("internal_test_table_02")
    pre_table.has_min_reqs = min_reqs
    column_1 = prepared_core.Column("Column.Internal2.column_01")
    pre_table.has_columns.append(column_1)
    column_2 = prepared_core.Column("Column.Internal2.column_02")
    pre_table.has_columns.append(column_2)
    yield pre_table
    destroy_entity(column_1)
    destroy_entity(column_2)
    destroy_entity(min_reqs)
    destroy_entity(pre_table)


@fixture()
def prepared_column(prepared_core, prepared_table):
    yield prepared_table.has_columns[0]


@fixture()
def list_constraint_under_test(prepared_core, prepared_column):
    list_const = prepared_core.ListConstraint(f"list_req_{datetime.now()}")
    list_const.is_constraining_column = prepared_column
    list_const.has_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']
    yield list_const
    destroy_entity(list_const)


@fixture()
def min_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("sgfgegawe")
    range_const.is_constraining_column = prepared_column
    range_const.has_min_range = 40
    return range_const
    destroy_entity(range_const)


@fixture()
def max_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("gajskdufhakdh")
    range_const.is_constraining_column = prepared_column
    range_const.has_max_range = 40
    return range_const


@fixture()
def actual_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("akjsdhflaishd")
    range_const.is_constraining_column = prepared_column
    range_const.has_max_range = 40
    range_const.has_min_range = 10
    return range_const


@fixture()
def regex_constraint_under_test(prepared_core, prepared_column):
    regex_const = prepared_core.RegexConstraint("rekajnisokdljf")
    regex_const.is_constraining_column = prepared_column
    regex_const.has_regex_format = "[a-z]oo"
    return regex_const
