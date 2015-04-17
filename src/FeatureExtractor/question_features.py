# -*- coding: utf-8 -*-

import numpy as np
import sys
sys.path.insert(0, '../')
from question import Question
from collections import defaultdict
#from parent_feature_extractor import FeatureExtractor


class QuestionFeatureExtractor():
    def __init__(self, qid):
        self.question = Question(qid)
        self.qtext = self.question.text
        self.answer = self.question.answer
        self.category = self.question.category
        self.sentences = self.question.get_sentences()
        self.tokens = self.question.tokenize()
        self.features = defaultdict(list)

    def caps_cumulative(self):
        word_position = 0.
        num_cap = 0.
        
        for word in self.tokens:
            if word.isupper():
                num_cap += 1.
            
            self.features[word_position].append(num_cap)  
            word_position += 1.
        
        
    def sentence_position(self):
        word_position = 0.
        sent_position = 0.
        for sent in self.sentences:
            tokens = sent.split()
            for token in tokens:
                self.features[word_position].append(sent_position)
                word_position += 1.
                
            sent_position += 1.
                
                
                
        
        
        
