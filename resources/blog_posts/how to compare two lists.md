# List subtraction when met condition

So we want to merge two sets of constraints and there is a few ways we can do it.

```

        def compliment_with(self, _other_constraint_group):
            """Key element to note here is that it can have only one constraint for
            one column"""
            temp_group = _core.ConstraintGroup(f"{self.name}_temp_{random.randint(100000,999999)}")
            temp_group.has_constraints = self.has_constraints.copy()

            taken_columns = self.get_names_of_constrained_columns()
            for other_constraint in _other_constraint_group.has_constraints:
                if other_constraint.is_constraining_column.name not in taken_columns:
                    temp_group.has_constraints.append(other_constraint)
                
            return temp_group

        def ___compliment_with(self, _other_constraint_group):

            temp_group = _core.ConstraintGroup(f"{self.name}_temp_{random.randint(100000,999999)}")
            temp_group.has_constraints = self.has_constraints.copy()

            constrained_columns = list()
            for my_constraint in self.has_constraints:
                constrained_columns.append(my_constraint.is_constraining_column.name)

            for other_constraint in _other_constraint_group.has_constraints:
                if other_constraint.is_constraining_column.name not in constrained_columns:
                    temp_group.has_constraints.append(other_constraint)
                
            return temp_group

        def _compliment_with(self, _other_constraint_group):

            temp_group = _core.ConstraintGroup(f"{self.name}_temp_{random.randint(100000,999999)}")
            temp_group.has_constraints = self.has_constraints.copy()

            for other_constraint in _other_constraint_group.has_constraints:
                is_other_constraint_overlapping = False
                for _my_constraint in self.has_constraints:
                    is_other_constraint_overlapping = \
                        is_other_constraint_overlapping or \
                            other_constraint.is_constraining_same_column_as(_my_constraint)
                if not is_other_constraint_overlapping:
                    temp_group.has_constraints.append(other_constraint)
                
            return temp_group


        def __compliment_with(self, _other_constraint_group):

            temp_group = _core.ConstraintGroup(f"{self.name}_temp_{random.randint(100000,999999)}")
            temp_group.has_constraints = self.has_constraints.copy()

            for candidate_constraint in _other_constraint_group.has_constraints:
                if any(map(
                    lambda _already_chosen_constraint: 
                        _already_chosen_constraint.is_constraining_same_column_as(candidate_constraint),
                    self.has_constraints
                )):
                    continue
                temp_group.has_constraints.append(candidate_constraint)
                
            return temp_group

        def _____compliment_with_(self, _other_constraint_group):
            """Key element to note here is that it can have only one constraint for
            one column"""
            temp_group = _core.ConstraintGroup(f"{self.name}_temp_{random.randint(100000,999999)}")
            temp_group.has_constraints = self.has_constraints.copy()

            taken_columns_set = set(self.get_names_of_constrained_columns())
            proposed_columns_set = set(_other_constraint_group.get_names_of_constrained_columns())
            columns_to_add = proposed_columns_set - taken_columns_set

            for other_constraint in _other_constraint_group.has_constraints:
                if other_constraint.is_constraining_column.name in columns_to_add:
                    temp_group.has_constraints.append(other_constraint)
            
            return temp_group

        def merge_with_override(self, _other_constraint_group):
            """Key element to note here is that it can have only one constraint for
            one column"""
            temp_group = _core.ConstraintGroup(f"{self.name}_temp_{random.randint()}")
            temp_group.has_constraints = _other_constraint_group.has_constraints.copy()

            for candidate_constraint in self.has_constraints:
                if any(map(lambda _already_chosen_constraint: 
                    candidate_constraint.is_constraining_same_column_as(_already_chosen_constraint),
                    temp_group.has_constraints
                )):
                    continue
                temp_group.has_constraints.append(candidate_constraint)
                
            return temp_group

        @property
        def get_names_of_constrained_columns(self):
            return [const.is_constraining_column.name for const in self.has_constraints]

```