from utils.utils import QueryMissformatException


class QueryContext:
    is_new_group = True
    core = None
    schema_onto = None
    constraint_groups_heap: list
    command: str = None
    defined_realization: dict
    load_location: str = None

    def __init__(self, load_location):
        self.defined_realization = dict()
        self.constraint_groups_heap = list()
        self.load_location = load_location

    def peek_latest_group(self):
        if len(self.constraint_groups_heap) == 0:
            raise QueryMissformatException("Too many closing brackets")

        return self.constraint_groups_heap[-1]

    def push_new_group(self, group):
        self.constraint_groups_heap.append(group)

    def pop_latest_group(self):
        return self.constraint_groups_heap.pop()
