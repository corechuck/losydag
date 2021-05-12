import rstr
import random
from owlready2 import Thing
#from SyntheticExceptions import GenerationTypeException




def extend_core(_core):
    
    def _merge_groups_left_prio(group1, group2):
        """ Left prio means that if group1 and group2 has contraint for same column, 
        left-group1 will be taken and group2 not"""

        # temp_group = _core.ConstraintGroup(
        #     f"tconstgrp_{random.randint(100000,999999)}__based_{group1.name}")
        # temp_group.has_constraints 
        new_merged_list = group1.has_constraints.copy()

        for other_constraint in group2.has_constraints:
            if other_constraint.is_constraining_column.name \
                    not in group1.names_of_constrained_columns:
                new_merged_list.append(other_constraint)
            
        return new_merged_list

    def _supervise_constraint_generation(__internal_generation_function_with_leftovers):
        not_ready_constraints = list()
        last_not_ready_constraints = -1
        while True:
            not_ready_constraints = list()
            __internal_generation_function_with_leftovers(not_ready_constraints)

            if last_not_ready_constraints == len(not_ready_constraints):
                raise Exception(f"ERROR: Could not resolve dependencies {not_ready_constraints}")
            
            if len(not_ready_constraints) == 0:
                break
            last_not_ready_constraints = len(not_ready_constraints)
            print(f"INFO: Not resolved dependencies {not_ready_constraints}")


    class ConstraintGroup(Thing):
        namespace = _core

        # def __init__(self):
        #     pass
        
        def fullfil_constraints(self):
            list_of_constraints = self.has_constraints
            return f"{self.name} has {len(list_of_constraints)} constraints."

        def compliment_with(self, _other_constraint_group):
            self.has_constraints = _merge_groups_left_prio(self, _other_constraint_group)
            
        def merge_with_override(self, _other_constraint_group):
            self.has_constraints = _merge_groups_left_prio(_other_constraint_group, self)

        @property
        def names_of_constrained_columns(self):
            return [const.is_constraining_column.name for const in self.has_constraints]
        
        
    class RealizationDefinition(Thing):
        namespace = _core
        _return_dict = dict()

        # def __init__(self, name, namespace):
        #     self._return_dict = dict()
        #     super().__init__(name, namespace)

        # def __new__(self, name, namespace):
        #      super().__new__(Thing, name, namespace)

        # def __init__(self):
        #     self._return_dict = dict()

        @property
        def constraint_table(self):
            return self.is_constraining_tables[0]
        
        @property
        def has_realized_constraints(self):
            return len(self._return_dict) > 0
        
        def fullfil_constraints_renew(self):
            self._return_dict = dict()
            return self.fullfil_constraints()
        
        def fullfil_constraints(self):
            if self.has_realized_constraints:
                print("INFO: already generated:")
                return self._return_dict

            if not self._validate_one_table():
                print ("ERROR: Realization def should be defined for one table." 
                    "TODO: serious exception!")
            
            print("INFO: Generating new values:")
            self._return_dict = dict()
            for column in self.constraint_table.has_columns:
                self._return_dict[column.plain_name] = None

            self.compliment_with(self.constraint_table.has_min_reqs)
            print(f"INFO: Result based on: {self.name}")

            ## Heavy lifting
            _supervise_constraint_generation(self._try_generating_for_all_constraints)

            return self._return_dict

        def _try_generating_for_all_constraints(self, not_ready_accumulator):
            print(f"DEBUG: try X for {self.name}")
            for constraint in self.has_constraints:
                if not constraint.is_ready(self._return_dict):
                    not_ready_accumulator.append(constraint)
                    continue
                print(f"DEBUG: Generating {constraint.name}") 
                self._return_dict[constraint.is_constraining_column.plain_name] = (
                    constraint.generate(self._return_dict)
                )

        def _validate_one_table(self):
            if len(self.is_constraining_tables) == 1:
                return True

            is_same = True
            first_table_name = self.is_constraining_tables[0].name
            for suspect_table in self.is_constraining_tables:
                is_same = is_same and suspect_table.name == first_table_name

            return is_same



