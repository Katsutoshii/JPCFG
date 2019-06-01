'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 11:04:48 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import Dict, List, Set
from collections import defaultdict, namedtuple, OrderedDict

from .tree import Tree


Rule = namedtuple("Rule", ["lhs", "rhs"])

def create_rule(node: Tree):
    lhs = node.data
    rhs = [c.data for c in node.children]
    return Rule(lhs, tuple(rhs))

class PCFG():
    def __init__(self):
        self.rules: Dict[str, OrderedDict] = defaultdict(OrderedDict)         # symbols to their rules
        self.counts: Dict[Rule, int] = defaultdict(int)             # rules to their counts
        self.terminals: Dict[str, OrderedDict] = defaultdict(OrderedDict)      # terminals to preterminals
        self.preterminals: Dict[str, OrderedDict] = defaultdict(OrderedDict)   # preterminals to terminals
        self.starts = set()                                         # all possible start variables

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
        self.rules[rule.lhs][rule] = None

    def add_terminal(self, rule: Rule) -> None:
        self.add(rule)
        self.terminals[rule.rhs[0]][rule.lhs] = None
        self.preterminals[rule.lhs][rule.rhs[0]] = None
