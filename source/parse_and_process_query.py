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

generator = LosydagGenerator(parser.context.schema_onto)
datasets = generator.generate_data_for_all_positive_cases(group=query_group)
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(datasets)






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
