'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 5:14:59 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dirs import TREEBANKD, LARKD
from pcfg import PCFG
from ktbparse import KTBParser
from larkadapter import LarkAdapter

if __name__ == "__main__":
    ktbparser = KTBParser()
    pcfg = PCFG()
    files = [
        TREEBANKD / 'aozora_Akutagawa-1922.psd',
    ]
    for file in files:
        for tree in ktbparser.parse(file):
            pcfg.train(tree)
    
    print("Rules['PP']:", pcfg.prods('PP'))
    print("Starts:", pcfg.starts)

    # lark test
    la = LarkAdapter(pcfg)
    print("Done.")
