'''
File: segment_test.py
Project: test
File Created: Saturday, 1st June 2019 2:24:01 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 1st June 2019 2:41:14 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from typing import List

from segmenting import Segmenter
from tools.dirs import TREEBANKD, LARKD, keyaki_trees
from tools.eval import calculate_accuracy
from parsing import KTBParser
sys.setrecursionlimit(2000)

def parse_test():
    ktbparser = KTBParser()

def simple_segment_test():
    test_tokens = ["the", "dog", "ate", "these", "foods", "se"]
    test_tokens2 = ["the", "dog", "ate", "the", "se", "foods", "se"]
    test_text = "".join(test_tokens)
    seg = Segmenter()

    for training_seq in [test_tokens, test_tokens2, test_tokens2, test_tokens2, test_tokens2, test_tokens2]:
        seg.train(training_seq)
        
    tokens = seg.segment(test_text)
    print(tokens)

def segment_test():
    ktbparser = KTBParser()
    seg = Segmenter()
    
    files = keyaki_trees('aozora*')
    
    token_lists = []
    texts = []

    for file in files:
        print(f"Parsing file {file.stem}...")
        
        for i, tree in enumerate(ktbparser.parse(file)):
            tokens = ktbparser.tokens(tree)
            print(tokens)
            seg.train(tokens)
            token_lists.append(tokens)
            texts.append("".join(tokens))
            
        break
    
    tokens = seg.segment(texts[-1])
    print(tokens)
