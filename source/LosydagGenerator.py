from enum import Enum

from owlready2 import *

import utils.context as CONTEXT

onto_path.append(f"{os.getcwd()}/resources/core/")
onto_path.append(f"{os.getcwd()}/resources/development/")


class LosydagGenerator:

    def __init__(self, loaded_onto):  # , realization_case_iri):
        # self.onto = get_ontology(schema_iri)
        # self.onto.load(only_local=True)

        self.onto = loaded_onto
        # todo: check if if self.onto.imported_ontologies contains core
        self.core = CONTEXT.core_context.core

        # sync_reasoner_hermit(infer_property_values=True)
        try:
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        except OwlReadyInconsistentOntologyError:
            self.core.save(file="inconsistent_on_load.owl")

    def realize_fresh(self, realization_case_iri, is_silent=False):
        real_case = self.onto.search_one(iri=f"*{realization_case_iri}")
        real_case._verbal = not is_silent

        if not isinstance(real_case, self.core.RealizationCase):
            print(f"ERROR: {real_case} is not a RealizationCase, returning None.")
            return None

        print(f"INFO: Realizing: {real_case.name}")
        return real_case.realize_random_fresh()

    def generate_all_test_case_datasets_from_realization_case(self, group_iri):
        realization_case = self.onto.search_one(iri=f"*{group_iri}")
        realization_case._verbal = True  # for now
        return realization_case.realize_all_test_case_relevant_datasets()

    # def generate_all_negative_cases_from_realization_case(self, group_iri):
    #     realization_case = self.onto.search_one(iri=f"*{group_iri}")
    #     list_of_realization_cases = realization_case.convert_to_negative_cases()
    #     return self._realize_all_cases(list_of_realization_cases)

    @staticmethod
    def _realize_all_cases(_list_of_realization_cases):
        realized_datasets = defaultdict(list)
        for realization_case in _list_of_realization_cases:
            realized_datasets[realization_case.name] = realization_case.realize_all_test_case_relevant_datasets()
        return realized_datasets

    def generate_data_for_all_positive_cases_from_iri(self, group_iri):
        """This method breaks down ConstraintGroup to all and precise POSITIVE cases of
        modelled custom constraints. This uses pairwaise approach of defining positive cases."""

        generic_group = self.onto.search_one(iri=f"*{group_iri}")
        list_of_realization_cases = generic_group.convert_to_negative_cases()
        return self._realize_all_cases(list_of_realization_cases)

    def _breakdown_and_generate_data_for_all_positive_cases(self, constraint_group):
        constraint_group.convert_to_positive_cases()

    #
    # def negative_case_breakdown(self):
    #     """This method breaks down this Realization Case to all and precise NEGATIVE cases of
    #     modelled custom constraints. This produces realization case that has single column negative value."""
    #     pass
