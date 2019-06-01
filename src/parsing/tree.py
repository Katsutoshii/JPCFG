'''
File: tree.py
Project: src
File Created: Monday, 27th May 2019 12:09:23 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Saturday, 1st June 2019 12:45:54 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import List, Any, Callable, Iterator
from lark.tree import Tree as LarkTree

class Tree():
    # simple tree data structure for holding the grammer trees
    def __init__(self, data: Any, children: List['Tree'] = None):
        self.data = data
        self.children = [] if children is None else children

    def str_children(self):
        return " ".join([str(c) for c in self.children])
        
    def __str__(self):
        # to string method for printing
        if self.children:
            return '(' + str(self.data) + ' '+ self.str_children() + ')'
        return '(' + str(self.data) + ')'

    def __repr__(self):
        return str(self)

    def iterlevels(self, condition: Callable[['Tree'], bool] = lambda x: True) -> Iterator['Tree']:
        level = [self]
        while level:
            next_level: List[Tree] = []
            for node in level:
                if condition(node):
                    yield node
                next_level += node.children
            level = next_level

    def iternonstems(self) -> Iterator['Tree']:
        return self.iterlevels(lambda n: bool(n.children and n.children[0].children))

    def iterstems(self) -> Iterator['Tree']:
        return self.iterlevels(lambda n: len(n.children) == 1 and not n.children[0].children)

    def iterleaves(self) -> List['Tree']:
        # depth first in-order traversal returning leaves
        leaves = []
        stack = [self]
        while stack:
            curr = stack.pop()
            stack += reversed(curr.children)
            if not curr.children:
                leaves.append(curr)
        return leaves

    @staticmethod
    def parse(string: str):
        tokens = string.split('(')[1:]
        
        root = Tree(tokens[0])
        stack = [root]
        for token in tokens[1:]:
            current = stack[-1]
            datastr, *endings = token.split(')')
            datastr = datastr.strip()

            # if datastr contains a terminal, then split
            # and make the second part the child
            if endings:
                datastr, childstr = datastr.split(maxsplit=1)
                child = Tree(datastr, [Tree(childstr)])
            else:
                child = Tree(datastr)

            current.children.append(child)
            stack.append(child)
            for _ in endings:
                stack.pop()
        return root

    @staticmethod
    def fromlark(larktree: LarkTree) -> 'Tree':
        root = Tree(larktree.data)
        stack = [root]
        larkstack = [larktree]
        while stack:
            curr = stack.pop()
            larkcurr = larkstack.pop()
            if isinstance(larkcurr, LarkTree):
                curr.children = [
                    Tree(lc.data) if isinstance(lc, LarkTree) else str(lc)
                    for lc in larkcurr.children
                ]
                stack += curr.children
                larkstack += larkcurr.children
        return root

if __name__ == "__main__":
    teststr = """
    (R1 (V1 (PT1 t1))
        (V2 (PT3 t3) (PT2 t2)))
    """
    tree = Tree.parse(teststr)
    print(tree)
    # for node in tree.iteredges():
    #     print(node.data, [c.data for c in node.children])
    for n in tree.iterleaves():
        print(n.data)
