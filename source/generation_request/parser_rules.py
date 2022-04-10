from generation_request.parser_fundamentals import QueryContext
from utils.utils import RealizationDefinitionException, QueryMissformatException


class SectionRulesBased:
    is_active = False
    core = None
    query_namespace = None

    def __init__(self, _core, _query_namespace):
        self.core = _core
        self.query_namespace = _query_namespace

    def match_section_template(self):
        pass


class GenerationRules(SectionRulesBased):
    parser_name = "first"

    def __init__(self, _core, _query_namespace):
        super().__init__(_core, _query_namespace)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            print(f"Here I am: {self.parser_name}")
            pass

        return "GENERATE .*", process_line


class TableRealizationRules(SectionRulesBased):

    def __init__(self, _core, _query_namespace):
        super().__init__(_core, _query_namespace)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            line = line.replace("FOR ", "")
            self.process_table_definition(line, query_context)

        return "^FOR .*", process_line

    def match_and_realizations(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            line = line.replace("AND ", "")
            self.process_table_definition(line, query_context)

        return "AND .*", process_line

    def process_table_definition(self, line: str, query_context: QueryContext):
        table_name, alias = line.split(" as ")
        realization_def = self.core.RealizationDefinition(
            name=f"rd_{alias}", namespace=self.query_namespace)
        table = self.query_namespace.search_one(iri=f"*{table_name}")
        if not table:
            raise RealizationDefinitionException(f"Could not find table: {table_name}")
        if alias in query_context.defined_realization:
            raise RealizationDefinitionException(f"There are multiple realization definitions with same alias: {alias}")
        query_context.defined_realization[alias] = (table, realization_def)


# Todo:
# 0. Implement regex - done
# 1. cope with operators and validation if not messing up - done
# 2. cope with groups - done
# 0. Range
# 5. Format dependency
# 0. Equal Dependencies
# 0. Greater Then Dependencies
# 0. Greater or Equal Then Dependencies
# 0. Smaller Then Dependencies
# 0. Smaller or Equal Then Dependencies
# 4. Restrictive constraints
# 3. No realization names
# 6. Tests for specific rules from query


class WhereRules(SectionRulesBased):

    def __init__(self, _core, _query_namespace):
        super().__init__(_core, _query_namespace)

    def match_section_template(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            print(f"INFO Where line: {line}")

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

    def set_realization_definition_and_column_from_target(self, build_constraint, target, query_context):
        realization_iri, column_name = self.parse_target(target)
        if realization_iri:
            table, realization_def = query_context.defined_realization[realization_iri]
            column = table.get_column_by_name(column_name)
            realization_def.has_constraints.append(build_constraint)
        else:
            column = self.core.search_one(iri=column_name)
        build_constraint.is_constraining_column = column

    def set_operator_to_latest_group(self, line_number, operator, query_context: QueryContext):
        if not operator:
            return

        if not query_context.is_new_group:
            if query_context.peek_latest_group().is_or_operator() and operator.strip() == "AND":
                raise QueryMissformatException(f"Mixed logical operators in line {line_number}")
            if query_context.peek_latest_group().is_and_operator() and operator.strip() == "OR":
                raise QueryMissformatException(f"Mixed logical operators in line {line_number}")

        query_context.is_new_group = False
        if query_context.peek_latest_group().is_or_operator() and operator.strip() == "AND":
            query_context.peek_latest_group().change_to_and_operator()
        if query_context.peek_latest_group().is_and_operator() and operator.strip() == "OR":
            query_context.peek_latest_group().change_to_or_operator()

    def match_01_or_and_list_constraint(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)

            list_constraint = self.core.ListConstraint(
                name=f"constraint_from_line_{line_number}", namespace=self.query_namespace)
            query_context.peek_latest_group().has_constraints.append(list_constraint)

            value_list = match["list_def"][1:-1].replace("'", "").replace(" ", "").split(",")
            list_constraint.has_picks = value_list

            self.set_realization_definition_and_column_from_target(list_constraint, match["target"], query_context)

        return "(?P<operator>(AND|OR) )?(?P<target>.*) IN (?P<list_def>.*)", process_line

    def match_02_or_and_regex_constraint(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)

            build_constraint = self.core.RegexConstraint(
                name=f"constraint_from_line_{line_number}", namespace=self.query_namespace)
            query_context.peek_latest_group().has_constraints.append(build_constraint)

            pattern = match["pattern"]
            build_constraint.has_regex_format = pattern

            self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)

        return "(?P<operator>(AND|OR) )?(?P<target>.*) MATCH \'(?P<pattern>.*)\'", process_line

    # def match_03_or_and_range_greater_constraint(self):
    #     def process_line(line_number: int, line: str, match, query_context: QueryContext):
    #         self.set_operator_to_latest_group(line_number, match["operator"], query_context)
    #         build_constraint = self.core.RangeConstraint(
    #             f"constraint_from_line_{line_number}",
    #             right_boundary=match["constant"],
    #             is_left_open=True)
    #         query_context.peek_latest_group().has_constraints.append(build_constraint)
    #         self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)
    #
    #     return "(?P<operator>(AND|OR) )?(?P<target>.*) > \'(?P<constant>.*)\'", process_line

    def match_04_or_and_range_greater_equal_constraint(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)
            build_constraint = self.core.RangeConstraint(f"constraint_from_line_{line_number}")
            query_context.peek_latest_group().has_constraints.append(build_constraint)
            self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)
            build_constraint.set_left_boundary(match["constant"], False)

        return "(?P<operator>(AND|OR) )?(?P<target>.*) >= \'(?P<constant>.*)\'", process_line

    def match_05_or_and_range_greater_constraint(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)
            build_constraint = self.core.RangeConstraint(f"constraint_from_line_{line_number}")
            query_context.peek_latest_group().has_constraints.append(build_constraint)
            self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)
            build_constraint.set_left_boundary(match["constant"], True)

        return "(?P<operator>(AND|OR) )?(?P<target>.*) > \'(?P<constant>.*)\'", process_line

    def match_06_or_and_range_smaller_equal_constraint(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)
            build_constraint = self.core.RangeConstraint(f"constraint_from_line_{line_number}")
            query_context.peek_latest_group().has_constraints.append(build_constraint)
            self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)
            build_constraint.set_right_boundary(match["constant"], False)

        return "(?P<operator>(AND|OR) )?(?P<target>.*) <= \'(?P<constant>.*)\'", process_line

    def match_07_or_and_range_smaller_constraint(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)
            build_constraint = self.core.RangeConstraint(f"constraint_from_line_{line_number}")
            query_context.peek_latest_group().has_constraints.append(build_constraint)
            self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)
            build_constraint.set_right_boundary(match["constant"], True)

        return "(?P<operator>(AND|OR) )?(?P<target>.*) < \'(?P<constant>.*)\'", process_line

    # def match_10_or_and_greater_constraint(self):
    #     def process_line(line_number: int, line: str, match, query_context: QueryContext):
    #         self.set_operator_to_latest_group(line_number, match["operator"], query_context)
    #
    #         build_constraint = self.core.GreaterThenDependency(
    #             name=f"constraint_from_line_{line_number}", namespace=self.query_namespace)
    #
    #         build_constraint.is_constraining_column = prepared_table_2.has_columns[2]
    #         build_constraint.is_depending_on_column = prepared_table.has_columns[3]
    #
    #         query_context.peek_latest_group().has_constraints.append(build_constraint)
    #
    #         pattern = match["pattern"]
    #         build_constraint.has_regex_format = pattern
    #
    #         self.set_realization_definition_and_column_from_target(build_constraint, match["target"], query_context)
    #
    #     return "(?P<operator>(AND|OR) )?(?P<target>.*) > \'(?P<constant>.*)\'", process_line

    def match_50_or_and_new_group(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            self.set_operator_to_latest_group(line_number, match["operator"], query_context)
            print(f"New group in line {line_number}")
            new_group = self.core.ConstraintGroup(
                name=f"query_group_from_line_{line_number}",
                namespace=self.query_namespace)
            query_context.peek_latest_group().contains_constraint_groups.append(new_group)
            query_context.push_new_group(new_group)
            query_context.is_new_group = True

        return "(?P<operator>(AND|OR) )?\\(", process_line

    def match_51_close_group(self):
        def process_line(line_number: int, line: str, match, query_context: QueryContext):
            print(f"Close group in line {line_number}")
            query_context.pop_latest_group()

        return "\)", process_line

    # def match_first_constraint(self):
    #     def process_line(line, query_group):
    #         line = line.replace("\t", "")
    #         line = line.replace("AND ", "")
    #         print(f"Constraint for parsing2: {line}")
    #
    #     return ".*", process_line
