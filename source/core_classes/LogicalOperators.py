from owlready2 import Thing
from utils.utils import ExtensionContext


def extend_core(context: ExtensionContext):
    _core = context.core

    class AndGroup(Thing):
        namespace = _core

        def checking_logical_operators(self):
            print("AND AND AND")

    class OrGroup(Thing):
        namespace = _core

        def checking_logical_operators(self):
            print("OR OR OR")



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