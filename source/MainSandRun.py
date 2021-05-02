from owlready2 import *
from core_classes.Constraints import extend_core as extend_constraints
from core_classes.ConstraintGroups import extend_core as extend_constraint_groups

onto_path.append("./resources/core/")
onto_path.append("./resources/development/")

print("INFO: Running Ontology")
onto = get_ontology("http://corechuck.com/modeling/dependent_onto")
# onto = get_ontology("http://corechuck.com/modeling/dependent_ontos")

onto.load()

core = onto.imported_ontologies[0]  # <- core classes are in wrong ontology
extend_constraints(core)
extend_constraint_groups(core)

sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True,keep_tmp_file = 1,debug=1)
print("INFO: Reasoned with pellet.")

print("Constraints:")
for indiv in onto.individuals():
    if isinstance(indiv, core.Constraint):
        print(indiv.generate())


print("Constraints group:")
for indiv in onto.individuals():
    if isinstance(indiv, core.ConstraintGroup):
        print(indiv.fullfil_constraints())


# TODO:
# 1. Move core to core !!!!!! DONE
# 2. Git Repo. Done
# 2. Implement all types in constraints. Done
# 2. Implement extensions to constraintGroup and generation of whole table
# 4. DependencyConstraints inside group
# 3. Tests ?
