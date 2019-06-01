'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 11:00:15 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import Dict, List, Set
from collections import defaultdict, namedtuple

from .tree import Tree


Rule = namedtuple("Rule", ["lhs", "rhs"])

def create_rule(node: Tree):
    lhs = node.data
    rhs = [c.data for c in node.children]
    return Rule(lhs, tuple(rhs))

class PCFG():
    def __init__(self):
        self.rules: Dict[str, List[Rule]] = defaultdict(list)         # symbols to their rules
        self.counts: Dict[Rule, int] = defaultdict(int)             # rules to their counts
        self.terminals: Dict[str, List[str]] = defaultdict(list)      # terminals to preterminals
        self.preterminals: Dict[str, List[str]] = defaultdict(list)   # preterminals to terminals
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
        self.rules[rule.lhs].append(rule)

    def add_terminal(self, rule: Rule) -> None:
        self.add(rule)
        self.terminals[rule.rhs[0]].append(rule.lhs)
        self.preterminals[rule.lhs].append(rule.rhs[0])
