import csv
import decimal
import json
import os
from datetime import datetime

import ijson
import ijson.backends
from owlready2 import get_ontology, sync_reasoner_pellet, OwlReadyInconsistentOntologyError

from core_classes import DataTypes
from core_classes import SimpleExtensions
from core_classes import Constraints
from core_classes import Dependencies
from core_classes import ConstraintGroups
from core_classes import LogicalOperators
from core_classes import RealizationCase

from utils.context import core_context

# file_for_processing = "C:\work\projects\intercars\db\schema_discovery\csv\mdp-database.scrapped_data.csv"
# with open(file_for_processing, encoding="utf-8-sig") as mapping_file:
#
#     table_example_reader = csv.DictReader(mapping_file, delimiter=',', quotechar='"', escapechar='\\')
#     for table_single_entry in table_example_reader:
#         print(table_single_entry)

aggregated_objects_data = {}
aggregated_objects_metadata = {}

file_for_processing = "C:\work\projects\intercars\db\schema_discovery\json\mdp-database.master_tasks.json"


def is_object_a_date(value):
    return isinstance(value, dict) and "$date" in value


def get_type_of_data(value):
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, decimal.Decimal):
        return "float"
    if isinstance(value, bool):
        return "bool"
    if is_object_a_date(value):
        return "date"


def cook_attribute_path(object_path, attribute):
    if object_path:
        return f"{object_path}.{attribute}"
    else:
        return attribute


def scan_object(root_summary_dict, scan_object_summary, object_path, object_under_scan):
    for attribute in object_under_scan.keys():
        attribute_path = cook_attribute_path(object_path, attribute)

        if attribute_path not in scan_object_summary:
            scan_object_summary[attribute_path] = {"amount": 0}
        scan_object_summary[attribute_path]["amount"] += 1

        if isinstance(object_under_scan[attribute], list):
            # print("cope with list")
            # print(f"{attribute}: {object_under_scan[attribute]}")
            if isinstance(object_under_scan[attribute], list):
                if "type" not in scan_object_summary[attribute_path]:
                    scan_object_summary[attribute_path].update({
                        "type": "internal_reference",
                        "sizes_set": set()
                    })
                scan_object_summary[attribute_path]["sizes_set"].add(len(object_under_scan[attribute]))
                if len(object_under_scan[attribute]) > 0 and isinstance(object_under_scan[attribute][0], dict):
                    scan_list_of_objects(root_summary_dict, attribute_path, object_under_scan[attribute])
                elif len(object_under_scan[attribute]) > 0 and isinstance(object_under_scan[attribute][0], list):
                    # handle matrix values ...
                    print(f"Handle Matrix values: {object_under_scan[attribute][0]}.")
            else:
                if "type" not in scan_object_summary[attribute_path]:
                    scan_object_summary[attribute_path].update({
                        "type": "internal_list",
                        "sizes": [],
                        "flatten_values": [],
                        "flatten_values_set": set()
                    })
                scan_object_summary[attribute_path]["sizes"].append(len(scan_object_summary[attribute_path]))
                scan_object_summary[attribute_path]["flatten_values"].extend(object_under_scan[attribute])
                for single_element in object_under_scan[attribute]:
                    scan_object_summary[attribute_path]["flatten_values_set"].add(single_element)

            continue

        if (object_under_scan[attribute] and
            isinstance(object_under_scan[attribute], dict) and
            not is_object_a_date(object_under_scan[attribute])
        ):
            # print(f"Cope with internal object without new collection.")
            # print(f"{attribute}: {object_under_scan[attribute]})")
            if "type" not in scan_object_summary[attribute_path]:
                scan_object_summary[attribute_path].update({
                    "type": "flatten_internal_object"
                })
            scan_object(root_summary_dict, scan_object_summary, attribute_path, object_under_scan[attribute])
            continue

        # print(f"{attribute}: {object_under_scan[attribute]}")
        if object_under_scan[attribute]:
            if "values" not in scan_object_summary[attribute_path]:
                scan_object_summary[attribute_path].update({
                    "type": "attribute",
                    "values": [],
                    "values_set": set(),
                    "types": {
                        "string": 0,
                        "int": 0,
                        "float": 0,
                        "date": 0,
                        "bool": 0
                    }
                })
            # this is a hack for now
            attribute_value = object_under_scan[attribute]
            if is_object_a_date(attribute_value):
                attribute_value = datetime.strptime(attribute_value["$date"], '%Y-%m-%dT%H:%M:%S.%fZ')
            scan_object_summary[attribute_path]["values"].append(attribute_value)
            scan_object_summary[attribute_path]["values_set"].add(attribute_value)
            # print(f"Value and type: {attribute} and {get_type_of_data(object_under_scan[attribute])}")
            scan_object_summary[attribute_path]["types"][get_type_of_data(object_under_scan[attribute])] += 1


