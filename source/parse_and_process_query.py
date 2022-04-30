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
all_cases = list()


def add_to_aggregator(data: dict, cases: list):
    datasets.update(data)
    all_cases.extend(cases)


if parser.context.command == GeneratorCommands.POSITIVE_CASES.value:
    print(f"INFO: Generating all variants of positive cases")
    add_to_aggregator(*generator.generate_all_variations_for_all_discovered_positive_cases(group=query_group))

elif parser.context.command == GeneratorCommands.NEGATIVE_CASES.value:
    print(f"INFO: Generating all variants of negative cases")
    add_to_aggregator(*generator.generate_all_variations_for_all_discovered_negative_cases(group=query_group))

elif parser.context.command == GeneratorCommands.ALL_CASES.value:
    print(f"INFO: Generating all variants of positive cases")
    add_to_aggregator(*generator.generate_all_variations_for_all_discovered_positive_cases(group=query_group))
    print(f"INFO: Generating all variants of negative cases")
    add_to_aggregator(*generator.generate_all_variations_for_all_discovered_negative_cases(group=query_group))


elif parser.context.command == GeneratorCommands.EXAMPLE_POSITIVE_CASES.value:
    print(f"INFO: Generating examples of positive cases")
    add_to_aggregator(*generator.generate_examples_of_discovered_positive_cases(group=query_group))

elif parser.context.command == GeneratorCommands.EXAMPLE_NEGATIVE_CASES.value:
    print(f"INFO: Generating examples of negative cases")
    add_to_aggregator(*generator.generate_examples_of_discovered_negative_cases(group=query_group))

elif parser.context.command == GeneratorCommands.EXAMPLE_ALL_CASES.value:
    print(f"INFO: Generating examples of positive cases")
    add_to_aggregator(*generator.generate_examples_of_discovered_positive_cases(group=query_group))
    print(f"INFO: Generating examples of negative cases")
    add_to_aggregator(*generator.generate_examples_of_discovered_negative_cases(group=query_group))
else:
    raise Exception("ERROR: Generation Error :(")


group_descriptors = dict()
group_data = dict()
count = 0
for key in datasets.keys():
    stripped_key = key.replace("Positive_case__", "").replace("Negative_case__", "")
    count += 1
    group_descriptors[f"G{count}"] = {
        "case_name": key,
        "meta": next(case.meta for case in all_cases if stripped_key in case.name)
    }
    group_data[f"G{count}"] = datasets[key]

pp = pprint.PrettyPrinter(indent=2, width=150)
print("INFO: Presenting excerpt from what datasets represent:")
pp.pprint(group_descriptors)

pp = pprint.PrettyPrinter(indent=2, width=250)
print("INFO: Presenting generated data:")
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
