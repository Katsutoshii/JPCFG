'''
File: segmenter.py
Project: src
File Created: Friday, 31st May 2019 11:47:22 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Sunday, 2nd June 2019 12:56:13 am
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from collections import defaultdict
from typing import DefaultDict, List, Set

from .ngram import NGramsModel

class Segmenter():
    def __init__(self):
        self.ngram = NGramsModel(2, l=0.2)
        self.vocab: DefaultDict[str, int] = defaultdict(int)
        self.prefixes: DefaultDict[str, Set[str]] = defaultdict(set)

    def train(self, tokens: List[str]):
        for token in tokens:
            self.ngram.train(tokens)
            self.vocab[token] += 1
            for i, _ in enumerate(token):
                self.prefixes[token[:i]].add(token)
    
    def segment(self, text: str) -> List[str]:
        current_token = ""
        segpoints: List[List[int]] = [[0]]  # stores each index point for each
                                            # possible segmentation
        invalid_segs: Set[int] = set()      # keeps track of segmentations that need to be deleted
        new_segs: List[List[int]] = []      # keeps track of new possible segmentations

        # loop over all symbols in the unsegmented text
        for i, _ in enumerate(text + " "):
            # reset the intermediate collections   
            new_segs = segpoints[:]

            # for all possible segmentation
            # see if added the next point makes it invalid or completes a token
            for si, segpoint in enumerate(segpoints):
                current_token = text[segpoint[-1]:i]
                if current_token in self.vocab:
                    # if this token is a prefix of another, consider that option
                    if current_token in self.prefixes:
                        new_segs.append(segpoint[:])
                    segpoint.append(i)

                # elif current_token not in self.prefixes:
                #     new_segs[si] = []

            segpoints = [s for s in new_segs if s]

        segmentations = [
            [text[segps[i]:segps[i + 1]] for i in range(len(segps) - 1)]
            for segps in segpoints if segps[-1] == len(text)
        ]

        # if there were no valid segmentations
        if not segmentations:
            return []
        
        # return the segmentation that has the highest probability
        def calc_prob(segmentation):
            prob = self.ngram.log_probability(segmentation)
            # print(segmentation, prob)
            return prob
        return max(segmentations, key=calc_prob)

    def test(self, text: str, true_tokens: List[str]) -> float:
        for token in true_tokens:
            if token not in self.vocab:
                print(f"Warning: {token} not in vocab.")
                
        self.ngram.smooth(true_tokens)
        tokens = self.segment(text)
        accuracy = self.calc_accuracy(tokens, true_tokens)
        return accuracy

    @staticmethod
    def calc_accuracy(tokens: List[str], true_tokens: List[str]) -> float:
        true_tokens_set = set(true_tokens)
        correct = 0
        for token in tokens:
            if token in true_tokens:
                correct += 1
        return correct / len(true_tokens)
