'''
File: ktbparse.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:36 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 5:31:06 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import TextIO

from tree import Tree
from pcfg import PCFG, Rule

class KTBParser():
    START = 'START'
    def __init__(self):
        self.file: TextIO = None
        self.treestr = ""
        
    @staticmethod
    def replace_hyph(string: str) -> str:
        return string.replace('-', '_')

    def parse(self, file: Path):
        with open(file, encoding='utf8') as self.file:
            for line in self.file:
                line = line.strip()
                if not line:
                    if not self.treestr:
                        continue
                    # process all rules in this tree
                    root = Tree.parse(self.treestr, transform=self.replace_hyph)
                    root.data = self.START
                    yield root
                    self.treestr = ""
                    continue

                self.treestr += line
