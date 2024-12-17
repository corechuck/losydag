import re
from typing import List, Dict

from core_classes.ConstraintGroups import ConstraintGroup
from generation_request.parser_fundamentals import QueryContext
from generation_request.parser_rules import LoadOntologyRules, GenerationRules, TableRealizationRules, \
    WhereRules, SectionRulesBased
import utils.context


class GenerationRequestSyntaxParser:
    core = None
    schema_iri: str = None
    loaded_rules: Dict = dict()
    processors: List[SectionRulesBased] = None
    context: QueryContext = None

    def __init__(self, load_location):
        self.context = QueryContext(load_location)
        self.context.core = utils.context.core_context.core
        self.define_processors()

    def __del__(self):
        print("sdjkf")
        pass

    def define_processors(self):
        self.processors = [
            LoadOntologyRules(self.context),
            GenerationRules(self.context),
            TableRealizationRules(self.context),
            WhereRules(self.context)
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
            callback(line_number, line, match)
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

    def parse_request_from_file(self, filename: str) -> ConstraintGroup:
        """This method takes file name from which to read request"""
        file1 = open(filename, 'r', encoding="UTF-8")
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
