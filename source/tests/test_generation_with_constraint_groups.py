import pytest
from owlready2 import sync_reasoner_pellet

from utils.utils import NotUnifiedConstraintsException


def test_not_unified_constraint_group_throws_exception(
        prepared_core, max_range_constraint_under_test, min_range_constraint_under_test, prepared_table):

    constraint_group = prepared_core.ConstraintGroup("TestGroup.Generation_groups_01")
    constraint_group.has_constraints.append(max_range_constraint_under_test)
    constraint_group.has_constraints.append(min_range_constraint_under_test)
    constraint_group.is_a.append(prepared_core.OrGroup)

    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    constraint_group.is_a.append(prepared_core.RealizationDefinition)
    with pytest.raises(NotUnifiedConstraintsException, match=r"ERROR: Multiple constraints defined for column.*"):
        constraint_group.fulfill_constraints_renew()
