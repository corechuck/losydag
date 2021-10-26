from owlready2 import Thing


def extend_core(_core):

    class AndGroup(Thing):
        namespace = _core

        def checking_logical_operators(self):
            print("AND AND AND")

    class OrGroup(Thing):
        namespace = _core

        def checking_logical_operators(self):
            print("OR OR OR")
