'''
File: __init__.py
Project: tools
File Created: Friday, 31st May 2019 11:42:58 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 3:54:06 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from typing import List, Any
import random

from .log import log

def pick_random_item(items: List[Any], weights: List[float]) -> Any:
    # reference: https://medium.com/@peterkellyonline/weighted-random-selection-3ff222917eb6
    total_weight = sum(weights)
    random_weight = random.uniform(0, total_weight)
    for i, item in enumerate(items):
        random_weight -= weights[i]
        if random_weight <= 0:
            return item
    return None


def precision(truepos: int, falsepos: int) -> float:
    # calculates precision
    return (truepos) / (truepos + falsepos)


def recall(truepos: int, falseneg: int) -> float:
    # calculates recall
    return float(truepos) / float(truepos + falseneg)


def f1(precision: float, recall: float):
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)
