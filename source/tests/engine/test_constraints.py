from datetime import datetime
import re

import pytest
from owlready2 import OwlReadyInconsistentOntologyError, destroy_entity

from utils.utils import DataTypeIssueException


def test_decimal_from_left_range_generated(prepared_core, prepared_table):
    range_constraint = prepared_core.RangeConstraint(
        name=f"decimal_left_range_const_{datetime.now()}",
        left_boundary=100,
        is_left_open=True,
        is_constraining_column=prepared_table.has_columns[2]
    )
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_1.owl")
        raise

    assert data, "Some data should be generated"
    assert float(data['internal_test_table_01'][0]['column_03']) > 100


def test_decimal_from_right_range_generated(prepared_core, prepared_table):
    range_constraint = prepared_core.RangeConstraint(
        name=f"decimal_right_range_const_{datetime.now()}",
        right_boundary=-3000,
        is_right_open=True,
        is_constraining_column=prepared_table.has_columns[2]
    )
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_2.owl")
        raise

    assert data, "Some data should be generated"
    assert float(data['internal_test_table_01'][0]['column_03']) < -3000


def test_decimal_from_actual_range_generated(prepared_core, prepared_table):

    range_constraint = prepared_core.RangeConstraint(
        name=f"decimal_actual_range_const_{datetime.now()}",
        left_boundary="100",
        is_left_open=True,
        right_boundary=102,
        is_right_open=True,
        is_constraining_column=prepared_table.has_columns[4]
    )
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_3.owl")
        raise

    assert data, "Some data should be generated"
    assert float(data['internal_test_table_01'][0]['column_05']) > 100.00
    assert float(data['internal_test_table_01'][0]['column_05']) < 102.00


def test_decimal_from_actual_range_with_scale_generated(prepared_core, prepared_table):

    range_constraint = prepared_core.RangeConstraint(
        name=f"decimal_actual_range_const_{datetime.now()}",
        left_boundary=100.00,
        is_left_open=True,
        right_boundary="102.23",
        is_right_open=True,
        is_constraining_column=prepared_table.has_columns[4]
    )
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_4.owl")
        raise

    assert data, "Some data should be generated"
    assert float(data['internal_test_table_01'][0]['column_05']) < 102.23
    assert float(data['internal_test_table_01'][0]['column_05']) > 100.00


def test_decimal_from_actual_range_with_overscale_left_exception(prepared_core, prepared_table):
    with pytest.raises(DataTypeIssueException):
        range_constraint = prepared_core.RangeConstraint(
            name=f"decimal_actual_range_const_{datetime.now()}",
            left_boundary=100.0052,
            is_constraining_column=prepared_table.has_columns[4]
        )
    # constraint_group = prepared_core.ConstraintGroup()
    # constraint_group.has_constraints.append(range_constraint)
    # with pytest.raises(DataTypeIssueException):
    #     try:
    #         case = constraint_group.build_realization_case()
    #         data = case.realize()
    #
    #     except OwlReadyInconsistentOntologyError:
    #         prepared_core.save(file=f"wrong_realization_case_5.owl")
    #         raise


def test_decimal_from_actual_range_with_overscale_right_exception(prepared_core, prepared_table):
    with pytest.raises(DataTypeIssueException):
        range_constraint = prepared_core.RangeConstraint(
            name=f"decimal_actual_range_const_{datetime.now()}",
            right_boundary="102.231",
            is_constraining_column=prepared_table.has_columns[4]
        )
    # constraint_group = prepared_core.ConstraintGroup()
    # constraint_group.has_constraints.append(range_constraint)
    # with pytest.raises(DataTypeIssueException):
    #     try:
    #         case = constraint_group.build_realization_case()
    #         case.realize()
    #
    #     except OwlReadyInconsistentOntologyError:
    #         prepared_core.save(file=f"wrong_realization_case_6.owl")
    #         raise


def test_decimal_with_scale_underscaled_from_actual_range_generated(prepared_core, prepared_table):

    range_constraint = prepared_core.RangeConstraint(
        name=f"decimal_actual_range_const_{datetime.now()}",
        left_boundary=100.10,
        is_left_open=True,
        right_boundary=102.20,
        is_right_open=True,
        is_constraining_column=prepared_table.has_columns[4]
    )
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_7.owl")
        raise

    assert data, "Some data should be generated"
    assert float(data['internal_test_table_01'][0]['column_05']) < 102.23
    assert float(data['internal_test_table_01'][0]['column_05']) > 100.00


def test_date_from_left_range_generated(prepared_core, prepared_table):

    range_constraint = prepared_core.RangeConstraint(
        name=f"date_left_range_const_{datetime.now()}",
        left_boundary="1988-06-30",
        is_left_open=True,
        is_constraining_column=prepared_table.has_columns[5]
    )
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_8.owl")
        raise

    assert data, "Some data should be generated"
    print(data['internal_test_table_01'][0]['column_06'])
    assert re.search(r'\d\d\d-\d\d-\d\d', data['internal_test_table_01'][0]['column_06'])
    # todo assert that is greater then 1988-06-30
    assert datetime.strptime(data['internal_test_table_01'][0]['column_06'], '%Y-%m-%d') > \
        datetime.strptime("1988-06-30", '%Y-%m-%d')


def test_date_from_range_generated(prepared_core, prepared_table):

    range_constraint = prepared_core.RangeConstraint(f"date_actual_range_const_{datetime.now()}")
    range_constraint.is_constraining_column = prepared_table.has_columns[5]
    range_constraint.set_left_boundary("1965-06-03", is_open=True)
    range_constraint.set_right_boundary("1988-06-30", is_open=True)

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_constraint)

    try:
        case = constraint_group.build_realization_case()
        data = case.realize()

    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_realization_case_9.owl")
        destroy_entity(range_constraint)
        raise
    assert data, "Some data should be generated"
    assert re.search(r"\d\d\d\d-\d\d-\d\d", data['internal_test_table_01'][0]['column_06'])
    assert datetime.strptime(data['internal_test_table_01'][0]['column_06'], '%Y-%m-%d') > \
        datetime.strptime("1965-06-03", '%Y-%m-%d')
    assert datetime.strptime(data['internal_test_table_01'][0]['column_06'], '%Y-%m-%d') < \
        datetime.strptime("1988-06-30", '%Y-%m-%d')


# def test_different formats