from owlready2 import Thing
import rstr



def extend_core(_core):

    class Constraint(Thing):
        namespace = _core

        # def __init__(self):
        #     pass
        
        def generate(self):
            child_value = self._generate()
            return f"Child value: {child_value}"
            
        def _generate(self):
            return ""

    class RegexConstraint(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            return rstr.xeger("Rgx__\w{1,7}")


    class ListConstraint(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            return rstr.xeger("List__\w{1,7}")


    class RangeConstriant(Thing):
        namespace = _core

        # def __init__(self):
        #     super().__init__()
        
        def _generate(self):
            return rstr.xeger("Rng__\w{1,7}")

