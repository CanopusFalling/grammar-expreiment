# Script to generate all the possible strings in a grammar up to a certain search depth.
# By Samuel Kent, August 2021

# ===== Imports =====
import re

# ===== Constants =====
ARROW_SEPERATOR = " -> "
RULE_DELIMETER = " | "


class Grammar:
    """Represents a context free grammar.

    Attributes:
        rules: A list of the Rule class to represent all the rules within the 
        grammar.
    """

    def __init__(self, rules=None, string_rules=None):
        """Inits Grammar.

        Uses either the `rules` or `string_rules` argument but one of the two 
        must be set. If both are set, string_rules is used.

        Args:
            rules: List of Rule objects
            string_rules: List of string representation of rules.
        """
        if string_rules is not None:
            self.rules = Grammar.__strings_to_rules(string_rules)
        elif rules is not None:
            self.rules = rules
        else:
            raise GrammarError("No rules supplied.")

    def __repr__(self):
        return "Grammar(rules={})".format(self.rules.__repr__())

    def possible_strings(self, search_depth, root=None):
        """Searches grammar for valid sentences.

        Searches for all the possible sentences within the grammar from the 
        `root` up to the `search_depth`.

        Args:
            search_depth: The depth of the search.
            root: The initial sentence that the search starts at, if not given
            then a root containing all the symbols from the rules is used.

        Returns:
            List of all the sentences that contain only terminals.
        """
        if root is None:
            root = self.__default_root()

        levels = [[root]]

        for i in range(search_depth):
            level_strings = []

            for node in levels[-1]:
                level_strings.extend(self.get_children(node))

            levels.append(level_strings)

        all_nodes = []
        [all_nodes.extend(x) for x in levels]

        rule_symbols = self.__get_symbols()
        return list(filter((lambda a: bool([x for x in rule_symbols if x not in a])), all_nodes))

    def __default_root(self):
        return "".join(self.__get_symbols())

    def __get_symbols(self):
        rule_symbols = []
        for rule in self.rules:
            rule_symbols.append(rule.symbol)
        return rule_symbols

    def get_children(self, node):
        """Get child sentences within a grammar.

        From the input sentence it finds all the "children", which are the 
        sentences achievable with only 1 opperation.

        Args:
            node: The sentence to find the children of.

        Returns:
            List of all the child sentences.
        """
        children = []

        for rule in self.rules:
            children.extend(rule.get_children(node))

        return children

    @staticmethod
    def __strings_to_rules(strings):
        return [Rule(string=x) for x in strings]


class Rule:
    """ Represents a rule in a context free grammar.

    Attributes:
        symbol: The nonterminal to represent the rule.
        patterns: List of patterns that the rule nonterminal can be 
        replaced with.
    """
    def __init__(self, symbol=None, patterns=None, string=None):
        """ Inits Rule

        Args:
            symbol: The nonterminal to represent the rule.
            patterns: List of patterns that the rule nonterminal can be 
            replaced with.
            string: A string representation of the rule. Example: 
            `A -> 0 | 1 | 0A | 1A`
        """
        if string is not None:
            symbol, patterns = Rule.__string_to_rule_info(string)

        self.symbol = symbol
        self.patterns = patterns

    def __repr__(self):
        return "Rule('{}', {})".format(self.symbol, self.patterns)

    def get_children(self, node):
        """Get child sentences for the rule

        From the input sentence finds all the possible sentences from 1 
        application of the rule.

        Args:
            node: The sentence to find the children of.

        Returns:
            List of all the child sentences.
        """
        symbol_count = len(re.findall(self.symbol, node))
        children = []

        for i in range(symbol_count):
            for pattern in self.patterns:
                children.append(Rule.__replace_nth_substring(
                    node, self.symbol, pattern, i))

        return children

    @staticmethod
    def __replace_nth_substring(string, substring, replacement_string, n):
        *splits, tail = string.split(substring, n+1)
        return replacement_string.join([substring.join(splits), tail])

    @staticmethod
    def __string_to_rule(string):
        symbol, patterns = Rule.__string_to_rule_info(string)
        return Rule(symbol=symbol, patterns=patterns)

    @staticmethod
    def __string_to_rule_info(string):
        symbol, patterns = string.split(ARROW_SEPERATOR)
        patterns = patterns.split(RULE_DELIMETER)
        return symbol, patterns


class GrammarError(Exception):
    pass


if __name__ == "__main__":
    grammar_string = ["A -> 0 | 1 | 0A | 1A"]
    grammar = Grammar(string_rules=grammar_string)
    print(grammar.possible_strings(3))
