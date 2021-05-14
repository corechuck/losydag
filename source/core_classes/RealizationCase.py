import rstr
import random
import datetime
import math
from owlready2 import Thing

def extend_core(_core):
    
    class RealizationCase(Thing):
        namespace = _core
        mapping_dict = None

        def __init__(self, name, namespace):
            super().__init__(name, namespace)
            self.__prepare_min_reqs_for_not_custom_constrained_but_reffered_tables()
            self.__prepare_table_name_to_singular_realization_def_dict()
            self.__setup_external_dependencies_with_single_realizations_definitions()
        
        def realize(self):
            for definition in self.contains_realizations:
                print(definition.fullfil_constraints())

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
                
        def __prepare_min_reqs_for_not_custom_constrained_but_reffered_tables(self):
            case_needed_tables = set()
            for definition in self.contains_realizations:
                case_needed_tables = case_needed_tables | definition.get_reffered_tables()

            for needed_table in case_needed_tables:
                is_needed_table_in_realization_case = \
                    any(map(
                        lambda rd: rd.constraint_table.name == needed_table.name, 
                        self.contains_realizations))
                if not is_needed_table_in_realization_case:
                    self.contains_realizations.append(needed_table.has_min_reqs)

            print(case_needed_tables)

            # TODO: Extend ontology with new Table and expect magic to happen
        