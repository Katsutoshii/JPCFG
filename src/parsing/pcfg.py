'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 12:40:11 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from math import log2
from typing import Dict, List, Set, Union, Tuple
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
        self.rules[rule.lhs][rule] = None

    def add_terminal(self, rule: Rule) -> None:
        self.add(rule)
        self.terminals[rule.rhs[0]][rule.lhs] = None
        self.preterminals[rule.lhs][rule.rhs[0]] = None

    def calc_probs(self):
        for rule in self.rules.values():
            self.probabilities[rule] = self.counts[rule] / self.counts[rule.lhs]
            
    def get_best_ambiguous(self, tree: Tree):
        path = []
        prob = 0.0
        num_ambig = 0
        path_probs: Dict[Tuple, float] = {}

        for node in tree.iterlevels():
            if node.data == '_ambig':
                num_ambig += 1
                for child in node.children:
                    path.append(child)
                    curr_path = tuple(path)
                    # pick this path if we haven't taken it yet
                    if curr_path not in path_probs:
                        path_probs[curr_path] = prob
                        break
                    del path[-1]
            else:
                rule = create_rule(node)
                prob += log2(self.probabilities[rule])

        # if no ambiguity, just return the prob
        if not path:
            return prob

        # otherwise find the best path
        def get_prob(path):
            return path_probs[path]
        best_path = max(path_probs, key=get_prob)
        return best_path
    
    @staticmethod
    def disambiguate(tree: Tree, choices: Tuple[str, ...]):
        pass
