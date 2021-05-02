import rstr
import random
from owlready2 import Thing
#from SyntheticExceptions import GenerationTypeException


def extend_core(_core):

    class ConstraintGroup(Thing):
        namespace = _core

        # def __init__(self):
        #     pass
        
        def fullfil_constraints(self):
            list_of_constraints = self.has_constraints
            return f"Has {len(list_of_constraints)} constraints."
