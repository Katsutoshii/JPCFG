'''
File: pcfg.py
Project: src
File Created: Wednesday, 22nd May 2019 11:04:27 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 26th May 2019 11:34:21 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import Dict, List
from collections import defaultdict, namedtuple

Rule = namedtuple("Rule", ["lhs", "rhs"])

class PCFG():
    def __init__(self):
        self.counts: Dict[Rule, int] = defaultdict(int)
