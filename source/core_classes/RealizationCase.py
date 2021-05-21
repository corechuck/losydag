import rstr
import random
import datetime
import math
from owlready2 import Thing, sync_reasoner_pellet, sync_reasoner, sync_reasoner_hermit
from ..utils.utils import _supervise_constraint_generation

def extend_core(_core):
    
    class RealizationCase(Thing):
        namespace = _core
        mapping_dict = None
        _verbal = True

        def __init__(self, name, namespace):
            super().__init__(name, namespace)
            self.__prepare_min_reqs_for_not_custom_constrained_but_reffered_tables(namespace)
            sync_reasoner_hermit(infer_property_values=True)
            # sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)

            self.__prepare_table_name_to_singular_realization_def_dict()
            self.__setup_external_dependencies_with_single_realizations_definitions()
        
        def realize(self):
            _supervise_constraint_generation(self._realize, f"{self.name}")
            return self._get_agregated_results()
        
        def realize_anew(self):
            [rd.clear_results() for rd in self.contains_realizations]
            _supervise_constraint_generation(self._realize, f"{self.name}")
            return self._get_agregated_results()

        def positive_case_breakdown(self):
            """This method breaks down this Realization Case to all and precise POSITIVE cases of
            modelled custom constraints. This uses pairwaise approach of defining positive cases."""
            pass

        def negative_case_breakdown(self):
            """This method breaks down this Realization Case to all and precise NEGATIVE cases of
            modelled custom constraints. This produces realization case that has single column negative value."""
            pass

        def _realize(self, not_ready_acc):
            for definition in self.contains_realizations:
                if self._verbal: print(f"INFO: Evaluating {definition.name}:")
                if definition.has_realized_constraints:
                    if self._verbal: print(f"INFO: Already realized : {definition.name}")
                    continue

                if definition.is_ready:
                    if self._verbal: print(f"INFO: Realizing : {definition.name}")
                    definition.fullfil_constraints()
                else:
                    if self._verbal: print(f"INFO: Not ready : {definition.name}")
                    not_ready_acc.append(definition)

        def _get_agregated_results(self):
            aggregate = dict()
            for definition in self.contains_realizations:
                if not definition.has_realized_constraints:
                    print(f"WARN: cannot agregate not realized constraint {definition.name}")
                    continue
                if not definition.constraint_table.name in aggregate.keys():
                    aggregate[definition.constraint_table.name] = list()

                aggregate[definition.constraint_table.name].append(definition._return_dict)
            
            return aggregate

                

        def __setup_external_dependencies_with_single_realizations_definitions(self):
            for definition in self.contains_realizations:
                if definition.is_having_external_dependencies:
                    definition.prepare_external_dependencies_with_single_realization_definition(
                        self.mapping_dict)


        def __prepare_table_name_to_singular_realization_def_dict(self):
            if self.mapping_dict is not None:
                return self.mapping_dict

            self.mapping_dict = dict()
            for definition in self.contains_realizations:
                if definition.constraint_table.name not in self.mapping_dict:
                    self.mapping_dict[definition.constraint_table.name] = definition
                    continue
                if definition.constraint_table.name in self.mapping_dict:
                    self.mapping_dict[definition.constraint_table.name] = None

            self.mapping_dict = dict(filter(lambda el: el[1], self.mapping_dict.items()))
                
        def __prepare_min_reqs_for_not_custom_constrained_but_reffered_tables(self, namespace):
            case_needed_tables = set()
            for definition in self.contains_realizations:
                case_needed_tables = case_needed_tables | definition.get_reffered_tables()

            for needed_table in case_needed_tables:
                is_needed_table_in_realization_case = \
                    any(map(
                        lambda rd: rd.constraint_table.name == needed_table.name, 
                        self.contains_realizations))
                if not is_needed_table_in_realization_case:
                    # TODO: this part should not be here but somewhere deeper
                    new_def = _core.RealizationDefinition(
                        f"{needed_table.has_min_reqs.name}_temp_{random.randint(10000,99999)}",
                        namespace)
                    new_def.compliment_with(needed_table.has_min_reqs)
                    self.contains_realizations.append(new_def)

            print(f"INFO: Referenced tables: {case_needed_tables}")

            # TODO: Extend ontology with new Table and expect magic to happen
        