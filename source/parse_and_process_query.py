import argparse
import pprint
from owlready2 import *
from LosydagGenerator import LosydagGenerator
from generation_request.syntax_parser import GenerationRequestSyntaxParser

parser = argparse.ArgumentParser(description='Losydag entry for parsing query and generating data.')
parser.add_argument("--onto-location", help="Set location from which to read local ontology.")
parser.add_argument("--query-path", help="Provide path to a query that should be parsed.")
args = parser.parse_args()

parser = GenerationRequestSyntaxParser(args.onto_location)
query_group = parser.parse_request_from_file(args.query_path)

cases = query_group.prepare_positive_cases()

query_group.pick_branches_from_or_groups()
realization_case = query_group.build_realization_case()
data = realization_case.realize()

generator = LosydagGenerator(parser.context.schema_onto)
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(data)




# print("----------------------------")
# pp.pprint(generator.realize_fresh("RealizationCase.Check1", is_silent=True))
# print("----------------------------")
# pp.pprint(generator.realize_fresh("RealizationCase.Check1", is_silent=True))
# print("----------------------------")
# pp.pprint(generator.realize_fresh("RealizationCase.Check1", is_silent=True))
# print("----------------------------")
# pp.pprint(generator.realize_fresh("RealizationCase.Check1", is_silent=True))

# from core_classes.Constraints import extend_core as extend_constraints
# from core_classes.ConstraintGroups import extend_core as extend_constraint_groups
# from core_classes.SimpleExtensions import extend_core as extend_simple_types
# from core_classes.Dependencies import extend_core as extend_dependencies
# from core_classes.RealizationCase import extend_core as extend_realization_case

# onto_path.append("./resources/core/")
# onto_path.append("./resources/development/")

# print("INFO: Running Ontology")
# onto = get_ontology("http://corechuck.com/modeling/dependent_onto")
# # core = get_ontology("http://corechuck.com/modeling/core_check")
# onto.load()

# # onto.get_namespace("http://purl.obolibrary.org/obo/")


# core = onto.imported_ontologies[0]  # <- core classes are in wrong ontology
# extend_constraints(core)
# extend_dependencies(core)
# extend_constraint_groups(core)
# extend_simple_types(core)
# extend_realization_case(core)

# sync_reasoner_hermit(infer_property_values=True)
# # sync_reasoner_pellet(infer_data_property_values=True, infer_property_values=True)
# # sync_reasoner_pellet()  # infer_data_property_values=True, infer_property_values=True)
# print("INFO: Reasoned with pellet.")

# pp = pprint.PrettyPrinter(indent=2)
# print("# Realization case:")
# for real_case in onto.individuals():
#     if isinstance(real_case, core.RealizationCase):
#         print(f"INFO: Result based on: {real_case.name}")
#         # contains_realizations



# TODO:
# 1. Move core to core !!!!!! DONE
# 2. Git Repo. Done
# 2. Implement all types in constraints. Done
# 2. Implement extensions to constraintGroup and generation of whole table - done
# 3. Merge Realization with Minimum requirements - done
# 3. abriviate column names. - done
# 4. Dependency inside group - done
# 4. Dependency outside group - done
# 5. Find missing table definition - in RealizationCase done
# 4. RangeConstraint - default min and max
# 6. Ad infinitum - deriving needed tables that were not present in realization case.
# 3. Tests - part 1 - done
# 6. Add Column uniqueness and used values
