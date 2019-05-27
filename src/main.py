'''
File: main.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:39 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Monday, 27th May 2019 1:27:19 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from dirs import TREEBANKD
from ktbparse import KTBParser

if __name__ == "__main__":
    ktbparser = KTBParser()
    ktbparser.parse(TREEBANKD / 'aozora_Akutagawa-1922.psd')
    print("Done.")
    