from datetime import datetime

from owlready2 import Thing
from utils.context import ExtensionContext
import utils.context


if not utils.context.core_context\
        or not utils.context.core_context.core\
        or not utils.context.core_context.value_generation_supervisor:
    raise Exception("Cannot import Operators without initialized utils.context.core_context")

_core = utils.context.core_context.core
ordinal = lambda n: "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


class AndGroup(Thing):
    namespace = _core

    def prepare_positive_cases(self):
        positive_cases = list()
        self.meta = f"No change {self.name}"
        if len(self.contains_constraint_groups) == 0:
            positive_cases.append(self)
        else:
            for child_group in self.contains_constraint_groups:
                child_group_list_of_positive_cases = child_group.prepare_positive_cases()
                for child_case in child_group_list_of_positive_cases:
                    positive_cases.append(self.merge_my_copy_with_group(child_case))
        return positive_cases

    def prepare_negative_cases(self):
        negative_cases = list()
        list_of_elements_for_breakdown = self.has_constraints.copy()
        list_of_elements_for_breakdown.extend(self.contains_constraint_groups)
        for constraint_or_group_to_invert in list_of_elements_for_breakdown:
            groups_for_processing = list()
            negative_case_under_process = _core.ConstraintGroup(
                f"{ordinal(len(negative_cases)+1)}_negative_case_of_{self.name}")
            negative_case_under_process.meta = \
                f"Negating {constraint_or_group_to_invert.name} in group {self.name}"
            negative_cases_for_chosen_constraint = [negative_case_under_process]
            for constraint in self.has_constraints:
                if constraint_or_group_to_invert == constraint:
                    inverted_constraint_to_group = self.inverter.invert(constraint)
                    # negative_case_under_process.meta = \
                    #     f"Inverted constraint {constraint.name}"
                    if len(inverted_constraint_to_group.has_constraints) == 1:
                        negative_case_under_process.has_constraints.append(
                            inverted_constraint_to_group.has_constraints[0])
                    else:
                        negative_cases_for_chosen_constraint = self.multiply_list_of_cases_times_group(
                            negative_cases_for_chosen_constraint, inverted_constraint_to_group)
                else:  # not invert constraint
                    for case in negative_cases_for_chosen_constraint:
                        case.has_constraints.append(constraint)

            for const_group in self.contains_constraint_groups:
                if constraint_or_group_to_invert == const_group:
                    child_group_list_of_negative_cases = const_group.prepare_negative_cases()
                    with_child_negative_cases = list()
                    for specific_negative_case in negative_cases_for_chosen_constraint:
                        for child_negative_case in child_group_list_of_negative_cases:
                            with_child_negative_cases.append(
                                specific_negative_case.merge_my_copy_with_group(child_negative_case)
                            )
                    negative_cases_for_chosen_constraint = with_child_negative_cases
                    continue
                # just add groups
                # TODO: Test with (c1 ^ c2 ^ (c3 v c4 v (c5 ^ c6)) ^ (c7 ^ c8)) when c2 is actual range

                # c1 ^ (c2 v c3) == c1^c2 v c1^c3
                # size, color, producer, fabric, creation date, layers amount, amount, category, descr as format

                my_negative_cases_times_plain_child_group = list()
                child_positive_cases = const_group.prepare_positive_cases()
                for child_positive_case in child_positive_cases:
                    my_negative_cases_times_plain_child_group.extend(
                        self.multiply_list_of_cases_times_group(
                            negative_cases_for_chosen_constraint, child_positive_case))

                # my_negative_cases_times_plain_child_group = list()
                # for specific_negative_case in negative_cases_for_chosen_constraint:
                #     my_negative_cases_times_plain_child_group.append(
                #         specific_negative_case.merge_my_copy_with_group(const_group)
                #     )
                negative_cases_for_chosen_constraint = my_negative_cases_times_plain_child_group

            negative_cases.extend(negative_cases_for_chosen_constraint)
        return negative_cases


