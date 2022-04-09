from utils.utils import QueryMissformatException


class QueryContext:
    defined_realization: dict = dict()
    constraint_groups_heap: list = list()
    is_new_group = True

    def peek_latest_group(self):
        if len(self.constraint_groups_heap) == 0:
            raise QueryMissformatException("Too many closing brackets")

        return self.constraint_groups_heap[-1]

    def push_new_group(self, group):
        self.constraint_groups_heap.append(group)

    def pop_latest_group(self):
        return self.constraint_groups_heap.pop()
