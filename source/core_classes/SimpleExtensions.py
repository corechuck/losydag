from owlready2 import Thing
from utils.context import ExtensionContext


def extend_core(context: ExtensionContext):
    _core = context.core

    class Column(Thing):
        namespace = _core

        @property
        def plain_name(self):
            splitted_name = self.name.split(".")
            return splitted_name[-1]

    class Table(Thing):
        namespace = _core

        def get_column_by_name(self, column_name):
            for column in self.has_columns:
                if column.plain_name == column_name:
                    return column

            return None
