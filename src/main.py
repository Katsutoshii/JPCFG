'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Thursday, 30th May 2019 11:15:26 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from dirs import TREEBANKD, LARKD
from pcfg import PCFG
from ktbparse import KTBParser
from larkadapter import LarkAdapter

if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    ktbparser = KTBParser()
    pcfg = PCFG()
    files = [
        TREEBANKD / 'aozora_Akutagawa-1922.psd',
    ]
    for file in files:
        for tree in ktbparser.parse(file):
            pcfg.train(tree)
    
    # print("Rules['PP']:", pcfg.prods('PP'))
    print("Starts:", pcfg.starts)

    # lark test
    la = LarkAdapter(pcfg)
    parse = la.parser.parse("トロッコ 1aozoraAkutagawa1922JP")
    print(parse)
    print("Done.")
