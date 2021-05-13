from owlready2 import *
from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
from core_classes.SimpleExtensions import extend_core as extend_simple_types
from core_classes.Dependencies import extend_core as extend_dependencies
from core_classes.RealizationCase import extend_core as extend_realization_case

onto_path.append("./resources/core/")
onto_path.append("./resources/development/")

print("INFO: Running Ontology")
onto = get_ontology("http://corechuck.com/modeling/dependent_onto")
# core = get_ontology("http://corechuck.com/modeling/core_check")
onto.load()

# onto.get_namespace("http://purl.obolibrary.org/obo/")


core = onto.imported_ontologies[0]  # <- core classes are in wrong ontology
extend_constraints(core)
extend_dependencies(core)
extend_constraint_groups(core)
extend_simple_types(core)
extend_realization_case(core)

sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True,keep_tmp_file = 1,debug=1)
print("INFO: Reasoned with pellet.")

# print("# Constraints:")
# for indiv in onto.individuals():
#     if isinstance(indiv, core.Constraint):
#         print(indiv.generate())


# last_realization = None
# print("# Constraints group:")
# for indiv in onto.individuals():
#     if isinstance(indiv, core.RealizationDefinition):
#         is_th_same = last_realization is None or last_realization is indiv
#         last_realization = indiv
#         print(f"DEBUG: {indiv} is the same as {last_realization}: {is_th_same}")
#         #print(f"INFO: Result based on: {indiv.name}")
#         print(indiv.fullfil_constraints())
#         print(indiv.fullfil_constraints())

# print("# Second pass:")
# for indiv in onto.individuals():
#     if isinstance(indiv, core.RealizationDefinition):
#         last_realization = indiv
#         print(f"INFO: Result based on: {indiv.name}")
#         print(indiv.fullfil_constraints())

print("# Realization case:")
for real_case in onto.individuals():
    if isinstance(real_case, core.RealizationCase):
        print(f"INFO: Result based on: {real_case.name}")
        # contains_realizations
        print(real_case.realize())

        

        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())
        # print(indiv.fullfil_constraints())


# TODO:
# 1. Move core to core !!!!!! DONE
# 2. Git Repo. Done
# 2. Implement all types in constraints. Done
# 2. Implement extensions to constraintGroup and generation of whole table - done
# 3. Merge Realization with Minimum requirements - done
# 3. abriviate column names. done
# 4. Dependency inside group - done
# 4. Dependency outside group -
# 4. RangeConstraint - default min and max
# 3. Tests ?
