'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 4:07:58 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from typing import List

from tools.dirs import TREEBANKD, LARKD, keyaki_trees
from parsing import PCFG, KTBParser, LarkAdapter


# from parser import PCFG, KTBParser, LarkAdapter
sys.setrecursionlimit(2000)

if __name__ == "__main__":
    
    ktbparser = KTBParser()
    pcfg = PCFG()

    test_tokens_lists: List[List[str]] = []
    test_texts: List[str] = []
    
    # files = [
    #     next(keyaki_trees())
    # ]
    files = keyaki_trees('aozora*')
    for file in files:
        print(f"Parsing file {file.stem}...")
        for tree in ktbparser.parse(file):
            pcfg.train(tree)

        tokens = ktbparser.tokens(tree)
        text = "".join(tokens)

        test_tokens_lists.append(tokens)
        test_texts.append(text)
        break
    
    print("Starts:", pcfg.starts)

    # lark test
    la = LarkAdapter(pcfg)
    test_spaced = " ".join(test_tokens_lists[0])
    parse = la.parser.parse(test_spaced)
    print(parse)
    print("Done.")
