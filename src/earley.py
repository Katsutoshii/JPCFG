'''
File: earley.py
Project: src
File Created: Tuesday, 28th May 2019 8:59:30 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Tuesday, 28th May 2019 10:57:57 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''

from typing import List, Set, Optional
from copy import copy
from pcfg import PCFG, Rule

class EarleyParser():
    GAMMA = 'GAMMA'
    
    class State():
        def __init__(
            self,
            rule: Rule,
            start: int,
            backpointer: Optional['EarleyParser.State'],
            dot: int = 0
        ):
            self.rule: Rule = rule
            self.start: int = start
            self.backpointer = backpointer
            self.dot = dot

        def finished(self):
            return self.dot == len(self.rule.rhs) - 1
        
        def curr(self):
            return self.rule.rhs[self.dot]

        def next(self):
            return self.rule.rhs[self.dot + 1]

        def prev(self):
            return self.rule.rhs[self.dot - 1]
            
    def __init__(self, pcfg: PCFG):
        self.pcfg = pcfg
        self.statesets: List[Set[EarleyParser.State]] = []
        
        self.i: int = 0
        self.word: str = ""
        self.state: Optional[EarleyParser.State] = None
    
    def parse(self, words: List[str]):
        self.statesets = [set() for word in words]
        self.statesets[0].add(self.State(Rule(self.GAMMA, self.pcfg.s), 0, None))
        for self.i, self.word in enumerate(words):
            for self.state in self.statesets[self.i]:
                if not self.state.finished():
                    if self.terminal(self.state.next()):
                        self.scanner()
                    else:
                        self.predictor()
                else:
                    self.completer()

    def terminal(self, word):
        return word in self.pcfg.preterminals

    def predictor(self):
        for rule in self.pcfg.prods(self.state.curr()):
            new_state = self.State(rule, self.i, self.state)
            self.statesets[self.i].add(new_state)

    def scanner(self):
        if self.state.curr() in self.pcfg.preterminals[self.word]:
            new_state = copy(self.state)
            new_state.dot += 1
            self.statesets[self.i + 1].add(new_state)

    
    def completer(self):
        pass

if __name__ == "__main__":
    pcfg = PCFG()
    rules = [
        Rule('P', ('S',)),
        Rule('S', ('S', '+', 'M',)),
        Rule('S', ('M',)),
        Rule('M', ('M', '*', 'T',)),
        Rule('M', ('T',)),
    ]
    terminals = [
        Rule('T', ('1',)),
        Rule('T', ('2',)),
        Rule('T', ('3',)),
        Rule('T', ('4',)),
    ]
    
    pcfg.starts.add('P')
    for rule in rules + terminals:
        pcfg.add(rule)
    for terminal in terminals:
        pcfg.add_terminal(terminal)

    print("terminals:", pcfg.preterminals)

    ep = EarleyParser(pcfg)
    print(ep.terminal('1'))
    print(ep.terminal('T'))
