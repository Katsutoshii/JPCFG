'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 3:12:06 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys
from tools.dirs import TREEBANKD, LARKD
from parsing import PCFG, KTBParser, LarkAdapter

# from parser import PCFG, KTBParser, LarkAdapter
sys.setrecursionlimit(2000)

if __name__ == "__main__":
    
    ktbparser = KTBParser()
    pcfg = PCFG()
    files = [
        TREEBANKD / 'aozora_Akutagawa-1922.psd',
    ]
    for file in files:
        for tree in ktbparser.parse(file):
            pcfg.train(tree)
    
    print("Starts:", pcfg.starts)

    # lark test
    la = LarkAdapter(pcfg)
    parse = la.parser.parse("トロッコ 1aozoraAkutagawa1922JP")
    print(parse)
    print("Done.")
