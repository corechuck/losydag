import datetime
import os

from _pytest.fixtures import fixture
from owlready2 import get_ontology, sync_reasoner_pellet, onto_path, OwlReadyInconsistentOntologyError

from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
from core_classes.SimpleExtensions import extend_core as extend_simple_types
from core_classes.Dependencies import extend_core as extend_dependencies
from core_classes.RealizationCase import extend_core as extend_realization_case
from core_classes.LogicalOperators import extend_core as extend_logical_operator
from core_classes.DataTypes import extend_core as extend_date_types
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
    extend_logical_operator(context)
    extend_date_types(context)

    try:
        sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)
    except OwlReadyInconsistentOntologyError:
        core.save(file=f"conftest_wrong_{datetime.now()}.owl")
        raise

    return core