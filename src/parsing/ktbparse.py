'''
File: ktbparse.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:36 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 3:11:49 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import TextIO

from .tree import Tree
from .pcfg import PCFG, Rule

class KTBParser():
    START = 'sentence'
    def __init__(self):
        self.file: TextIO = None
        self.treestr = ""
        
    @staticmethod
    def replace_invalid(string: str) -> str:
        return string.\
            replace('-', '').\
            replace('_', '').\
            replace(';', '').\
            replace('*', 'a')

    def parse(self, file: Path):
        with open(file, encoding='utf8') as self.file:
            for line in self.file:
                line = line.strip()
                if not line:
                    if not self.treestr:
                        continue
                    # process all rules in this tree
                    root = Tree.parse(self.treestr, transform=self.replace_invalid)
                    root.data = self.START
                    yield root

                    self.treestr = ""
                    continue

                self.treestr += line
