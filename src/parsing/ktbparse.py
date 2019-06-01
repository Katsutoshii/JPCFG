'''
File: ktbparse.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:36 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 1st June 2019 2:34:58 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import TextIO, Iterator, List

from .tree import Tree


class KTBParser():
    START = 'sentence'
    IGNORE = {
        'ID',
        'NP-SBJ',
        'NP-OB1',
        'SCON',
        'NP-LOC'
        # 'NP;*SBJ*',
    }
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
            .replace('*', 'n')\
            .replace('{', '')\
            .replace('}', '')\

    @staticmethod
    def replace_invalid_nt(string: str) -> str:
        return KTBParser.replace_invalid(string)\
            .replace('の', 'no')\
            .replace('から', 'kara')\
            .replace('へ', 'he')\
            .replace('に', 'ni')

    @staticmethod
    def tokens(tree: Tree) -> List[str]:
        return [KTBParser.replace_invalid(node.data) for node in tree.iterleaves()]

    @staticmethod
    def process(tree: Tree):
        tree.data = KTBParser.START
        
        # make last replacements and ignore nulls
        for node in tree.iterlevels():
            node.children = [
                c for c in node.children 
                if c.data not in KTBParser.IGNORE
            ]
            # node.children = [c for c in node.children if '*' not in c.data]

        # remove all id rules:
        # make all nonpreterminals lowercase
        for node in tree.iternonstems():
            node.data = KTBParser.replace_invalid_nt(node.data)
            node.data = node.data.lower()
            
        # make all preterminals uppercase
        for node in tree.iterstems():
            node.data = KTBParser.replace_invalid(node.data)
            node.data = node.data.upper()

        for node in tree.iterleaves():
            node.data = KTBParser.replace_invalid(node.data)
            
    def parse(self, file: Path) -> Iterator[Tree]:
        with open(file, encoding='utf8') as self.file:
            for line in self.file:
                line = line.strip()
                if not line:
                    if not self.treestr:
                        continue
                    # process all rules in this tree
                    tree = Tree.parse(self.treestr)
                    
                    self.process(tree)
                    yield tree

                    self.treestr = ""
                    continue

                self.treestr += line
        try:
            # process all rules in the last tree
            tree = Tree.parse(self.treestr)
            
            self.process(tree)
            yield tree
        except Exception as e:
            print(e)
