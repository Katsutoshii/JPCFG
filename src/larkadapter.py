'''
File: larkadapter.py
Project: src
File Created: Wednesday, 29th May 2019 11:04:49 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 11:13:47 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pcfg import PCFG, Rule
from dirs import LARKD

class LarkAdapter():
    def __init__(self, pcfg: PCFG):
        self.pcfg = pcfg

    def rule_larkstr(self, rule: Rule) -> str:
        return rule.lhs + ': ' + ' | '.join(rule.rhs)

    def to_larkstr(self) -> str:
        larkstr = ""
        for rule in self.pcfg.counts:
            larkstr += self.rule_larkstr(rule)
        larkstr += r"%import common.WS\n"
        larkstr += r"%ignore WS\n"
        return larkstr
