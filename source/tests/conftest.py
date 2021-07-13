import os
import pytest

from owlready2 import get_ontology, sync_reasoner_pellet, onto_path
from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
from core_classes.SimpleExtensions import extend_core as extend_simple_types
from core_classes.Dependencies import extend_core as extend_dependencies
from core_classes.RealizationCase import extend_core as extend_realization_case


@pytest.fixture(scope="session")
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