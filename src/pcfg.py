'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 5:10:11 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from tree import Tree
from typing import Dict, List, Set
from collections import defaultdict, namedtuple

Rule = namedtuple("Rule", ["lhs", "rhs"])

def create_rule(node: Tree):
    lhs = node.data
    rhs = [c.data for c in node.children]
    return Rule(lhs, tuple(rhs))

class PCFG():
    def __init__(self):
        self.rules: Dict[str, Set[Rule]] = defaultdict(set)         # symbols to their rules
        self.counts: Dict[Rule, int] = defaultdict(int)             # rules to their counts
        self.preterminals: Dict[str, Set[str]] = defaultdict(set)   # terminals to preterminals
        self.starts = set()                                         # all possible start variables

    def train(self, tree: Tree):
        for node in tree.iteredges():
            rule = create_rule(node)
            self.add(rule)

        # add all terminals and preterminals
        for node in tree.leafedges():
            rule = create_rule(node)
            self.add_terminal(rule)
        
        # save this root as a start
        self.starts.add(tree.data)
        
    def add(self, rule: Rule) -> None:
        self.counts[rule] += 1
        self.rules[rule.lhs].add(rule)

    def add_terminal(self, rule: Rule) -> None:
        self.preterminals[rule.rhs[0]].add(rule.lhs)

    def prods(self, lhs: str) -> Set[Rule]:
        return self.rules[lhs]
