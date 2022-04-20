import os
from owlready2 import get_ontology, onto_path, sync_reasoner_pellet
from generation_request.parser_fundamentals import QueryContext
from utils.utils import RealizationDefinitionException, QueryMissformatException

from core_classes import DataTypes
from core_classes import SimpleExtensions
from core_classes import Constraints
from core_classes import Dependencies
from core_classes import ConstraintGroups
from core_classes import LogicalOperators
from core_classes import RealizationCase


class SectionRulesBased:
    is_active = False
    core = None
    query_context = None

    def __init__(self, context: QueryContext):
        self.query_context = context
        self.core = context.core

    def match_section_template(self):
        pass


class LoadOntologyRules(SectionRulesBased):

    def __init__(self, context: QueryContext):
        super().__init__(context)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match):
            print(f"INFO: Parsing line {line_number}: Using ontology: {match['schema_iri']}")
            # onto_path.append(f"{os.getcwd()}/resources/development/")
            onto_path.append(f"{os.getcwd()}/{self.query_context.load_location}")

            schema_onto = get_ontology(match["schema_iri"])
            schema_onto.load(only_local=True)
            self.query_context.schema_onto = schema_onto

            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=False)

            self.query_context.constraint_groups_heap.append(
                self.query_context.core.QueryGroup(name="query_main_group", namespace=self.query_context.schema_onto))

        return "USES \'(?P<schema_iri>.+?)\'", process_line


class GenerationRules(SectionRulesBased):

    def __init__(self, context: QueryContext):
        super().__init__(context)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match):
            print(f"INFO: Parsing line {line_number}: command {match['command']}")
            self.query_context.command = match["command"]

        return "GENERATE (?P<command>.+)", process_line


class TableRealizationRules(SectionRulesBased):

    def __init__(self, context: QueryContext):
        super().__init__(context)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match):
            line = line.replace("FOR ", "")
            self.process_table_definition(line)

        return "^FOR .*", process_line

    def match_and_realizations(self):
        def process_line(line_number: int, line: str, match):
            line = line.replace("AND ", "")
            self.process_table_definition(line)

        return "AND .*", process_line

    def process_table_definition(self, line: str):
        table_name, alias = line.split(" as ")
        realization_def = self.core.RealizationDefinition(
            name=f"rd_{alias}", namespace=self.query_context.schema_onto)
        table = self.query_context.schema_onto.search_one(iri=f"*{table_name}")
        if not table:
            raise RealizationDefinitionException(f"Could not find table: {table_name}")
        if alias in self.query_context.defined_realization:
            raise RealizationDefinitionException(f"There are multiple realization definitions with same alias: {alias}")
        self.query_context.defined_realization[alias] = (table, realization_def)


# Todo:
#  Implement regex - done
#  cope with operators and validation if not messing up - done
#  cope with groups - done
#  Range - done
#  Format dependency - done
#  Equal Dependencies - done
#  Greater Then Dependencies - done
#  Greater or Equal Then Dependencies - done
#  Smaller Then Dependencies - done
#  Smaller or Equal Then Dependencies - done
#  Restrictive constraints - done
#  Tests for specific rules from query - done
#  No realization names
#  Move to not single file
#  Cope with commands < slightly bigger architectural situation


