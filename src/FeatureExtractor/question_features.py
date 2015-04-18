# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../')
from question import Question
from collections import defaultdict
from nltk import FreqDist
from parent_feature_extractor import FeatureExtractor


class QuestionFeatureExtractor(FeatureExtractor):
    def __init__(self, granularity = 'word'):
        self.granularity = granularity
        with open("sparse_mega_dict.txt", "r") as fp:
            self.sparse_mega_dict = pickle.load(fp)
    
    def __call__(self, qid):
        self.question = Question(qid)
        self.qid = qid
        self.qtext = self.question.text
        self.answer = self.question.answer
        self.category = self.question.category
        self.sentences = self.question.get_sentences()
        self.tokens = self.question.tokenize()
        self.features = defaultdict(list)
        

    def caps_cumulative(self):
        '''assigns number of words[cumulative] starting with capital letters'''
        word_position = 0.
        num_cap = 0.
        
        if self.granularity == 'word': 
            for word in self.tokens:
                if word.isupper():
                    num_cap += 1.
                
                self.features[word_position].append(num_cap)  
                word_position += 1.
            
        if self.granularity == 'question':
            for word in self.tokens:
                if word.isupper():
                    num_cap += 1.
                
            self.features[self.qid].append(num_cap)  
            
        
        
    def sentence_position(self):
        '''assigns the sentence position containing the word for word granularity
           [or]  assigns number of sentences in question for question granularity'''
        word_position = 0.
        sent_position = 0.
        
        if self.granularity == 'word': 
            for sent in self.sentences:
                tokens = sent.split()
                for token in tokens:
                    self.features[word_position].append(sent_position)
                    word_position += 1.
                    
                sent_position += 1.
                
        if self.granularity == 'question':
            self.features[self.qid].append(len(self.sentences))  
            
    def part_of_speech(self, allow = 'all', restrict = None):
        '''assigns the sentence position containing the word for word granularity
           [or]  assigns number of sentences in question for question granularity'''
           
        pos_dict = {}
        for sent_parse_dict in self.sparse_mega_dict[self.qid]['sentences']:
            for lst in sent_parse_dict['words']:
                pos_dict.update({(lst[0], lst[1]['CharacterOffsetBegin']):lst[1]['PartOfSpeech']})
        
        word_position = 0.
        sent_position = 0.
        char_position = 0.
        pos_occurences_so_far = defaultdict(FreqDist)
        
        if self.granularity == 'word': 
            for word, char_pos in pos_dict:
                pos_occurences_so_far[pos_dict[(word, char_pos)]] += 1.
                word_position = self.qtext.count(" ",0, char_pos) + 1.
                self.features[word_position].append(pos_occurences_so_far[pos_dict[(word, char_pos)]])

                
        if self.granularity == 'question':
            self.features[self.qid].append(len(self.sentences))  
                    
                
                
        
        
        