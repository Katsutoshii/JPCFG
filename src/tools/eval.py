'''
File: eval.py
Project: tools
File Created: Saturday, 1st June 2019 1:11:12 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 1st June 2019 1:40:23 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from parsing import Tree

# Multiple measures: Labeled recall (LR):
# num of correct constituents in hyp. parse / num of constituents in reference parse 
# Labeled precision (LP): 
# num of correct constituents in hyp. parse / of  total constituents in hyp. parse

def calculate_accuracy(true_tree: Tree, tree: Tree):
    tree_stems, true_stems = tree.stems(), true_tree.stems()
    correct, total = 0, 0
    for i, (terminal, preterm) in enumerate(tree_stems):
        true_term, true_preterm = tree_stems[i]
        if preterm.data == true_preterm.data:
            correct += 1
        total += 1

    return correct / total