class OrGroup(Thing):
    namespace = _core

    def prepare_negative_cases(self):
        negative_cases = list()
        negative_case_under_process = _core.ConstraintGroup(
            f"negative_OR_case_{self.name}"
        )
        negative_case_under_process.meta = f"Negated all constraints and child groups from {self.name}"
        negative_cases.append(negative_case_under_process)
        for constraint in self.has_constraints:
            inverted_constraint_to_group = self.inverter.invert(constraint)
            if len(inverted_constraint_to_group.has_constraints) == 1:
                negative_case_under_process.has_constraints.append(
                    inverted_constraint_to_group.has_constraints[0])
            else:
                negative_case_under_process.contains_constraint_groups.append(
                    inverted_constraint_to_group)

        if len(self.contains_constraint_groups) > 0:
            for child_group in self.contains_constraint_groups:
                child_group_list_of_negative_cases = child_group.prepare_negative_cases()
                for child_case in child_group_list_of_negative_cases:
                    negative_cases.append(negative_case_under_process.merge_my_copy_with_group(child_case))

        if len(negative_case_under_process.contains_constraint_groups) > 0:
            for child_group in negative_case_under_process.contains_constraint_groups:
                child_group_list_of_negative_cases = child_group.prepare_negative_cases()
                for child_case in child_group_list_of_negative_cases:
                    negative_cases.append(negative_case_under_process.merge_my_copy_with_group(child_case))
        return negative_cases

    def prepare_positive_cases(self):
        positive_cases = list()
        list_of_elements_for_breakdown = self.has_constraints.copy()
        list_of_elements_for_breakdown.extend(self.contains_constraint_groups)
        for constraint_or_group_too_keep in list_of_elements_for_breakdown:
            positive_case_under_process = _core.ConstraintGroup(
                f"{ordinal(len(positive_cases)+1)}_positive_case_of_{self.name}")
            for constraint in self.has_constraints:
                if constraint_or_group_too_keep == constraint:
                    positive_case_under_process.has_constraints.append(constraint)
                    positive_case_under_process.meta = \
                        f"Negated all, but chosen {constraint_or_group_too_keep.name} " \
                        f"from OR group {self.name} for positive case"
                else:  # not too keep constraint
                    positive_case_under_process.has_constraints.append(constraint.toggle_restriction())

            partially_processed_variances = [positive_case_under_process]
            for const_group in self.contains_constraint_groups:
                if constraint_or_group_too_keep == const_group:
                    child_group_list_of_positive_cases = const_group.prepare_positive_cases()
                    new_further_processed_variances = list()
                    for left_partial in partially_processed_variances:
                        for child_variant in child_group_list_of_positive_cases:
                            new_further_processed_variances.append(
                                left_partial.merge_my_copy_with_group(child_variant)
                            )
                    partially_processed_variances = new_further_processed_variances
                    continue
                child_group_list_of_restriction_variances = const_group.make_all_restricting_variations()
                new_further_processed_variances = list()
                for left_partial in partially_processed_variances:
                    for child_restriction_variant in child_group_list_of_restriction_variances:
                        new_further_processed_variances.append(
                            left_partial.merge_my_copy_with_group(child_restriction_variant)
                        )
                partially_processed_variances = new_further_processed_variances
            positive_cases.extend(partially_processed_variances)
        return positive_cases

    # def _make_realizable_from_and_group(self, not_needed_constraint_for_and_group):
    #     if not isinstance(self, _core.AndGroup):
    #         raise Exception("ERROR: Calling a function only for AND groups.")
    #     anded_constraint_list = self.has_constraints.copy()
    #     aggregated_meta_info = ""
    #     for child_constraint_group in self.contains_constraint_groups:
    #         random_main_constraint = random.choice(child_constraint_group.has_constraints)
    #         aggregated_meta_info = f"{aggregated_meta_info}, chosen {random_main_constraint.name}"
    #         child_result, meta_info = \
    #             child_constraint_group.make_realizable_list_of_constraints_for(random_main_constraint)
    #         anded_constraint_list.extend(child_result)
    #     return anded_constraint_list, aggregated_meta_info