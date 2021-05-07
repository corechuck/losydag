from owlready2 import Thing


def extend_core(_core):

    class Column(Thing):
        namespace = _core

        @property
        def plain_name(self):
            splitted_name = self.name.split(".")
            return splitted_name[-1]