def scan_list_of_objects(root_summary_dict, object_path, objects_to_iterate):
    if object_path not in root_summary_dict:
        root_summary_dict[object_path] = {}
        aggregated_objects_metadata[object_path] = {}
    scan_object_summary = root_summary_dict[object_path]
    scanned_object_index = -1
    for object_under_scan in objects_to_iterate:
        scanned_object_index += 1
        if "." not in object_path:
            print(f"Path {object_path} scanning {scanned_object_index}th")
        # print(f"Scaning: {object_under_scan}")
        # is object or not ...
        if object_under_scan:
            scan_object(root_summary_dict, scan_object_summary, object_path, object_under_scan)
    aggregated_objects_metadata[object_path]["amount"] = scanned_object_index+1


search_dir_path = "C:\work\projects\intercars\db\schema_discovery\json"
for json_file in os.listdir(search_dir_path):
    if ".json" not in json_file:
        continue
    file_for_processing = os.path.join(search_dir_path, json_file)
    with open(file_for_processing, encoding="utf-8-sig") as json_collection:
        scan_list_of_objects(
            aggregated_objects_data,
            json_file.replace(".json", "").replace("mdp-database.", ""),
            ijson.items(json_collection, 'item')
        )


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, datetime):
            return datetime.strftime(obj, "%Y-%m-%dT%H:%M:%S.%f%z")
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


# json_object = json.dumps(aggregated_object_data, indent=2, cls=SetEncoder)
# with open(os.path.join(search_dir_path, "metadata_aggregation.json"), "w") as outfile:
#     outfile.write(json_object)

#
# # try to generate owl ready file with tables and columns

def get_column_data_type(column_meta_data, ontology_under_build):

    if "types" not in column_meta_data:
        return core_context.core.search_one(iri="http://corechuck.com/modeling/core_check#DataType_String")

    max_amount = 0
    max_type = None
    for type_name in column_meta_data["types"]:
        if column_meta_data["types"][type_name] > max_amount:
            max_amount = column_meta_data["types"][type_name]
            max_type = type_name

    if max_amount == 0:
        return None

    if max_type == "string":
        return core_context.core.search_one(iri="http://corechuck.com/modeling/core_check#DataType_String")
    elif max_type == "bool":
        return core_context.core.search_one(iri="http://corechuck.com/modeling/core_check#DataType_Bool")
    elif max_type == "float":
        decimal_float = ontology_under_build.search_one(iri="DataType_float")
        if decimal_float:
            return decimal_float

        decimal_float = core_context.core.Decimal("DataType_float", namespace=ontology_under_build)
        decimal_float.has_precision = 12
        decimal_float.has_scale = 2
        return decimal_float
    elif max_type == "int":
        decimal_float = ontology_under_build.search_one(iri="DataType_integer")
        if decimal_float:
            return decimal_float

        decimal_int = core_context.core.Decimal("DataType_integer", namespace=ontology_under_build)
        decimal_int.has_precision = 10
        decimal_int.has_scale = 0
        return decimal_int
    elif max_type == "date":
        return core_context.core.search_one(iri="http://corechuck.com/modeling/core_check#DataType_Date")
    else:
        return None


core_context.core.load()

first_cook_batch_filename = "resources/foo/first_cook_batch.owl"
onto_under_build = get_ontology(f"http://cooking_graphs.com/{first_cook_batch_filename}")
onto_under_build.imported_ontologies.append(core_context.core)
# onto_under_build.load()

# aggregate_table = core_context.core.Table("cooked_tabel_01", namespace=onto_under_build)
# onto_under_build.individuals().

skipped_count = 0
skipped_list = list()

