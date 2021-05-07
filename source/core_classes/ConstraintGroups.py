import rstr
import random
from owlready2 import Thing
#from SyntheticExceptions import GenerationTypeException




def extend_core(_core):
    
    def _merge_groups_left_prio(group1, group2):
        """ Left prio means that if group1 and group2 has contraint for same column, 
        left-group1 will be taken and group2 not"""

        temp_group = _core.ConstraintGroup(
            f"tconstgrp_{random.randint(100000,999999)}__based_{group1.name}")
        temp_group.has_constraints = group1.has_constraints.copy()

        for other_constraint in group2.has_constraints:
            if other_constraint.is_constraining_column.name \
                    not in group1.names_of_constrained_columns:
                temp_group.has_constraints.append(other_constraint)
            
        return temp_group


    class ConstraintGroup(Thing):
        namespace = _core

        # def __init__(self):
        #     pass
        
        def fullfil_constraints(self):
            list_of_constraints = self.has_constraints
            return f"{self.plain_name} has {len(list_of_constraints)} constraints."

        def compliment_with(self, _other_constraint_group):
            return _merge_groups_left_prio(self, _other_constraint_group)
        
        def merge_with_override(self, _other_constraint_group):
            return _merge_groups_left_prio(_other_constraint_group, self)

        @property
        def names_of_constrained_columns(self):
            return [const.is_constraining_column.name for const in self.has_constraints]
        
        
    class RealizationDefinition(Thing):
        namespace = _core
        
        def fullfil_constraints(self):
            if not self._validate_one_table():
                print ("ERROR: Realization def should be defined for one table." 
                    "TODO: serious exception!")
            return_dict = dict()
            for column in self.constraint_table.has_columns:
                return_dict[column.plain_name] = None

            temp_merged_definition = self.compliment_with(self.constraint_table.has_min_reqs)
            print(f"INFO: Result based on: {temp_merged_definition.name}")

            for constraint in temp_merged_definition.has_constraints:
                if not constraint.is_ready():
                    continue
                return_dict[constraint.is_constraining_column.plain_name] = constraint.generate()

            return return_dict


        def _validate_one_table(self):
            if len(self.is_constraining_tables) == 1:
                return True

            is_same = True
            first_table_name = self.is_constraining_tables[0].name
            for suspect_table in self.is_constraining_tables:
                is_same = is_same and suspect_table.name == first_table_name

            return is_same

        @property
        def constraint_table(self):
            return self.is_constraining_tables[0]



