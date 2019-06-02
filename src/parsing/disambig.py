'''
File: disambig.py
Project: parsing
File Created: Sunday, 2nd June 2019 2:58:07 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 3:23:32 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from math import log2
from typing import Dict, Union
from lark.tree import Tree as LarkTree
from lark import Token

from .pcfg import PCFG, create_rule

class Disambiguator():
    def __init__(self, pcfg: PCFG):
        self.pcfg = pcfg
        self.best_choices: Dict[LarkTree, LarkTree] = {}

    def calc_probs_for_choices(self, tree: Union[LarkTree, Token]) -> float:
        if isinstance(tree, Token):
            rule = create_rule(tree)
            return log2(self.pcfg.probabilities[rule])

        # otherwise it's a LarkTree!
        # if ambiguous pick the best probability
        if tree.data == '_ambig':
            child_probs = [(c, self.calc_probs_for_choices(c)) for c in tree.children]
            def get_prob(child_prob):
                return child_prob[1]
            best_child, best_prob = max(child_probs, key=get_prob)
            self.best_choices[tree] = best_child
            return best_prob

        # otherwise we are unambiguous, just reutrn the sum of child probs
        return sum([self.calc_probs_for_choices(c) for c in tree.children])

    def disambiguate(self, tree: LarkTree):
        self.calc_probs_for_choices(tree)
        stack = [tree]
        while(stack):
            node = stack.pop()
            if isinstance(node, Token):
                continue
            for i, child in enumerate(node.children):
                if isinstance(child, Token):
                    continue
                if child.data == '_ambig':
                    # if we have an ambiguous child, splice in
                    # the choice we made for the best tree
                    node.children[i] = self.best_choices[child]
            stack += node.children
