'''
File: __init__.py
Project: src
File Created: Friday, 31st May 2019 11:47:22 am
Author: Josiah Putman (joshikatsu@gmail.com)
-----
Last Modified: Friday, 31st May 2019 3:04:11 pm
Modified By: Josiah Putman (joshikatsu@gmail.com)
'''
from collections import defaultdict
from typing import DefaultDict, List, Set
from ngram import NGramsModel

class Segmenter():
    def __init__(self):
        self.ngram = NGramsModel(2)
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
            invalid_segs = set()    
            new_segs = []

            # for all possible segmentation
            # see if added the next point makes it invalid or completes a token
            for si, segpoint in enumerate(segpoints):
                current_token = text[segpoint[-1]:i]
                if current_token in self.vocab:
                    segpoint.append(i)
                    # if this token is a prefix of another, consider that option
                    if current_token in self.prefixes:
                        new_segs.append(segpoint[:-1])

                elif current_token not in self.prefixes:
                    invalid_segs.add(si)
                    
            for invalid_seg in invalid_segs:
                del segpoints[invalid_seg]
            
            segpoints += new_segs

        segmentations = [
            [text[segps[i]:segps[i + 1]] for i in range(len(segps) - 1)]
            for segps in segpoints
        ]

        # return the segmentation that has the highest probability
        def calc_prob(segmentation):
            prob = self.ngram.log_probability(segmentation)
            # print(segmentation, prob)
            return prob
        return max(segmentations, key=calc_prob)

if __name__ == "__main__":
    test_tokens = ["the", "dog", "ate", "these", "foods", "se"]
    test_tokens2 = ["the", "dog", "ate", "the", "se", "foods", "se"]
    test_text = "".join(test_tokens)
    seg = Segmenter()

    for training_seq in [test_tokens, test_tokens2, test_tokens2, test_tokens2, test_tokens2, test_tokens2]:
        seg.train(training_seq)
        
    tokens = seg.segment(test_text)
    print(tokens)
