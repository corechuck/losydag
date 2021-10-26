import pytest
from owlready2 import sync_reasoner_pellet


def test_not_unified_constraint_group_throws_exception(
        prepared_core, list_constraint_under_test, min_range_constraint_under_test):
    constraint_group = prepared_core.ConstraintGroup("TestGroup.Generation_groups_01")
    constraint_group.has_constraints.append(list_constraint_under_test)
    constraint_group.has_constraints.append(min_range_constraint_under_test)
    constraint_group.is_a.append(prepared_core.OrGroup)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.is_a.append(prepared_core.RealizationDefinition)
    # constraint_group.compliment_with_min_reqs()
    generated_dataset = constraint_group.fulfill_constraints_renew()
    assert generated_dataset is not None

    generated_value_under_test = generated_dataset['internal_test_table_01']["Column.Internal1.column_01"]
    assert (generated_value_under_test.isnumeric() and int(generated_dataset) > 40) or \
           generated_value_under_test in ['foo', 'moo', '1', 'baa', '-3.14', 'xD', '54']

