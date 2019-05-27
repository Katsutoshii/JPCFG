'''
File: ktbparse.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:36 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 27th May 2019 1:30:05 am
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

    def parseline(self, line: str):
        line = line.strip()
        if not line:
            if not self.treestr:
                return
            
            # process the treestr, then reset
            tree = Tree.parse(self.treestr)
            for parent, children in tree.iteredges():
                lhs = parent.data
                rhs = [c.data for c in children]
                rule = Rule(lhs, tuple(rhs))
                self.pcfg.counts[rule] += 1
            self.treestr = ""
            return
        self.treestr += line
        
    def parse(self, file: Path):
        with open(file, encoding='utf8') as self.file:
            for line in self.file:
                self.parseline(line)
