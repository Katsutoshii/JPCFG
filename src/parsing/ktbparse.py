'''
File: ktbparse.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:36 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 4:33:35 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import TextIO, Iterator, List

from .tree import Tree


class KTBParser():
    START = 'sentence'
    def __init__(self):
        self.file: TextIO = None
        self.treestr = ""
        
    @staticmethod
    def replace_invalid(string: str) -> str:
        return string\
            .replace('-', '')\
            .replace('-', '')\
            .replace('_', '')\
            .replace(';', '')\
            .replace('+', '')\
            # .replace('*', 'nul')\
            # .replace('{', '')\
            # .replace('}', '')\
            # .replace('の', 'no')\
            # .replace('から', 'kara')\
            # .replace('へ', 'he')\
            # .replace('に', 'ni')

    @staticmethod
    def tokens(tree: Tree) -> List[str]:
        return [KTBParser.replace_invalid(node.data) for node in tree.iterleaves()]

    def parse(self, file: Path) -> Iterator[Tree]:
        with open(file, encoding='utf8') as self.file:
            for line in self.file:
                line = line.strip()
                if not line:
                    if not self.treestr:
                        continue
                    # process all rules in this tree
                    root = Tree.parse(self.treestr)
                    root.data = self.START

                    
                    # make all nonpreterminals lowercase
                    for node in root.iternonstems():
                        node.data = node.data.lower()
                        
                    # make all preterminals uppercase
                    for node in root.iterstems():
                        node.data = node.data.upper()

                    # make last replacements and ignore nulls
                    for node in root.iterlevels():
                        node.data = self.replace_invalid(node.data)
                        temp = False
                        for c in node.children:
                            if c.data in {'PRN', '*ICH*-1'}:
                                temp = True
                        if temp: print(node.children)
                        node.children = [c for c in node.children if '*' not in c.data]
                        if temp: 
                            print(node.children)
                            print()

                    yield root

                    self.treestr = ""
                    continue

                self.treestr += line
