'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Tuesday, 28th May 2019 10:57:13 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import Dict, List, Set
from collections import defaultdict, namedtuple

Rule = namedtuple("Rule", ["lhs", "rhs"])

class PCFG():
    def __init__(self):
        self.rules: Dict[str, Set[Rule]] = defaultdict(set)         # symbols to their rules
        self.counts: Dict[Rule, int] = defaultdict(int)             # rules to their counts
        self.preterminals: Dict[str, Set[str]] = defaultdict(set)   # terminals to preterminals
        self.starts = set()                                         # all possible start variables

    def add(self, rule: Rule) -> None:
        self.counts[rule] += 1
        self.rules[rule.lhs].add(rule)

    def add_terminal(self, rule: Rule) -> None:
        self.preterminals[rule.rhs[0]].add(rule.lhs)

    def prods(self, lhs: str) -> Set[Rule]:
        return self.rules[lhs]
