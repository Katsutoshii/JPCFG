'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 1st June 2019 12:04:21 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from typing import List

from tools.dirs import TREEBANKD, LARKD, keyaki_trees
from parsing import PCFG, KTBParser, LarkAdapter


# from parser import PCFG, KTBParser, LarkAdapter
sys.setrecursionlimit(2000)
total = 6
targets = {0, 1, 2, 3, 4, 5, 6}
if __name__ == "__main__":
    
    ktbparser = KTBParser()
    pcfg = PCFG()

    test_tokens_lists: List[List[str]] = []
    test_texts: List[str] = []
    
    # files = [
    #     next(keyaki_trees())
    # ]
    files = keyaki_trees('aozora*')
    # files = keyaki_trees('test')
    
    for file in files:
        
        count = 0
        print(f"Parsing file {file.stem}...")
        
        for tree in ktbparser.parse(file):
            count += 1
            if count > total:
                break
            if count not in targets:
                continue
            pcfg.train(tree)

            tokens = ktbparser.tokens(tree)
            text = "".join(tokens)

            test_tokens_lists.append(tokens)
            test_texts.append(text)
        break
    
    print("Starts:", pcfg.starts)

    # lark test
    la = LarkAdapter(pcfg)
    # for test_tokens in test_tokens_lists:
    for test_tokens in [test_tokens_lists[-1]]:
        test_spaced = u" ".join(test_tokens)
        print(test_spaced)
        parse = la.parser.parse(test_spaced)
        print(parse)
    print("Done.")