class WhereRules(SectionRulesBased):

    def __init__(self, context: QueryContext):
        super().__init__(context)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match):
            print(f"INFO Starting WHERE section")

        return "WHERE", process_line

    def parse_target(self, target: str):
        number_of_dots = target.count(".")

        if number_of_dots == 1:
            realization, column = target.split(".")
            return realization, column

        if number_of_dots == 2:
            column_key_word, table, column = target.split(".")
            if column_key_word != "Column":
                raise Exception("If you have specified 3 part URI then it should be column.")
            return None, target

        raise Exception("Wrong number of dots.")

    def _set_realization_definition_and_column_from_target(self, build_constraint, target):
        realization_iri, column_name = self.parse_target(target)
        if realization_iri:
            table, realization_def = self.query_context.defined_realization[realization_iri]
            column = table.get_column_by_name(column_name)
            realization_def.has_constraints.append(build_constraint)
        else:
            column = self.core.search_one(iri=column_name)
        build_constraint.is_constraining_column = column

    def _build_constraint(self, line_number: int, line: str, match, constraint_init):
        self._set_operator_to_latest_group(line_number, match["operator"])
        appending_constraint = build_constraint = \
            constraint_init(f"constraint_from_line_{line_number}", namespace=self.query_context.schema_onto)
        if match["is_not"]:
            appending_constraint = build_constraint.toggle_restriction(f"restriction_from_line_{line_number}")
        self.query_context.peek_latest_group().has_constraints.append(appending_constraint)
        self._set_realization_definition_and_column_from_target(build_constraint, match["target"])
        return build_constraint

    def get_realization_and_column_from_dependent(self, dependent):
        realization_iri, column_name = self.parse_target(dependent)
        if realization_iri:
            table, realization_def = self.query_context.defined_realization[realization_iri]
            column = table.get_column_by_name(column_name)
            return realization_def, column
        else:
            # TODO: Test if dependencies without realization definition will work
            # TODO: Overall realization-definition-less query
            column = self.core.search_one(iri=column_name)
            return None, column

    def _set_dependent_realization_and_column_from_dependent(self, build_dependency, dependent):
        realization_def, column = self.get_realization_and_column_from_dependent(dependent)
        if not column:
            raise RealizationDefinitionException(f"Pointed dependent could not find column from {dependent}")
        build_dependency.is_depending_on_column = column

        if realization_def:
            build_dependency.is_depending_on_realization = realization_def

    def _set_operator_to_latest_group(self, line_number, operator):
        if not operator:
            return

        if not self.query_context.is_new_group:
            if self.query_context.peek_latest_group().is_or_operator() and operator.strip() == "AND":
                raise QueryMissformatException(f"Mixed logical operators in line {line_number}")
            if self.query_context.peek_latest_group().is_and_operator() and operator.strip() == "OR":
                raise QueryMissformatException(f"Mixed logical operators in line {line_number}")

        self.query_context.is_new_group = False
        if self.query_context.peek_latest_group().is_or_operator() and operator.strip() == "AND":
            self.query_context.peek_latest_group().change_to_and_operator()
        if self.query_context.peek_latest_group().is_and_operator() and operator.strip() == "OR":
            self.query_context.peek_latest_group().change_to_or_operator()

    def match_01_or_and_list_constraint(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.ListConstraint)
            build_constraint.has_picks = match["list_def"][1:-1].replace("'", "").replace(" ", "").split(",")

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? IN (?P<list_def>.*)", process_line

    def match_02_or_and_regex_constraint(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.RegexConstraint)
            build_constraint.has_regex_format = match["pattern"]

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? MATCH \'(?P<pattern>.+)\'", process_line

    def match_04_or_and_range_greater_equal_constraint(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.RangeConstraint)
            build_constraint.set_left_boundary(match["constant"], False)

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? >= \'(?P<constant>.+)\'", process_line

    def match_05_or_and_range_greater_constraint(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.RangeConstraint)
            build_constraint.set_left_boundary(match["constant"], True)

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? > \'(?P<constant>.+)\'", process_line

    def match_06_or_and_range_smaller_equal_constraint(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.RangeConstraint)
            build_constraint.set_right_boundary(match["constant"], False)

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? <= \'(?P<constant>.+)\'", process_line

    def match_07_or_and_range_smaller_constraint(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.RangeConstraint)
            build_constraint.set_right_boundary(match["constant"], True)

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? < \'(?P<constant>.+)\'", process_line

    """                                                         """
    """-------------------  DEPENDENCIES  ----------------------"""
    """                                                         """

    def match_10_or_and_format_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.FormatDependency)
            build_constraint.has_format_definition = match["format"]

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? FORMAT \'(?P<format>.+)\'", process_line

    def match_11_or_and_equal_word_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.ValueDependency)
            self._set_dependent_realization_and_column_from_dependent(
                build_constraint, match["dependent"])

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? EQUAL (?P<dependent>.+)", process_line

    def match_12_or_and_equal_sign_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.ValueDependency)
            self._set_dependent_realization_and_column_from_dependent(
                build_constraint, match["dependent"])

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? = (?P<dependent>.+)", process_line

    def match_13_or_and_smaller_then_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.SmallerThenDependency)
            self._set_dependent_realization_and_column_from_dependent(
                build_constraint, match["dependent"])

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? < (?P<dependent>.+)", process_line

    def match_14_or_and_smaller_or_equal_then_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.SmallerOrEqualThenDependency)
            self._set_dependent_realization_and_column_from_dependent(
                build_constraint, match["dependent"])

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? <= (?P<dependent>.+)", process_line

    def match_15_or_and_greater_then_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.GreaterThenDependency)
            self._set_dependent_realization_and_column_from_dependent(
                build_constraint, match["dependent"])

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? > (?P<dependent>.+)", process_line

    def match_16_or_and_greater_or_equal_then_dependency(self):
        def process_line(line_number: int, line: str, match):
            build_constraint = self._build_constraint(line_number, line, match, self.core.GreaterOrEqualThenDependency)
            self._set_dependent_realization_and_column_from_dependent(
                build_constraint, match["dependent"])

        return "(?P<operator>(AND|OR) )?(?P<target>.+?)(?P<is_not> NOT)? >= (?P<dependent>.+)", process_line

    def match_50_or_and_new_group(self):
        def process_line(line_number: int, line: str, match):
            self._set_operator_to_latest_group(line_number, match["operator"])
            print(f"New group in line {line_number}")
            new_group = self.core.ConstraintGroup(
                name=f"query_group_from_line_{line_number}",
                namespace=self.query_context.schema_onto)
            self.query_context.peek_latest_group().contains_constraint_groups.append(new_group)
            self.query_context.push_new_group(new_group)
            self.query_context.is_new_group = True

        return "(?P<operator>(AND|OR) )?\\(", process_line

    def match_51_close_group(self):
        def process_line(line_number: int, line: str, match):
            print(f"Close group in line {line_number}")
            self.query_context.pop_latest_group()

        return "\)", process_line