COLUMN_IGNORANCE_LIMIT = 0.1  # means if column exists in more than 10% of records it is saved.
COLUMN_SEMANTIC_LIST_LIMIT = 0.2


for table_meta_name in aggregated_objects_data:
    skipped_count = 0
    skipped_list = list()
    # if 'tasks.process_tracking' == table_meta_name:
    #     continue
    print(f"Producing {table_meta_name}")
    table_meta_data = aggregated_objects_data[table_meta_name]
    aggregate_table = core_context.core.Table(table_meta_name, namespace=onto_under_build)

    ignorance_limit = aggregated_objects_metadata[table_meta_name]["amount"]*0.1
    table_min_constraint_group = core_context.core.ConstraintGroup(f"MinGroup.{table_meta_name}", namespace=onto_under_build)
    aggregate_table.has_min_reqs = table_min_constraint_group

    if "." in table_meta_name:
        parent_path = table_meta_name[:table_meta_name.rfind(".")]
        ignorance_limit = aggregated_objects_data[parent_path][table_meta_name]["amount"]*0.1

        # Add artificial column with __internal_parent_id
        internal_reference_column_name = f"{table_meta_name}.__internal_parent_id"
        internal_reference_column = core_context.core.Column(internal_reference_column_name, namespace=onto_under_build)
        internal_reference_column.has_data_type = get_column_data_type({}, onto_under_build)  # that is a hack for string
        aggregate_table.has_columns.append(internal_reference_column)

        # Add Value Dependency to min
        internal_value_constrain = core_context.core.ValueDependency(f"Constraint.{internal_reference_column_name}", namespace=onto_under_build)
        internal_value_constrain.is_constraining_column = internal_reference_column
        # WARNING: You might not have referencing column in ontology yet, you have it here due to algorythm of discovery
        #          Make some functionality where you find any UNIQUE attribute
        # WARNING: Id attribute is hardcoded not passed from discovery
        internal_value_constrain.is_depending_on_column = onto_under_build.search_one(iri=f"*{parent_path}._id")
        table_min_constraint_group.has_constraints.append(internal_value_constrain)


    for full_column_name in table_meta_data:
        column_name = full_column_name[(len(table_meta_name)+1):]
        column_metadata = table_meta_data[full_column_name]

        if column_metadata["amount"] < ignorance_limit:
            skipped_count += 1
            skipped_list.append(full_column_name)
            continue

        if "type" in column_metadata and column_metadata["type"] in ['internal_reference']:
            # Make constrain reference into separate table << that can be done when all columns are done ...
            continue

        internal_reference_column = core_context.core.Column(full_column_name, namespace=onto_under_build)
        internal_reference_column.has_data_type = get_column_data_type(column_metadata, onto_under_build)

        # aggregate_table["has_columns"] = list()
        aggregate_table.has_columns.append(internal_reference_column)

        # Make Constrians
        column_constraint = core_context.core.FormatConstraint(f"Constraint.{full_column_name}")
        table_min_constraint_group.has_constraints.append(column_constraint)

        # 1. Is it unique ?? if set matches values << or close << or
        if len(column_metadata['values']) == len(column_metadata['values_set']) and "_id" in full_column_name:
            column_constraint.has_format_definition = ""

        # 2. Find list values
        # 3. Format if string <<
        # 4. Range if has min and max and number


    # for reference_constraints in internal_references
    # ValueDependency main_id referenced in child table

    # external references < discovery ...




    try:
        # sync_reasoner_hermit(infer_property_values=True)
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    except OwlReadyInconsistentOntologyError:
        err_filename = first_cook_batch_filename.replace(".owl", "_error.owl")
        with open(f"{err_filename}", mode="wb") as save_point:
            onto_under_build.save(file=save_point)
        exit(1)

    # sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)
    print(f"Skipped {skipped_count} columns for {table_meta_name} : {skipped_list[:30]}.")


with open(first_cook_batch_filename, mode="wb") as save_point:
    onto_under_build.save(file=save_point)

print("end")


# d = None
# with open(os.path.join(search_dir_path, "metadata_aggregation.json")) as json_data:
#     d = json.load(json_data)
#     json_data.close()
    # pprint(d)
# foo = ijson.basic_parse(open())
print("askdjfh")



