'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 1st June 2019 12:47:49 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from typing import List
from pprint import pprint
from tools.dirs import TREEBANKD, LARKD, keyaki_trees
from parsing import PCFG, KTBParser, LarkAdapter, Tree


# from parser import PCFG, KTBParser, LarkAdapter
sys.setrecursionlimit(2000)
total = 100000
targets = {0, 1, 2, 3, 4, 5, 6}
if __name__ == "__main__":
    
    ktbparser = KTBParser()
    pcfg = PCFG()

    test_tokens_lists: List[List[str]] = []
    test_texts: List[str] = []
    
    files = keyaki_trees('aozora*')
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
        break
    
    print("Starts:", pcfg.starts)

    # lark test
    la = LarkAdapter(pcfg)
    for test_tokens in test_tokens_lists:
    # for test_tokens in [test_tokens_lists[-1]]:
        test_spaced = u" ".join(test_tokens)
        print(test_spaced)
        try:
            parse = la.parser.parse(test_spaced)
            tree = Tree.fromlark(parse)
            pprint(tree)
        except Exception as e:
            print("Lark error.")
            pass
    print("Done.")
