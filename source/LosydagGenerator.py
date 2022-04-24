from enum import Enum

from owlready2 import *
import utils.context as CONTEXT

# onto_path.append(f"{os.getcwd()}/resources/core/")
# onto_path.append(f"{os.getcwd()}/resources/development/")
from core_classes.ConstraintGroups import ConstraintGroup
from utils.utils import MergingException, ValueGenerationException


class GeneratorGenerationType(Enum):
    EXAMPLE = 1
    ALL_VARIATIONS = 2


class GeneratorCaseType(Enum):
    POSITIVE_CASES = "p_cases"
    NEGATIVE_CASES = "n_cases"


class LosydagGenerator:

    def __init__(self, loaded_onto):  # , realization_case_iri):

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

    # def generate_all_test_case_datasets_from_realization_case(self, group_iri):
    #     realization_case = self.onto.search_one(iri=f"*{group_iri}")
    #     realization_case._verbal = True  # for now
    #     return realization_case.realize_all_test_case_relevant_datasets()

    def _realize_cases(self, realized_datasets, _list_of_realization_cases, realization_type: GeneratorGenerationType):
        cases_index = 0
        for case in _list_of_realization_cases:
            cases_index += 1
            print(f"INFO: Case {cases_index} with meta: {case.meta}")
            try:
                realization_case = case.build_realization_case()
            except MergingException as e:
                print(f"Case {case.meta} resulted is empty choices")
                print(e.args[0])
                continue

            try:
                if realization_type == GeneratorGenerationType.ALL_VARIATIONS:
                    realized_datasets[realization_case.name] = \
                        realization_case.realize_all_test_case_relevant_datasets()
                elif realization_type == GeneratorGenerationType.EXAMPLE:
                    realized_datasets[realization_case.name] = realization_case.realize()

            except ValueGenerationException:
                print(f"ERROR: Could not generate value for case {case.meta}.")
                continue

    def _make_cases_and_realizations(
            self, loaded_group, breakdownType: GeneratorCaseType, realization_type: GeneratorGenerationType):
        realized_datasets = defaultdict(list)
        if breakdownType == GeneratorCaseType.POSITIVE_CASES:
            list_of_realization_cases = loaded_group.prepare_positive_cases()
        elif breakdownType == GeneratorCaseType.NEGATIVE_CASES:
            list_of_realization_cases = loaded_group.prepare_negative_cases()
        else:
            raise Exception(f"ERROR: chosen wrong breakdown type {breakdownType}")

        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        self._realize_cases(realized_datasets, list_of_realization_cases, realization_type)
        return realized_datasets

    def _pick_group_xor_group_iri(self, group_iri: str = "", group: ConstraintGroup = None):
        if not group_iri and not group:
            raise Exception("ERROR: Please provide either group_iri or loaded constraint_group")

        if group_iri and group:
            raise Exception("ERROR: Please provide only one: ('iri for a group' or 'already loaded group')")
        if group_iri:
            group = self.onto.search_one(iri=f"*{group_iri}")
        return group

    def generate_all_variations_for_all_discovered_positive_cases(
            self, group_iri: str = "", group: ConstraintGroup = None):
        """This method breaks down ConstraintGroup to all and precise POSITIVE cases of
        modelled custom constraints and generate all variants.
        This uses pairwise approach of defining positive cases."""

        group = self._pick_group_xor_group_iri(group_iri, group)
        realized_datasets = self._make_cases_and_realizations(
            group, GeneratorCaseType.POSITIVE_CASES, GeneratorGenerationType.ALL_VARIATIONS)
        return realized_datasets

    def generate_all_variations_for_all_discovered_negative_cases(
            self, group_iri: str = "", group: ConstraintGroup = None):
        """This method breaks down ConstraintGroup to all and precise NEGATIVE cases of
        custom constraints and generate all variants from that cases."""

        group = self._pick_group_xor_group_iri(group_iri, group)
        realized_datasets = self._make_cases_and_realizations(
            group, GeneratorCaseType.NEGATIVE_CASES, GeneratorGenerationType.ALL_VARIATIONS)
        return realized_datasets

    def generate_examples_of_discovered_positive_cases(
            self, group_iri: str = "", group: ConstraintGroup = None):
        """This method breaks down ConstraintGroup to all and precise POSITIVE cases of
        modelled custom constraints and generate examples from that cases.
        This uses pairwise approach of defining positive cases."""

        group = self._pick_group_xor_group_iri(group_iri, group)
        realized_datasets = self._make_cases_and_realizations(
            group, GeneratorCaseType.POSITIVE_CASES, GeneratorGenerationType.EXAMPLE)
        return realized_datasets

    def generate_examples_of_discovered_negative_cases(
            self, group_iri: str = "", group: ConstraintGroup = None):
        """This method breaks down ConstraintGroup to all and precise NEGATIVE cases of
        custom constraints and generate examples from that cases."""

        group = self._pick_group_xor_group_iri(group_iri, group)
        realized_datasets = self._make_cases_and_realizations(
            group, GeneratorCaseType.NEGATIVE_CASES, GeneratorGenerationType.EXAMPLE)
        return realized_datasets

    # def _breakdown_and_generate_data_for_all_positive_cases(self, constraint_group):
    #     constraint_group.convert_to_positive_cases()

    #
    # def negative_case_breakdown(self):
    #     """This method breaks down this Realization Case to all and precise NEGATIVE cases of
    #     modelled custom constraints. This produces realization case that has single column negative value."""
    #     pass
