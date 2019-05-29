'''
File: larktest.py
Project: src
File Created: Wednesday, 29th May 2019 10:41:55 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Wednesday, 29th May 2019 10:58:35 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from dirs import LARKD
from lark import Lark
from lark.tree import pydot__tree_to_png    # Just a neat utility function

if __name__ == "__main__":
    gfile = LARKD / 'simple.lark'
    gstr = ""
    with open(gfile) as f:
        gstr = f.read()
    parser = Lark(gstr, start='sentence', ambiguity='explicit')
    expr = "fruit flies like bananas"
    tree = parser.parse(expr)
    print(tree)
    pydot__tree_to_png(tree, LARKD / "fruitflies.png")
