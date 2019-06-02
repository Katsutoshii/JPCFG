'''
File: segment_test.py
Project: test
File Created: Saturday, 1st June 2019 2:24:01 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 2:28:53 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from typing import List

from segmenting import Segmenter
from tools.dirs import TREEBANKD, LARKD, keyaki_trees
from tools import log
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
    total_r, total_p, total_f = 0, 0, 0
    ktbparser = KTBParser()
    seg = Segmenter()
    test_ids = set(range(10, 20))
    
    files = keyaki_trees('aozora_A*')
    
    token_lists = []
    texts = []

    for file in files:
        print(f"Parsing file {file.stem}...")
        
        for i, tree in enumerate(ktbparser.parse(file)):
            tokens = ktbparser.tokens(tree)
            
            token_lists.append(tokens)
            texts.append("".join(tokens))
            seg.train(tokens)
    
    for i in test_ids:
        prec, rcll, fscore = seg.test(texts[i], token_lists[i], verbose=True)
        total_p += prec
        total_r += rcll
        total_f += fscore
    
    n = len(test_ids)
    log("Averages (p, r, f):")
    log(total_p / n, total_r / n, total_f / n)
    log("Done.")
    # tests = [
    #     ("私は子供がいる", ["私", "は", "子供", "が", "い", "る"]),
    # ]
    # for test in tests:
    #     acc = seg.test(test[0], test[1])
    #     print(acc)

if __name__ == "__main__":
    segment_test()
