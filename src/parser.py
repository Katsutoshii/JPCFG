'''
File: parser.py
Project: src
File Created: Saturday, 1st June 2019 11:26:22 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 1:39:20 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from pathlib import Path
from typing import List, Union

from parsing import PCFG, KTBParser, LarkAdapter, Tree
from segmenting import Segmenter

class JapaneseParser():
    # full parser class
    # performs both segmentation and grammar tagging
    def __init__(self):
        self.count = 0
        self.total = 10
        self.vocab = set()
        self.ktbparser = KTBParser()
        self.segmenter = Segmenter()
        self.pcfg = PCFG()
        self.larkadapter: LarkAdapter = None

        # for evaluation
        self.token_lists: List[List[str]] = []
        self.total_parse_accuracy = 0
        self.total_segment_accuracy = 0
        
    def train(self, files: List[Path]):
        # trains the parser on a list of files
        for _, file in enumerate(files):
            self.train_on_file(file)
            
        self.pcfg.calc_probs()
        self.larkadapter = LarkAdapter(self.pcfg)
            
    def train_on_file(self, file: Path):
        # trains the parser on a particular file
        print(f"Parsing file {file.stem}...")
        for i, tree in enumerate(self.ktbparser.parse(file)):
            self.count += 1
            if self.count > self.total:
                break
                
            tokens = self.ktbparser.tokens(tree)
            print(tokens)

            for token in tokens:
                self.vocab.add(token)
            self.segmenter.train(tokens)
            self.pcfg.train(tree)

            self.token_lists.append(tokens)
    
    def parse(self, text: Union[str, List[str]]) -> Tree:
        # parses text
        if isinstance(text, str):
            tokens = self.segmenter.segment(text)
        else:
            tokens = text

        larktree = self.larkadapter.parse(tokens)
        return Tree.fromlark(larktree)

    def test(self, text: str, true_tree: Tree) -> float:
        tokens = self.segmenter.segment(text)
        return self.larkadapter.test(tokens, true_tree)
