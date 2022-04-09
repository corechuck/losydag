
from datetime import datetime
from _pytest.fixtures import fixture
from owlready2 import destroy_entity

_LOG_LEVEL = 1


INTERNAL_TEST_TABLE_1 = "internal_test_table_01"
TEST_TBL = INTERNAL_TEST_TABLE_1

@fixture()
def prepared_table(prepared_core):
    pre_table = prepared_core.Table(INTERNAL_TEST_TABLE_1)
    column_1 = prepared_core.Column("Column.Internal1.column_01")
    column_2 = prepared_core.Column("Column.Internal1.column_02")
    column_3 = prepared_core.Column("Column.Internal1.column_03")
    column_4 = prepared_core.Column("Column.Internal1.column_04")
    column_5 = prepared_core.Column("Column.Internal1.column_05")
    column_6 = prepared_core.Column("Column.Internal1.column_06")
    column_7 = prepared_core.Column("Column.Internal1.column_07")
    column_8 = prepared_core.Column("Column.Internal1.column_08")

    pre_table.has_columns.append(column_1)
    pre_table.has_columns.append(column_2)
    pre_table.has_columns.append(column_3)
    pre_table.has_columns.append(column_4)
    pre_table.has_columns.append(column_5)
    pre_table.has_columns.append(column_6)
    pre_table.has_columns.append(column_7)
    pre_table.has_columns.append(column_8)

    varchar_type = prepared_core.Varchar()
    data_type_date = prepared_core.Date()
    data_type_datetime = prepared_core.Date(has_date_format="%Y-%m-%d %H:%M:%S")
    data_type_decimal_8_0 = prepared_core.Decimal()
    data_type_decimal_8_0.has_precision = 8
    data_type_decimal_8_0.has_scale = 0
    data_type_decimal_8_2 = prepared_core.Decimal()
    data_type_decimal_8_2.has_precision = 8
    data_type_decimal_8_2.has_scale = 2

    column_1.has_data_type = data_type_decimal_8_0
    column_2.has_data_type = varchar_type
    column_3.has_data_type = data_type_decimal_8_0
    column_4.has_data_type = data_type_decimal_8_0
    column_5.has_data_type = data_type_decimal_8_2
    column_6.has_data_type = data_type_date
    column_7.has_data_type = varchar_type
    column_8.has_data_type = data_type_datetime

    yield pre_table
    destroy_entity(column_1)
    destroy_entity(column_2)
    destroy_entity(column_3)
    destroy_entity(column_4)
    destroy_entity(column_5)
    destroy_entity(column_6)
    destroy_entity(column_7)
    destroy_entity(column_8)
    destroy_entity(data_type_date)
    destroy_entity(data_type_datetime)
    destroy_entity(pre_table)


@fixture()
def min_req_list_constraint(prepared_core, prepared_table):
    list_const = prepared_core.ListConstraint(f"list_req_{datetime.now()}")
    list_const.is_constraining_column = prepared_table.has_columns[1]
    list_const.has_picks = ['col1_pick1', 'col1_pick2', 'col1_pick3']
    yield list_const
    # destroy_entity(list_const)


@fixture()
def min_req_range_constraint(prepared_core, prepared_table):
    range_const = prepared_core.RangeConstraint("tbl_01_min_req_decimal_lft_rng")
    range_const.is_constraining_column = prepared_table.has_columns[3]
    range_const.set_left_boundary(40)
    yield range_const
    destroy_entity(range_const)


@fixture()
def min_req_range_for_date_constraint(prepared_core, prepared_table):
    range_const = prepared_core.RangeConstraint("tbl_01_min_req_date_range")
    range_const.is_constraining_column = prepared_table.has_columns[5]
    range_const.set_left_boundary("1999-01-01")
    range_const.set_right_boundary("2022-12-31")
    yield range_const
    destroy_entity(range_const)


@fixture()
def min_req_for_prepared_table(
        prepared_core, prepared_table,
        min_req_list_constraint, min_req_range_constraint, min_req_range_for_date_constraint):
    min_reqs = prepared_core.ConstraintGroup(f"min_req_{datetime.now()}")
    min_reqs.has_constraints = [
        min_req_list_constraint, min_req_range_constraint, min_req_range_for_date_constraint
    ]
    prepared_table.has_min_reqs = min_reqs
    yield
    destroy_entity(min_reqs)


@fixture()
def prepared_table_2(prepared_core):
    min_reqs_2 = prepared_core.ConstraintGroup(f"min_req_2_{datetime.now()}")

    pre_table_2 = prepared_core.Table("internal_test_table_02")
    pre_table_2.has_min_reqs = min_reqs_2

    column_1 = prepared_core.Column("Column.Internal2.column_01")
    column_2 = prepared_core.Column("Column.Internal2.column_02")
    column_3 = prepared_core.Column("Column.Internal2.column_03")
    column_4 = prepared_core.Column("Column.Internal2.column_04")
    column_5 = prepared_core.Column("Column.Internal2.column_05")
    pre_table_2.has_columns.append(column_1)
    pre_table_2.has_columns.append(column_2)
    pre_table_2.has_columns.append(column_3)
    pre_table_2.has_columns.append(column_4)
    pre_table_2.has_columns.append(column_5)
    data_type_varchar = prepared_core.Varchar()
    data_type_decimal_8_0 = prepared_core.Decimal()
    data_type_decimal_8_0.has_precision = 8
    data_type_decimal_8_0.has_scale = 0
    data_type_date = prepared_core.Date()
    data_type_datetime = prepared_core.Date(has_date_format="%Y-%m-%d %H:%M:%S")
    column_1.has_data_type = data_type_varchar
    column_2.has_data_type = data_type_varchar
    column_3.has_data_type = data_type_decimal_8_0
    column_4.has_data_type = data_type_date
    column_5.has_data_type = data_type_datetime
    yield pre_table_2
    destroy_entity(column_1)
    destroy_entity(column_2)
    destroy_entity(column_3)
    destroy_entity(column_4)
    destroy_entity(column_5)
    destroy_entity(data_type_date)
    destroy_entity(data_type_datetime)
    destroy_entity(min_reqs_2)
    destroy_entity(pre_table_2)


@fixture()
def prepared_column(prepared_core, prepared_table):
    yield prepared_table.has_columns[0]


@fixture()
def list_constraint_under_test(prepared_core, prepared_table):
    list_const = prepared_core.ListConstraint(f"list_req_l")
    list_const.is_constraining_column = prepared_table.has_columns[1]
    list_const.has_picks = ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']
    yield list_const
    destroy_entity(list_const)


@fixture()
def min_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint(f"min_range_mm")
    range_const.is_constraining_column = prepared_column
    range_const.set_left_boundary(40)
    yield range_const
    destroy_entity(range_const)


@fixture()
def max_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint(f"max_range_xx")
    range_const.is_constraining_column = prepared_column
    range_const.set_right_boundary(40)
    yield range_const
    destroy_entity(range_const)


@fixture()
def actual_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint(f"actual_range_r")
    range_const.is_constraining_column = prepared_column
    range_const.set_right_boundary(40)
    range_const.set_left_boundary(10)
    yield range_const
    destroy_entity(range_const)



@fixture()
def regex_constraint_under_test(prepared_core, prepared_column):
    regex_const = prepared_core.RegexConstraint(f"rgx_cnstr")
    regex_const.is_constraining_column = prepared_column
    regex_const.has_regex_format = "[a-z]oo"
    yield regex_const
    destroy_entity(regex_const)

