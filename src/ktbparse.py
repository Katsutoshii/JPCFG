'''
File: ktbparse.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:36 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Tuesday, 28th May 2019 10:57:24 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import TextIO

from tree import Tree
from pcfg import PCFG, Rule

class KTBParser():
    def __init__(self):
        self.file: TextIO = None
        self.pcfg: PCFG = PCFG()
        self.treestr = ""

    @staticmethod
    def create_rule(node: Tree):
        lhs = node.data
        rhs = [c.data for c in node.children]
        return Rule(lhs, tuple(rhs))

    def parseline(self, line: str):
        line = line.strip()
        if not line:
            if not self.treestr:
                return
        
            # process all rules in this tree
            root = Tree.parse(self.treestr)
            for node in root.iteredges():
                rule = self.create_rule(node)
                self.pcfg.add(rule)

            # add all terminals and preterminals
            for node in root.leafedges():
                rule = self.create_rule(node)
                self.pcfg.add_terminal(rule)
            
            # save this root as a start
            self.pcfg.starts.add(root.data)

            self.treestr = ""
            return

        self.treestr += line
        
    def parse(self, file: Path):
        with open(file, encoding='utf8') as self.file:
            for line in self.file:
                self.parseline(line)
