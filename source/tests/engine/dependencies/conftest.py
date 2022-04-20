from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError

from LosydagGenerator import LosydagGenerator


def perform_dependency_test(prepared_core, test_case_title, dependency_under_test_maker):
    testing_iri = "http://corechuck.com/testing/dependency_namespace"
    test_ontology = get_ontology(testing_iri)
    test_ontology.imported_ontologies.append(prepared_core)

    dependency_under_test = dependency_under_test_maker(test_ontology)

    table_2_realization_def = prepared_core.RealizationDefinition(name=f"rd_{test_case_title}", namespace=test_ontology)
    table_2_realization_def.has_constraints = [dependency_under_test]
    try:
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
        table_2_realization_def.compliment_with_min_reqs()

        test_realization = prepared_core.RealizationCase(name=f"case_{test_case_title}", namespace=test_ontology)
        test_realization.contains_realizations = [table_2_realization_def]

        generator = LosydagGenerator(test_ontology)
        realized_case = generator.realize_fresh(f"case_{test_case_title}")
        return realized_case
    except OwlReadyInconsistentOntologyError:
        prepared_core.save(file=f"wrong_{test_case_title}.owl")
        raise