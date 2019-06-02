'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 3:00:16 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from math import log2
from typing import Dict, List, Set, Union, Tuple
from collections import defaultdict, namedtuple, OrderedDict
from lark import Token
from lark.tree import Tree as LarkTree

from .tree import Tree


Rule = namedtuple("Rule", ["lhs", "rhs"])

def create_rule(node: Union[Tree, LarkTree, Token]):
    # creates a rule based on a tree node
    lhs = node.type if isinstance(node, Token) else node.data
    rhs = [str(node)] if isinstance(node, Token) else \
        [c.type if isinstance(c, Token) else c.data
         for c in node.children]
    return Rule(lhs, tuple(rhs))

class PCFG():
    def __init__(self):
        self.rules: Dict[str, OrderedDict] = defaultdict(OrderedDict)         # symbols to their rules
        self.counts: Dict[Union[Rule, str], int] = defaultdict(int)             # rules to their counts
        self.terminals: Dict[str, OrderedDict] = defaultdict(OrderedDict)      # terminals to preterminals
        self.preterminals: Dict[str, OrderedDict] = defaultdict(OrderedDict)   # preterminals to terminals
        self.starts = set()                                         # all possible start variables
        self.probabilities: Dict[Rule, float] = {}

    def train(self, tree: Tree):
        # problem: symbols that were nonterminals are getting recreated as preterminals
        
        # add all nonpreterminals
        for node in tree.iternonstems():
            rule = create_rule(node)
            self.add(rule)

        # add all preterminals
        for node in tree.iterstems():
            rule = create_rule(node)
            self.add_terminal(rule)
        
        # save this root as a start
        self.starts.add(tree.data)

    def add(self, rule: Rule) -> None:
        self.counts[rule] += 1
        self.counts[rule.lhs] += 1
        self.rules[rule.lhs][rule] = None

    def add_terminal(self, rule: Rule) -> None:
        self.add(rule)
        self.terminals[rule.rhs[0]][rule.lhs] = None
        self.preterminals[rule.lhs][rule.rhs[0]] = None

    def calc_probs(self):
        for ruleset in self.rules.values():
            for rule in ruleset:
                self.probabilities[rule] = self.counts[rule] / self.counts[rule.lhs]
    