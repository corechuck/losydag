import pytest
from _pytest.fixtures import fixture
from owlready2 import sync_reasoner_pellet, destroy_entity
from datetime import datetime


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
    range_const = prepared_core.RangeConstraint("gajskdufhakdh")
    range_const.is_constraining_column = prepared_column
    range_const.has_min_range = 40
    return range_const


@fixture()
def max_range_constraint_under_test(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("gajskdufhakdh")
    range_const.is_constraining_column = prepared_column
    range_const.has_max_range = 40
    return range_const


@fixture()
def regex_constraint_under_test(prepared_core, prepared_column):
    regex_const = prepared_core.RegexConstraint("rekajnisokdljf")
    regex_const.is_constraining_column = prepared_column
    regex_const.has_regex_format = "[a-z]oo"
    return regex_const


def test_not_unified_constraint_group_throws_exception(
        prepared_core, list_constraint_under_test, min_range_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup("TestGroup.Internal_01")
    constraint_group.has_constraints.append(list_constraint_under_test)
    constraint_group.has_constraints.append(min_range_constraint_under_test)
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.is_a.append(prepared_core.RealizationDefinition)
    constraint_group.compliment_with_min_reqs()
    with pytest.raises(Exception, match=r"ERROR: Multiple constraints defined for column.*"):
        obj = constraint_group.fulfill_constraints_renew()


def test_min_range_merge_with_list(
        prepared_core, list_constraint_under_test, min_range_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(min_range_constraint_under_test)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group
    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] == '54'


def test_list_merge_with_range_max(
        prepared_core, list_constraint_under_test, max_range_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(list_constraint_under_test)
    constraint_group.has_constraints.append(max_range_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] == '1'


def test_regex_merge_with_list(prepared_core, list_constraint_under_test, regex_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(list_constraint_under_test)
    constraint_group.has_constraints.append(regex_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in ['moo', 'foo']


def test_list_merge_with_regex(prepared_core, list_constraint_under_test, regex_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(regex_constraint_under_test)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in ['moo', 'foo']


def test_regex_with_range(prepared_core, min_range_constraint_under_test, regex_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(regex_constraint_under_test)
    constraint_group.has_constraints.append(min_range_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    with pytest.raises(Exception, match=r"ERROR: Not implemented"):
        constraint_group.unify_constraints()


def test_list_merged_with_not_in_list(prepared_core, prepared_column, list_constraint_under_test):
    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_picks = ['foo', 'moo', '1', 'baa', '54']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(list_constraint_under_test)
    constraint_group.has_constraints.append(generic_constraint)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in ['-3.14', 'xD']


def test_not_in_list_merged_with_list(prepared_core, prepared_column, list_constraint_under_test):
    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_picks = ['foo', '-3.14', 'xD', 'baa', '54']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(generic_constraint)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in ['moo', '1']


def test_list_merged_with_not_match(prepared_core, prepared_column, list_constraint_under_test):
    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_matching_regex = ['.oo', '.aa', '-.*']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(list_constraint_under_test)
    constraint_group.has_constraints.append(generic_constraint)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in ['1', 'xD', '54']


def test_list_merged_with_multiple_not_matches(prepared_core, prepared_column, list_constraint_under_test):
    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_matching_regex = ['^x.$', '^.$', '^..$', '^-.*$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(generic_constraint)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in ['foo', 'moo', 'baa']


def test_not_in_list_merged_with_regex(prepared_core, prepared_column, regex_constraint_under_test):
    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_picks = \
        ["aoo", "boo", "coo", "doo", "eoo", "foo", "goo", "hoo", "ioo", "joo", "koo", "loo", "moo", "noo"]

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(generic_constraint)
    constraint_group.has_constraints.append(regex_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in \
               ["ooo", "poo", "qoo", "roo", "soo", "too", "uoo", "voo", "woo", "xoo", "yoo", "zoo"]


def test_regex_merged_with_multiple_not_matches(prepared_core, prepared_column, regex_constraint_under_test):
    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_matching_regex = ['^[a-f]oo$', '^[t-z]oo$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(regex_constraint_under_test)
    constraint_group.has_constraints.append(generic_constraint)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in \
               ["goo", "hoo", "ioo", "joo", "koo", "loo", "moo", "noo", "ooo", "poo", "qoo", "roo", "soo"]


def test_range_merged_with_not_in_list(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("jhlkndsd")
    range_const.is_constraining_column = prepared_column
    range_const.has_min_range = 40
    range_const.has_max_range = 60

    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_picks = \
        ["40", "41", "42", "43", "44", "45", "46", "47", "58", "59", "60"]

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_const)
    constraint_group.has_constraints.append(generic_constraint)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in \
               ["48", "49", "50", "51", "52", "53", "54", "55", "56", "57"]


def test_range_merged_with_not_match(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("jhlkndsd")
    range_const.is_constraining_column = prepared_column
    range_const.has_min_range = 40
    range_const.has_max_range = 60

    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_matching_regex = ['^4.$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_const)
    constraint_group.has_constraints.append(generic_constraint)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in \
               ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60"]


def test_range_merged_with_multiple_not_matches(prepared_core, prepared_column):
    range_const = prepared_core.RangeConstraint("jhlkndsd")
    range_const.is_constraining_column = prepared_column
    range_const.has_min_range = 40
    range_const.has_max_range = 60

    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_matching_regex = ['^4.$', '^.[5-9]$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_const)
    constraint_group.has_constraints.append(generic_constraint)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in \
               ["50", "51", "52", "53", "54", "60"]


def test_constraint_and_dependency_for_same_column(prepared_core, prepared_column, list_constraint_under_test):
    # raise exception cannot have constraint and dependency for same column
    dependency_const = prepared_core.ValueDependency("badfgqasx")
    dependency_const.is_constraining_column = prepared_column
    dependency_const.has_format_definition = "copy_{column_1}"

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(dependency_const)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    with pytest.raises(Exception, match=r"^ERROR: Cannot merge Value Dependency.*"):
        constraint_group.unify_constraints()


def test_unification_of_constraint_works_with_dependencies(prepared_core, prepared_column, list_constraint_under_test):
    column_2 = next(col for col in prepared_column.is_part_of_table.has_columns if "column_02" in col.name)
    list_constraint_under_test.is_constraining_column = column_2

    range_const = prepared_core.RangeConstraint("jhlkndsd")
    range_const.is_constraining_column = prepared_column
    range_const.has_min_range = 40
    range_const.has_max_range = 60

    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_column
    generic_constraint.not_matching_regex = ['^4.$', '^.[5-9]$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_const)
    constraint_group.has_constraints.append(generic_constraint)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.convert_to_realization_definition()
    realization_definition = constraint_group

    for number in range(100):
        generated_result = realization_definition.fulfill_constraints_renew()
        assert generated_result['column_01'] in \
               ["50", "51", "52", "53", "54", "60"]
        assert generated_result['column_02'] in \
               ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']


def test_two_dependencies(prepared_core, prepared_column):
    dependency_const = prepared_core.ValueDependency("badfgqasx")
    dependency_const.is_constraining_column = prepared_column
    dependency_const.has_format_definition = "copy_{column_02}"

    dependency_const_2 = prepared_core.ValueDependency("aksdjfhw49eydh")
    dependency_const_2.is_constraining_column = prepared_column
    dependency_const_2.has_format_definition = "copy_{column_02}"

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(dependency_const)
    constraint_group.has_constraints.append(dependency_const_2)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    with pytest.raises(Exception, match=r"^ERROR: Cannot merge Value Dependency.*"):
        constraint_group.unify_constraints()


def test_constraints_for_multiple_tables_in_constraints_group_bad_convertion_to_single_reazlization_definition(
        prepared_core, prepared_table, prepared_table_2, list_constraint_under_test):
    list_constraint_under_test.is_constraining_column = prepared_table_2.has_columns[0]

    range_const = prepared_core.RangeConstraint("jhlkndsd")
    range_const.is_constraining_column = prepared_table.has_columns[0]
    range_const.has_min_range = 40
    range_const.has_max_range = 60

    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_table.has_columns[0]
    generic_constraint.not_matching_regex = ['^4.$', '^.[5-9]$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_const)
    constraint_group.has_constraints.append(generic_constraint)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    with pytest.raises(Exception, match=r"^ERROR: .*constraints more then one table. Should only one."):
        constraint_group.convert_to_realization_definition()


def test_constraints_for_multiple_tables_in_constraints_group_turns_into_realization_case(
        prepared_core, prepared_table, prepared_table_2, list_constraint_under_test):
    """ or multiple_realization_definitions_"""
    list_constraint_under_test.is_constraining_column = prepared_table_2.has_columns[0]

    range_const = prepared_core.RangeConstraint("jhlkndsd")
    range_const.is_constraining_column = prepared_table.has_columns[0]
    range_const.has_min_range = 40
    range_const.has_max_range = 60

    generic_constraint = prepared_core.Constraint()
    generic_constraint.is_constraining_column = prepared_table.has_columns[0]
    generic_constraint.not_matching_regex = ['^4.$', '^.[5-9]$']

    constraint_group = prepared_core.ConstraintGroup()
    constraint_group.has_constraints.append(range_const)
    constraint_group.has_constraints.append(generic_constraint)
    constraint_group.has_constraints.append(list_constraint_under_test)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    case = constraint_group.build_realization_case()
    generated_result = case.realize()

    # expected result example
    # generated_result = {
    #       'internal_test_table_01': [{'column_01': '60', 'column_02': None}],
    #       'internal_test_table_02': [{'column_02': '-3.14'}]
    #    }

    assert len(generated_result.keys()) == 2, "Generated results should be for two different tables."
    assert generated_result['internal_test_table_01'][0]['column_01'] in \
               ["50", "51", "52", "53", "54", "60"]
    assert generated_result['internal_test_table_01'][0]['column_02'] is None

    assert "column_01" in generated_result['internal_test_table_02'][0]
    assert generated_result['internal_test_table_02'][0]['column_01'] in ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']



