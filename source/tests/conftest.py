import os

from _pytest.fixtures import fixture
from owlready2 import onto_path

import utils.context


@fixture(scope="session")
def prepared_core():

    from core_classes import DataTypes
    from core_classes import SimpleExtensions
    from core_classes import Constraints
    from core_classes import Dependencies
    from core_classes import ConstraintGroups
    from core_classes import LogicalOperators
    from core_classes import RealizationCase

    onto_path.append(f"{os.getcwd()}/resources/development/")
    utils.context.core_context.core.load()

    return utils.context.core_context.core
