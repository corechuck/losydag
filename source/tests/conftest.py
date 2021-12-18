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
from utils.context import ExtensionContext
from utils.value_generator_supervisor import ValueGenerationSupervisor


@fixture(scope="session")
def prepared_core():
    onto_path.append(f"{os.getcwd()}/resources/core/")
    onto_path.append(f"{os.getcwd()}/resources/development/")

    schema_iri = "http://corechuck.com/modeling/core_check"
    core = get_ontology(schema_iri)
    core.load(only_local=True)
    context = ExtensionContext()
    context.core = core
    context.value_generation_supervisor = ValueGenerationSupervisor()

    extend_constraints(context)
    extend_dependencies(context)
    extend_constraint_groups(context)
    extend_simple_types(context)
    extend_realization_case(context)
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    return core


@fixture()
def min_req_list_constraint_under_test(prepared_core):
    list_const = prepared_core.ListConstraint(f"list_req_{datetime.now()}")
    list_const.has_picks = ['col1_pick1', 'col1_pick2', 'col1_pick3']
    yield list_const
    # destroy_entity(list_const)

@fixture()
def min_req_range_constraint_under_test(prepared_core):
    range_const = prepared_core.RangeConstraint("lmgjkhawopinvzdff")
    range_const.set_left_boundary(40)
    yield range_const
    # destroy_entity(range_const)


@fixture()
def prepared_table(prepared_core, min_req_list_constraint_under_test, min_req_range_constraint_under_test):
    min_reqs = prepared_core.ConstraintGroup(f"min_req_{datetime.now()}")
    min_reqs.has_constraints = [min_req_list_constraint_under_test, min_req_range_constraint_under_test]

    pre_table = prepared_core.Table("internal_test_table_01")
    pre_table.has_min_reqs = min_reqs
    column_1 = prepared_core.Column("Column.Internal1.column_01")
    min_req_list_constraint_under_test.is_constraining_column = column_1
    pre_table.has_columns.append(column_1)
    column_2 = prepared_core.Column("Column.Internal1.column_02")
    pre_table.has_columns.append(column_2)
    column_3 = prepared_core.Column("Column.Internal1.column_03")
    min_req_range_constraint_under_test.is_constraining_column = column_3
    pre_table.has_columns.append(column_3)
    data_type_col_3 = prepared_core.Decimal()
    data_type_col_3.has_precision = 8
    data_type_col_3.has_scale = 0
    column_3.has_data_type = data_type_col_3
    yield pre_table
    destroy_entity(column_1)
    destroy_entity(column_2)
    destroy_entity(column_3)
    destroy_entity(min_reqs)
    destroy_entity(pre_table)


@fixture()
def prepared_table_2(prepared_core):
    min_reqs_2 = prepared_core.ConstraintGroup(f"min_req_2_{datetime.now()}")
    pre_table_2 = prepared_core.Table("internal_test_table_02")
    pre_table_2.has_min_reqs = min_reqs_2
    column_1 = prepared_core.Column("Column.Internal2.column_01")
    pre_table_2.has_columns.append(column_1)
    data_type_col_1 = prepared_core.Varchar()
    column_1.has_data_type = data_type_col_1
    column_2 = prepared_core.Column("Column.Internal2.column_02")
    pre_table_2.has_columns.append(column_2)
    data_type_col_2 = prepared_core.Varchar()
    column_2.has_data_type = data_type_col_2
    column_3 = prepared_core.Column("Column.Internal2.column_03")
    pre_table_2.has_columns.append(column_3)
    data_type_col_3 = prepared_core.Decimal()
    data_type_col_3.has_precision = 8
    data_type_col_3.has_scale = 0
    column_3.has_data_type = data_type_col_3
    yield pre_table_2
    destroy_entity(column_1)
    destroy_entity(column_2)
    destroy_entity(column_3)
    destroy_entity(min_reqs_2)
    destroy_entity(pre_table_2)


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
    range_const.set_left_boundary(40)
    yield range_const
    #destroy_entity(range_const)


@fixture()
def max_range_constraint_under_test(prepared_core, prepared_column):
    range_const_cls = prepared_core.RangeConstraint
    range_const = range_const_cls("gajskdufhakdh")
    range_const.is_constraining_column = prepared_column
    range_const.set_right_boundary(40)
    yield range_const
    # destroy_entity(range_const)


@fixture()
def actual_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("akjsdhflaishd")
    range_const.is_constraining_column = prepared_column
    range_const.set_right_boundary(40)
    range_const.set_left_boundary(10)
    yield range_const
    destroy_entity(range_const)



@fixture()
def regex_constraint_under_test(prepared_core, prepared_column):
    regex_const = prepared_core.RegexConstraint("rekajnisokdljf")
    regex_const.is_constraining_column = prepared_column
    regex_const.has_regex_format = "[a-z]oo"
    yield regex_const
    #destroy_entity(regex_const)

