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
                

        