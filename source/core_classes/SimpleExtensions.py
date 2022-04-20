from owlready2 import Thing
from utils.context import ExtensionContext
import utils.context


if not utils.context.core_context\
        or not utils.context.core_context.core\
        or not utils.context.core_context.value_generation_supervisor:
    raise Exception("Cannot import Operators without initialized utils.context.core_context")

_core = utils.context.core_context.core


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
