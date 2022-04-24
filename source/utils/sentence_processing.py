
class MultiplicationSupervisor:
    """
    That multiply list of lists to become times another list of lists: so
    A = [[a,b],[c,d]]
    B = [[w,x],[y,z]]
    but lists are just extended in the end so not really multiplyed like matrixes

    A x B = [[a,b],[c,d]] * [[w,x],[y,z]] = [[a,b]*[w,x], [c,d]*[w,x], [a,b]*[y,z], [c,d]*[y,z]] =
          = [[a,b,w,x], [c,d,w,x], [a,b,y,z], [c,d,y,z]]

    but also is custom made to strip core_classes and leave just lists
    (which probably should be somewhere else if that REALLY should be a module, but 'meh' for now)
    """
    core = None

    def __init__(self, core):
        self.core = core

    def prepare_constraints_for_multiplication(self, group):
        if isinstance(group, self.core.OrGroup):
            return list(map(lambda e: [e], group.has_constraints))
        else:
            return [group.has_constraints]

    def multiply(self, left_term_list, right_term_list):
        multiplied_sets = list()
        for left_element_list in left_term_list:
            for right_element_list in right_term_list:
                new_list = list()
                new_list.extend(left_element_list)
                new_list.extend(right_element_list)
                multiplied_sets.append(new_list)

        return multiplied_sets

    def multiply_list_by_group(self, left_term_list, right_group):
        right_term_list = self.prepare_constraints_for_multiplication(right_group)
        return self.multiply(left_term_list, right_term_list)

    def multiply_groups(self, left_group, right_group):
        left_term_list = self.prepare_constraints_for_multiplication(left_group)
        return self.multiply_list_by_group(left_term_list, right_group)

    def breakdown_of_or_branches_to_possible_constraint_sentences(self):
        list_of_constraint_sentences = self.prepare_constraints_for_multiplication(self)
        for child_constraint_group in self.contains_constraint_groups:
            list_of_constraint_sentences = \
                self.multiply_list_by_group(list_of_constraint_sentences, child_constraint_group)

        return list_of_constraint_sentences