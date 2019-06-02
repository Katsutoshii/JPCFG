'''
File: larkadapter.py
Project: src
File Created: Wednesday, 29th May 2019 11:04:49 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 4:03:27 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from collections import OrderedDict
from typing import List, Set, Dict, Tuple, Optional
from copy import deepcopy

from lark import Lark
from lark.tree import pydot__tree_to_png    # Just a neat utility function
from lark.tree import Tree as LarkTree
from lark import UnexpectedCharacters

from .tree import Tree

from tools.dirs import LARKD, LARKIMGD, DATAD
from tools import f1, log

from .pcfg import PCFG, Rule, create_rule
from .disambig import Disambiguator


class LarkAdapter():
    
    def __init__(self, pcfg: PCFG):
        self.pcfg = pcfg
        self.savelark(LARKD / 'grammar.lark')
        
        log("Creating Lark Parser...")

        self.parser = Lark(
            self.larkstr(),
            start='sentence',
            ambiguity='explicit',
            parser='earley'
        )
        self.disambig = Disambiguator(self.pcfg)

    def rules_larkstr(self, lhs: str, rules: OrderedDict) -> str:
        # log("lhs", lhs)
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

    def test(self, tokens: List[str], true_tree: Tree, verbose: bool = False) \
            -> Optional[Tuple[float, float, float]]:
        larktree = self.parse(tokens)
        if larktree is None:
            return None
            
        if verbose:
            log("Pre disambiguation:")
            log(larktree.pretty())

        self.disambig.disambiguate(larktree)

        if verbose:
            log("Post disambiguation:")
            log(larktree.pretty())

        tree = Tree.fromlark(larktree)
        recall = self.calc_recall(tree, true_tree)
        precision = self.calc_precision(tree, true_tree)
        fscore = f1(recall, precision)

        if verbose:
            log(precision, recall, fscore)
            log()
        return recall, precision, fscore

    @staticmethod
    def calc_precision(tree: Tree, true_tree: Tree) -> float:
        true_ruleset: Set[Rule] = set()
        correct, total = 0, 0
        for node in true_tree.iterlevels():
            true_ruleset.add(create_rule(node))
            total += 1
        for node in tree.iterlevels():
            rule = create_rule(node)
            if rule in true_ruleset:
                correct += 1

        return correct / total
    
    @staticmethod
    def calc_recall(tree: Tree, true_tree: Tree) -> float:
        true_ruleset: Set[Rule] = set()
        correct, total = 0, 0
        for node in true_tree.iterlevels():
            true_ruleset.add(create_rule(node))
        for node in tree.iterlevels():
            rule = create_rule(node)
            if rule in true_ruleset:
                correct += 1
            total += 1

        return correct / total


    def parse(self, tokens: List[str]) -> Optional[LarkTree]:
        try:
            return self.parser.parse(" ".join(tokens))
        except UnexpectedCharacters:
            log("Lark does not support this sentence structure.")
            return None
