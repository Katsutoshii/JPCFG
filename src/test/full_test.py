'''
File: full_test.py
Project: test
File Created: Sunday, 2nd June 2019 4:37:20 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 2:43:30 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
import sys

from tools.dirs import keyaki_trees
from tools import log
from jparser import JapaneseParser

sys.setrecursionlimit(2000)

def full_test():
    total_r, total_p, total_f = 0, 0, 0
    files = keyaki_trees('aozora_A*')
    jparser = JapaneseParser()
    jparser.train(files)
    n = 0
    for i in range(11, 40):
        results = jparser.test(i)
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
    full_test()
    