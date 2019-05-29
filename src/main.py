'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 4:20:03 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dirs import TREEBANKD
from ktbparse import KTBParser
from larkadapter import LarkAdapter

if __name__ == "__main__":
    ktbparser = KTBParser()
    ktbparser.parse(TREEBANKD / 'aozora_Akutagawa-1922.psd')
    print(ktbparser.pcfg.prods('PP'))
    print("Done.")
