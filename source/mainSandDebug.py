import os
import pprint

from owlready2 import *

onto_path.append(f"{os.getcwd()}/resources/core/")
onto_path.append(f"{os.getcwd()}/resources/development/")

core = get_ontology("http://corechuck.com/modeling/core_check")
# core_onto.load(only_local=True)

onto = get_ontology("http://corechuck.com/modeling/dependent_onto")

# core = onto.imported_ontologies[0]

# sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

# pp = pprint.PrettyPrinter(indent=2)

# cons = generator.core.Constraint()
#
# cons_2 = generator.onto.search_one(iri=f"*Constraint.Test2_Col3__list")
#
# pp.pprint(generator.realize_fresh("RealizationCase.Check1"))

# with onto:
class RealizationCase:
    namespace = core

    def foo(self):
        print("fakjsdhfkj")


onto.load(only_local=True)
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

# onto.load(only_local=True)
# sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

# rc1_list = onto.search(iri=f"*RealizationCase.Check1")
rc1 = onto.search_one(iri=f"*RealizationCase.Check1")
# rc1 = onto.search_one(iri=f"*RealizationCase.Check1", type=RealizationCase)
sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
# rc1 = rc1_list[0]
rc1.foo()

rc2 = RealizationCase("RealizationCase.CheckSandbox")
rc2.foo()
# print("fpo")
print(f"Are foos the same :{rc2.foo == rc1.foo}")

# for i in onto.individuals():
#     print(i.iri)

# class FooClassForFun:
#
#     def whatthehell(self):
#         print("the fuck")
#
#
# screemer = FooClassForFun()
# screemer.whatthehell()
