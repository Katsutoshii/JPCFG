'''
File: larkadapter.py
Project: src
File Created: Wednesday, 29th May 2019 11:04:49 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 3:29:35 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from collections import OrderedDict
from typing import List, Set, Dict, Tuple
from copy import deepcopy

from lark import Lark
from lark.tree import pydot__tree_to_png    # Just a neat utility function
from lark.tree import Tree as LarkTree
from lark import UnexpectedCharacters

from .tree import Tree

from tools.dirs import LARKD, LARKIMGD

from .pcfg import PCFG, Rule
from .disambig import Disambiguator


class LarkAdapter():
    def __init__(self, pcfg: PCFG):
        self.pcfg = pcfg
        self.savelark(LARKD / 'grammar.lark')
        self.parser = Lark(
            self.larkstr(),
            start='sentence',
            ambiguity='explicit',
            parser='earley'
        )
        self.disambig = Disambiguator(self.pcfg)

    def rules_larkstr(self, lhs: str, rules: OrderedDict) -> str:
        # print("lhs", lhs)
        is_preterminal = lhs in self.pcfg.preterminals
        return lhs + ': ' + \
            ' | '.join(
                [' '.join(
                    [f"\"{p}\"" for p in rule.rhs]
                    if is_preterminal else rule.rhs
                ) for rule in rules]
            ) + \
            '\n'
        
    def larkstr(self) -> str:
        larkstr = ""
        for lhs, rules in self.pcfg.rules.items():
            larkstr += self.rules_larkstr(lhs, rules)
        larkstr += "%import common.WS\n"
        larkstr += "%ignore WS\n"
        return larkstr

    def savelark(self, file: Path):
        with open(file, 'w', encoding='utf8') as f:
            f.write(self.larkstr())

    def test(self, tokens: List[str], true_tree: Tree, verbose: bool = False) -> float:
        larktree = self.parse(tokens)
        if verbose:
            print(larktree.pretty())
            
        # larktree = self.pcfg.get_best_ambiguous(larktree)
        self.disambig.disambiguate(larktree)
        if verbose:
            print(larktree.pretty())
        tree = Tree.fromlark(larktree)
        accuracy = self.calc_accuracy(tree, true_tree)
        return accuracy

    @staticmethod
    def calc_accuracy(tree: Tree, true_tree: Tree) -> float:
        tree_stems, true_stems = tree.stems(), true_tree.stems()
        correct, total = 0, 0
        for i, (terminal, preterm) in enumerate(tree_stems):
            true_term, true_preterm = tree_stems[i]
            if preterm.data == true_preterm.data:
                correct += 1
            total += 1

        return correct / total

    def parse(self, tokens: List[str]) -> LarkTree:
        try:
            return self.parser.parse(" ".join(tokens))
        except UnexpectedCharacters:
            print("Lark does not support this sentence structure.")
            return LarkTree('Error.', [])
