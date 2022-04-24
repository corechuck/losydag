import argparse
import pprint
from LosydagGenerator import LosydagGenerator
from generation_request.syntax_parser import GenerationRequestSyntaxParser
from utils.utils import GeneratorCommands

# [positive cases|negative cases|all cases|example|example positive cases|example negative cases|example all cases]
parser = argparse.ArgumentParser(description='Losydag entry for parsing query and generating data.')
parser.add_argument("--onto-location", help="Set location from which to read local ontology.")
parser.add_argument("--query-path", help="Provide path to a query that should be parsed.")
args = parser.parse_args()

parser = GenerationRequestSyntaxParser(args.onto_location)
query_group = parser.parse_request_from_file(args.query_path)
generator = LosydagGenerator(parser.context.schema_onto)

datasets = dict()
if parser.context.command == GeneratorCommands.POSITIVE_CASES.value:
    print(f"INFO: Generating all variants of positive cases")
    datasets.update(generator.generate_all_variations_for_all_discovered_positive_cases(group=query_group))

elif parser.context.command == GeneratorCommands.NEGATIVE_CASES.value:
    print(f"INFO: Generating all variants of negative cases")
    datasets.update(generator.generate_all_variations_for_all_discovered_negative_cases(group=query_group))

elif parser.context.command == GeneratorCommands.ALL_CASES.value:
    print(f"INFO: Generating all variants of positive cases")
    datasets.update(generator.generate_all_variations_for_all_discovered_positive_cases(group=query_group))
    print(f"INFO: Generating all variants of negative cases")
    datasets.update(generator.generate_all_variations_for_all_discovered_negative_cases(group=query_group))


elif parser.context.command == GeneratorCommands.EXAMPLE_POSITIVE_CASES.value:
    print(f"INFO: Generating examples of positive cases")
    datasets.update(generator.generate_examples_of_discovered_positive_cases(group=query_group))

elif parser.context.command == GeneratorCommands.EXAMPLE_NEGATIVE_CASES.value:
    print(f"INFO: Generating examples of negative cases")
    datasets.update(generator.generate_examples_of_discovered_negative_cases(group=query_group))

elif parser.context.command == GeneratorCommands.EXAMPLE_ALL_CASES.value:
    print(f"INFO: Generating examples of positive cases")
    datasets.update(generator.generate_examples_of_discovered_positive_cases(group=query_group))
    print(f"INFO: Generating examples of negative cases")
    datasets.update(generator.generate_examples_of_discovered_negative_cases(group=query_group))
else:
    raise Exception("ERROR: Generation Error :(")


group_names = dict()
group_data = dict()
count = 0
for key in datasets.keys():
    count += 1
    group_names[f"G{count}"] = key
    group_data[f"G{count}"] = datasets[key]

pp = pprint.PrettyPrinter(indent=2, width=250)
pp.pprint(group_names)
pp.pprint(group_data)

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
