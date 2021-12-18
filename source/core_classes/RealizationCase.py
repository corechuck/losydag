import rstr
import random
import datetime
import math
from owlready2 import Thing, sync_reasoner_pellet, sync_reasoner, sync_reasoner_hermit

from utils.utils import _supervise_constraint_generation
from utils.context import ExtensionContext


def extend_core(context: ExtensionContext):
    _core = context.core
    
    class RealizationCase(Thing):
        namespace = _core
        mapping_dict = None
        _verbal = True
        is_prepared_for_realization = False

        # def __init__(self, name, namespace=None):
        #     super().__init__(name, namespace)
        
        def realize(self):
            meta_definitions = self._prepare_for_realization()
            _supervise_constraint_generation(self._realize, f"{self.name}")
            return self._get_aggregated_results(meta_definitions)

        def realize_all_test_case_relevant_datasets(self):
            """ This method generates datasets using generators that keep track of boundary conditions and returns
            all meaningfully variable datasets for all constraints contain in that group:

             Consider to mark constraints that should give all potential variances of test data and treat that as
             relevant. That one for positive all are relevant, but for negative take only negated ones."""

            all_data_sets = []
            for definition in self.contains_realizations:
                definition.prepare_relevant_partition_values()

            loop_count = 0
            loop_max = 1000
            while self._has_more_relevant_datasets_for_generation() and loop_count < loop_max:
                loop_count += 1
                all_data_sets.append(self.realize_random_fresh())

            return all_data_sets

        def _has_more_relevant_datasets_for_generation(self):
            return any([realization_definition.has_more_relevant_options()
                        for realization_definition in self.contains_realizations])

        def realize_random_fresh(self):
            meta_definitions = self._prepare_for_realization()
            [rd.clear_results() for rd in self.contains_realizations]
            _supervise_constraint_generation(self._realize, f"{self.name}")
            return self._get_aggregated_results(meta_definitions)

        def _prepare_for_realization(self):
            if self.is_prepared_for_realization:
                return

            # No test starting with OR GROUP operator as main Constraint Group you try to realize
            # break contains_constraint_groups from pick one and
            meta_definitions = self.__prepare_constraint_groups_to_realizable()
            self.__setup_realizations_definitions()

            self.__prepare_min_reqs_for_not_custom_constrained_but_referred_tables()
            sync_reasoner_pellet(infer_data_property_values=False, infer_property_values=True)
            self.__prepare_table_name_to_singular_realization_def_dict()
            self.__setup_external_dependencies_with_single_realizations_definitions()

            self.is_prepared_for_realization = True
            return meta_definitions

        def _realize(self, not_ready_acc):
            for definition in self.contains_realizations:
                if self._verbal:
                    print(f"INFO: Evaluating {definition.name}:")
                # TODO: rename has_realized_constraints to is_realized
                if definition.has_realized_constraints:
                    if self._verbal:
                        print(f"INFO: Already realized : {definition.name}")
                    continue

                if definition.is_ready():
                    if self._verbal:
                        print(f"INFO: Realizing : {definition.name}")
                    definition.fulfill_constraints()
                else:
                    if self._verbal:
                        print(f"INFO: Not ready : {definition.name}")
                    not_ready_acc.append(definition)

        def _get_aggregated_results(self, meta):
            aggregate = dict()
            for definition in self.contains_realizations:
                if not definition.has_realized_constraints:
                    print(f"WARN: cannot aggregate not realized constraint {definition.name}")
                    continue
                if definition.constraints_table().name not in aggregate.keys():
                    aggregate[definition.constraints_table().name] = list()

                aggregate[definition.constraints_table().name].append(definition._return_dict)
            
            return aggregate

        def __prepare_constraint_groups_to_realizable(self):
            chosen_branches = list()
            for realization_definition in self.contains_realizations:
                meta_list = realization_definition.pick_branches_from_or_groups()
                if len(meta_list) == 0:
                    continue
                chosen_branches.append({realization_definition.name: meta_list})
                print(f"INFO: Found branched constraints in {realization_definition.name} chosen list {meta_list}")
                # realization_definition.prepare_for_realization()
                # flat_list, meta = realization_definition.make_realizable_list_of_constraints_random()
                # print(f"META groups: {meta}")
                # if isinstance(realization_definition, _core.OrGroup):
                #     realization_definition.is_a.remove(_core.OrGroup)
                #     realization_definition.is_a.append(_core.AndGroup)
                # realization_definition.has_constraints = flat_list  #TODO: this is good place to assign to work_constraints
                # realization_definition.is_constraining_tables = list()
                # realization_definition.unify_constraints()
            return chosen_branches

        def __setup_realizations_definitions(self):
            for definition in self.contains_realizations:
                definition.prepare_for_realization()

        def __setup_external_dependencies_with_single_realizations_definitions(self):
            for definition in self.contains_realizations:
                if definition.is_having_external_dependencies():
                    definition.prepare_external_dependencies_with_single_realization_definition(
                        self.mapping_dict)

        def __prepare_table_name_to_singular_realization_def_dict(self):
            if self.mapping_dict is not None:
                return self.mapping_dict

            self.mapping_dict = dict()
            for definition in self.contains_realizations:
                if definition.constraints_table().name not in self.mapping_dict:
                    self.mapping_dict[definition.constraints_table().name] = definition
                    continue
                if definition.constraints_table().name in self.mapping_dict:
                    self.mapping_dict[definition.constraints_table().name] = None

            self.mapping_dict = dict(filter(lambda el: el[1], self.mapping_dict.items()))
                
        def __prepare_min_reqs_for_not_custom_constrained_but_referred_tables(self):
            case_needed_tables = set()
            for definition in self.contains_realizations:
                case_needed_tables = case_needed_tables | definition.get_referred_tables()

            for needed_table in case_needed_tables:
                is_needed_table_in_realization_case = \
                    any(map(
                        lambda rd: rd.constraints_table().name == needed_table.name,
                        self.contains_realizations))
                if not is_needed_table_in_realization_case:
                    # TODO: this part should not be here but somewhere deeper
                    new_def = _core.RealizationDefinition(
                        f"{needed_table.has_min_reqs.name}_temp_{random.randint(10000,99999)}")
                    new_def.compliment_with(needed_table.has_min_reqs)
                    self.contains_realizations.append(new_def)

            print(f"INFO: Referenced tables: {case_needed_tables}")

            # TODO: Extend ontology with new Table and expect magic to happen
