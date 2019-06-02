'''
File: ngram.py
Project: hw2
File Created: Saturday, 20th April 2019 1:56:15 pm
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 12:08:48 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from sys import argv
from collections import defaultdict
import math
from typing import List, Tuple

from tools import pick_random_item

class NGramsModel():
    def __init__(self, n: int, l: float = 1):
        # constructor for the n-grams model
        self.n = n
        self.l = l

        # counts keeps track of the number of occurrences of strings of size n
        self.alphabet = set()                           # type: set
        self.sequence_counts = defaultdict(int)         # type: defaultdict
        self.precedent_counts = defaultdict(int)        # type: defaultdict

        self.smoothed = False
        self.probabilities = {}       # type: dict
        
    def sequences(self, symbols):
        # generator function to get all sequences of length
        # and all precedents of length n-1
        m = self.n - 1
        symbols = ['#'] * m + symbols + ['#']

        for i, symbol in enumerate(symbols[m - 1:-1], m):
            self.alphabet.add(symbol)
            precedent = tuple(symbols[(i - m):i])
            sequence = tuple(symbols[(i - m):(i + 1)])
            yield precedent, sequence

    def train(self, symbols: List[str]) -> None:
        # trains the model on a given tokens
        for precedent, sequence in self.sequences(symbols):
            self.precedent_counts[precedent] += 1
            self.sequence_counts[sequence] += 1

    def smooth(self, symbols: List[str]):
        # reads in the line, adding all unseen precedents to the dictionary
        for precedent, symbols in self.sequences(symbols):
            if precedent not in self.precedent_counts:
                self.precedent_counts[precedent] = 0

    def generate_words(self, n: int) -> List[str]:
        # generates n words using the model
        return [self.generate_word() for _ in range(n)]

    def generate_word(self) -> str:
        # generates a random word using the model
        m = self.n - 1
        word = ['#'] * m

        # until we generate an ending symbol
        while True:
            alphabet = list(self.alphabet)
            precedent = word[-m:]
            probabilities = [
                self.probability(tuple(precedent), tuple(precedent + [a])) 
                for a in alphabet
            ]

            symbol = pick_random_item(alphabet, probabilities)
            word += [symbol]
            if symbol == '#':
                break
        return " ".join(word[m:-1])
        
    def probability(self, precedent: Tuple[str, ...], sequence: Tuple[str, ...]) -> float:
        # calculates the probability of a sequence given a precedent sequence
        # for bi-grams the precedent is only one character
        if self.smoothed:
            
            return (self.sequence_counts[sequence] + self.l) / (self.precedent_counts[precedent] + self.l * len(self.precedent_counts))
        else:
            return float(self.sequence_counts[sequence]) / float(self.precedent_counts[precedent])

    def log_probability(self, symbols: List[str]) -> float:
        # calculates the logarithmic probability of a sequence of symbols
        total_log_prob = 0.0
        
        for symbol, sequence in self.sequences(symbols):
            prob = self.probability(symbol, sequence)
            if prob == 0:
                total_log_prob += -float('inf')
            else: 
                total_log_prob += math.log(prob, 2)

        return total_log_prob

    def perplexity(self, log_prob: float, num_samples: int):
        return 2 ** (log_prob * (-1.0) / float(num_samples))

    def evaluate_line(self, line: str) -> Tuple[float, int]:
        # calculates the logarithmic probability of a given line
        word = line.strip()
        symbols = word.split()
        log_prob = self.log_probability(symbols)
        prob = 2 ** log_prob
        self.probabilities[word] = prob
        print(word + "\t" + str(prob))
        return log_prob, len(symbols) + 1
