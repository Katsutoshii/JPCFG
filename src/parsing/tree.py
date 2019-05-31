'''
File: tree.py
Project: src
File Created: Monday, 27th May 2019 12:09:23 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 2:58:37 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import List, Any, Callable

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

    def iterlevels(self, condition: Callable[['Tree'], bool]):
        level = [self]
        while level:
            next_level: List[Tree] = []
            for node in level:
                if condition(node):
                    yield node
                next_level += node.children
            level = next_level

    def iternonstems(self):
        return self.iterlevels(lambda n: n.children and n.children[0].children)

    def iterstems(self):
        return self.iterlevels(lambda n: len(n.children) == 1 and not n.children[0].children)

    def iterleaves(self):
        return self.iterlevels(lambda n: not n.children)

    @staticmethod
    def parse(string: str, transform: Callable[[str], str] = None):
        tokens = string.split('(')[1:]
        
        root = Tree(tokens[0])
        stack = [root]
        for token in tokens[1:]:
            current = stack[-1]
            datastr, *endings = token.split(')')
            datastr = datastr.strip()
            if transform is not None:
                datastr = transform(datastr)
                
            # if datastr contains a terminal, then split
            # and make the second part the child
            if endings:
                datastr, childstr = datastr.split(maxsplit=1)
                child = Tree(datastr, [Tree(childstr)])
            else:
                child = Tree(datastr)

            current.children.append(child)
            stack.append(child)
            for ending in endings:
                stack.pop()
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
    for node in tree.iterleaves():
        print(node.data)
