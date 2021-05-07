from owlready2 import *
from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
from core_classes.SimpleExtensions import extend_core as extend_simple_types

onto_path.append("./resources/core/")
onto_path.append("./resources/development/")

print("INFO: Running Ontology")
onto = get_ontology("http://corechuck.com/modeling/dependent_onto")
onto.load()

# onto.get_namespace("http://purl.obolibrary.org/obo/")

core = onto.imported_ontologies[0]  # <- core classes are in wrong ontology
extend_constraints(core)
extend_constraint_groups(core)
extend_simple_types(core)

sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True,keep_tmp_file = 1,debug=1)
print("INFO: Reasoned with pellet.")

print("# Constraints:")
for indiv in onto.individuals():
    if isinstance(indiv, core.Constraint):
        print(indiv.generate())


print("# Constraints group:")
for indiv in onto.individuals():
    if isinstance(indiv, core.RealizationDefinition):
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())
        print(indiv.fullfil_constraints())


# TODO:
# 1. Move core to core !!!!!! DONE
# 2. Git Repo. Done
# 2. Implement all types in constraints. Done
# 2. Implement extensions to constraintGroup and generation of whole table - done
# 3. Merge Realization with Minimum requirements - done
# 3. abriviate column names.
# 4. Dependency inside group - 
# 4. Dependency outside group -
# 4. RangeConstraint - default min and max
# 3. Tests ?
