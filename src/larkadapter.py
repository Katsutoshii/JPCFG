'''
File: larkadapter.py
Project: src
File Created: Wednesday, 29th May 2019 11:04:49 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 5:37:12 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import List

from lark import Lark
from lark.tree import pydot__tree_to_png    # Just a neat utility function

from pcfg import PCFG, Rule
from dirs import LARKD


class LarkAdapter():
    def __init__(self, pcfg: PCFG):
        self.pcfg = pcfg
        self.savelark(LARKD / 'test1.lark')
        self.parser = Lark(self.larkstr(), start='sentence', ambiguity='explicit')

    def rules_larkstr(self, lhs: str, rules: List[Rule]) -> str:
        return lhs + ': ' + \
            ' | '.join([' '.join(rule.rhs) for rule in rules 
                if rule not in self.pcfg.preterminals]) + \
            ' | '.join([f"\"{rule.rhs[0]}\"" for rule in rules
                if rule in self.pcfg.preterminals]) + \
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
