import re
from typing import List, Dict

from generation_request.parser_fundamentals import QueryContext
from generation_request.parser_rules import GenerationRules, TableRealizationRules, WhereRules, SectionRulesBased


class GenerationRequestSyntaxParser:
    core = None
    schema_iri: str = None
    loaded_rules: Dict = dict()
    processors: List[SectionRulesBased] = None
    context: QueryContext = QueryContext()

    def __init__(self, loaded_onto):
        self.onto = loaded_onto
        self.core = self.onto.imported_ontologies[0]
        self.process_rule_classes()
        self.context.constraint_groups_heap = [self.core.QueryGroup(name="query_main_group", namespace=self.onto)]

    def process_rule_classes(self):
        self.processors = [
            GenerationRules(self.core, self.onto),
            TableRealizationRules(self.core, self.onto),
            WhereRules(self.core, self.onto)
        ]

    def deactivate_processors(self):
        for processor in self.processors:
            processor.is_active = False

    def process_line_by_processor(self, line_number, line, match_rule, processor) -> bool:
        """ This method processes line by rule and if it was matching the patter and actually processed it will return
        True otherwise False """
        pattern, callback = getattr(processor, match_rule)()
        match = re.search(pattern, line)
        if match:
            self.deactivate_processors()
            processor.is_active = True
            callback(line_number, line, match, self.context)
            return True
        return False

    def parse_line_by_processors(self, line_number, line):
        for processor in self.processors:
            sorted_match_rules = dir(processor)
            sorted_match_rules.sort()
            for match_rule in sorted_match_rules:
                if not match_rule.startswith("match"):
                    continue

                if not processor.is_active:
                    if match_rule == "match_section_template":
                        if self.process_line_by_processor(line_number, line, match_rule, processor):
                            return
                else:
                    # active processor rule
                    if self.process_line_by_processor(line_number, line, match_rule, processor):
                        return

    def parse_request_from_file(self, filename: str):
        """This method takes file name from which to read request"""
        file1 = open(filename, 'r')
        count = 0
        while True:
            count += 1
            line = file1.readline().strip()
            self.parse_line_by_processors(count, line)

            if not line:
                break
        # line = file1.readline().strip()
        # red_realization_case = self.core.RealizationCase(line)
        return self.context.peek_latest_group()

    def parse_request_query(self, request_query: str):
        """This method takes multiline string and parses line by line to create RealizationCase and
        returns RealizationCase uri."""
        pass
