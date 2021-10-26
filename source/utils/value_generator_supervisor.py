import random


class ValueGenerationSupervisor:
    TRIES_COUNT = 500

    def generate(self, constraint, not_matching_constraint_list, local_dict):
        tries = 0
        tried_values = list()

        while True:
            tries += 1
            if constraint.has_more_relevant_options():
                random.shuffle(constraint.partition_relevant_value_options)
                generated_value = constraint.partition_relevant_value_options.pop()
            else:
                generated_value = str(constraint._generate(local_dict))

            if not self._is_value_matching_any_constraint(generated_value, not_matching_constraint_list):
                return generated_value
            else:
                tried_values.append(generated_value)

                if tries >= self.TRIES_COUNT:
                    print(f"INFO: Tried values {tried_values}")
                    raise Exception(f"ERROR: Could not generate value that met constrained in {self}")

        return "#non-value-002"

    def _is_value_matching_any_constraint(self, value, matching_list):
        return any(constraint.does_value_match_constraint(value) for constraint in matching_list)