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
