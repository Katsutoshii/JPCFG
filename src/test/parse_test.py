'''
File: parse_test.py
Project: test
File Created: Saturday, 1st June 2019 2:23:28 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 2:58:32 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from typing import List
from tools.dirs import TREEBANKD, LARKD, keyaki_trees
from tools import log
from parsing import PCFG, KTBParser, LarkAdapter, Tree

# from parser import PCFG, KTBParser, LarkAdapter
sys.setrecursionlimit(2000)
total = 100000
targets = {0, 1, 2, 3, 4, 5, 6}

def parse_test():
    total_r, total_p, total_f = 0, 0, 0
    ktbparser = KTBParser()
    pcfg = PCFG()

    test_tokens_lists: List[List[str]] = []
    test_texts: List[str] = []
    trees = []
    
    files = keyaki_trees('aozora_A*')
    # files = keyaki_trees('test')
    
    for _, file in enumerate(files):
        
        count = 0
        print(f"Parsing file {file.stem}...")
        
        for i, tree in enumerate(ktbparser.parse(file)):
            count += 1
            if count > total:
                break
            if count not in targets:
            #     continue
                pass

            pcfg.train(tree)

            tokens = ktbparser.tokens(tree)
            text = "".join(tokens)

            test_tokens_lists.append(tokens)
            test_texts.append(text)
            trees.append(tree)

    # lark test
    pcfg.calc_probs()
    la = LarkAdapter(pcfg)
    n = 0
    for i, test_tokens in enumerate(test_tokens_lists):
    # for i, test_tokens in enumerate([test_tokens_lists[-1]]):
        results = la.test(test_tokens, trees[i], verbose=True)
        if results is not None:
            prec, rcll, fscore = results
            total_p += prec
            total_r += rcll
            total_f += fscore
            n += 1
            
    log("Averages (p, r, f):")
    log(total_p / n, total_r / n, total_f / n)
    log("Done.")

if __name__ == "__main__":
    parse_test()
