from owlready2 import *
from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
from core_classes.SimpleExtensions import extend_core as extend_simple_types
from core_classes.Dependencies import extend_core as extend_dependencies
from core_classes.RealizationCase import extend_core as extend_realization_case


onto_path.append(f"{os.getcwd()}/resources/core/")
onto_path.append(f"{os.getcwd()}/resources/development/")


class LosydagGenerator:

    def __init__(self, schema_iri):  # , realization_case_iri):
        self.onto = get_ontology(schema_iri)
        self.onto.load(only_local=True)

        self.core = self.onto.imported_ontologies[0]  # <- core classes are in wrong ontology
        extend_constraints(self.core)
        extend_dependencies(self.core)
        extend_constraint_groups(self.core)
        extend_simple_types(self.core)
        extend_realization_case(self.core)
        # sync_reasoner_hermit(infer_property_values=True)
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

    def realize_fresh(self, realization_case_iri, is_silent=False):
        real_case = self.onto.search_one(iri=f"*{realization_case_iri}")
        real_case._verbal = not is_silent

        if not isinstance(real_case, self.core.RealizationCase):
            print(f"ERROR: {real_case} is not a RealizationCase, returning None.")
            return None

        print(f"INFO: Realizing: {real_case.name}")
        return real_case.realize_anew()
