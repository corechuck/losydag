from enum import Enum

from utils.value_generator_supervisor import ValueGenerationSupervisor

_verbal = False


def _merge_groups_left_prio(group1, group2):
    """ Left prio means that if group1 and group2 has contraint for same column, 
    left-group1 will be taken and group2 not"""

    new_overwritten_list = group1.has_constraints.copy()

    for other_constraint in group2.has_constraints:
        if other_constraint.is_constraining_column.name \
                not in group1.names_of_constrained_columns():
            new_overwritten_list.append(other_constraint)
        
    return new_overwritten_list


def _supervise_constraint_generation(__internal_generation_function_with_leftovers, comment):
    not_ready_constraints = list()
    last_not_ready_constraints = -1
    loop_count = 0
    while True:
        not_ready_constraints = list()
        loop_count += 1
        if _verbal:
            print(f"DEBUG: Supervised generation for {comment}. Try number {loop_count}")
        __internal_generation_function_with_leftovers(not_ready_constraints)

        if last_not_ready_constraints == len(not_ready_constraints):
            raise Exception(f"ERROR: Could not resolve dependencies {not_ready_constraints}")
        
        if len(not_ready_constraints) == 0:
            break
        last_not_ready_constraints = len(not_ready_constraints)
        if _verbal: print(f"DEBUG: Supervised generation. Not resolved dependencies {not_ready_constraints}")

    return True


class ExtensionContext:
    core = None
    value_generation_supervisor: ValueGenerationSupervisor = None


class MultiplicationSupervisor():
    core = None

    def __init__(self, core):
        self.core = core

    def multiply_groups(self, left_group, right_group):
        left_list = list()
        if isinstance(left_group, self.core.OrGroup):
            left_list.extend(map(lambda e: [e], left_group.has_constraints))
        else:
            left_list.append(left_group.has_constraints)

        right_list = list()
        if isinstance(right_group, self.core.OrGroup):
            right_list.extend(map(lambda e: [e], right_group.has_constraints))
        else:
            right_list.append(right_group.has_constraints)

        multiplied_sets = list()
        for left_element_list in left_list:
            for right_element_list in right_list:
                new_list = list()
                new_list.extend(left_element_list)
                new_list.extend(right_element_list)
                multiplied_sets.append(new_list)

        return multiplied_sets