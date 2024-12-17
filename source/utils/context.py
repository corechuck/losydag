import os

from owlready2 import get_ontology, onto_path

from utils.value_generator_supervisor import ValueGenerationSupervisor

onto_path.append(f"{os.getcwd()}/resources/core/")
# onto_path.append(f"{os.getcwd()}/resources/development/")


class ExtensionContext:
    core = None
    value_generation_supervisor: ValueGenerationSupervisor = None

    def __init__(self):
        schema_iri = "http://corechuck.com/modeling/core_check"
        self.core = get_ontology(schema_iri)
        # self.core.load(only_local=True)
        self.value_generation_supervisor = ValueGenerationSupervisor()


core_context: ExtensionContext = ExtensionContext()
