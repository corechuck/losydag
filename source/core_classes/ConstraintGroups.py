import rstr
import random
from owlready2 import Thing
#from SyntheticExceptions import GenerationTypeException


def extend_core(_core):

    class ConstraintGroup(Thing):
        namespace = _core

        # def __init__(self):
        #     pass
        
        def fullfil_constraints(self):
            list_of_constraints = self.has_constraints
            return f"{self.name} has {len(list_of_constraints)} constraints."


    class RealizationDefinition(Thing):
        namespace = _core
        
        def fullfil_constraints(self):
            if not self._validate_one_table():
                print ("ERROR: Realization def should be defined for one table. TODO: serious exception!")
            return_dict = dict()
            for column in self.constraint_table.has_columns:
                return_dict[column.name] = None

            for constraint in self.has_constraints:
                if isinstance(constraint, _core.OrGroup) or not constraint.is_ready():
                    continue
                return_dict[constraint.is_constraining_column.name] = constraint.generate()

            return return_dict

        def _validate_one_table(self):
            is_same = True
            first_table_name = self.is_constraining_tables[0].name
            # print("INFO: Amount of tables constraint : "+str(len(self.is_constraining_tables)))
            for suspect_table in self.is_constraining_tables:
                is_same = is_same and suspect_table.name == first_table_name

            return is_same

        @property
        def constraint_table(self):
            return self.is_constraining_tables[0]