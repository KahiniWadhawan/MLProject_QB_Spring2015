# -*- coding: utf-8 -*-

import sys
import cPickle as pickle
sys.path.insert(0, '../')
from question import Question
from collections import defaultdict, OrderedDict
from nltk import FreqDist



class QuestionFeatureExtractor(object):
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
        self.features = defaultdict(dict)
        

    def caps_cumulative(self):
        '''assigns number of words[cumulative] starting with capital letters'''
        word_position = 0.
        num_cap = 0.
        
        if self.granularity == 'word': 
            for word in self.tokens:
                if word.isupper():
                    num_cap += 1.
                
                self.features[word_position].update({"c_cap": num_cap})  
                word_position += 1.
            
        if self.granularity == 'question':
            for word in self.tokens:
                if word.isupper():
                    num_cap += 1.
                
            self.features[self.qid].update({"c_cap": num_cap})  
            
        
        
    def sentence_position(self):
        '''assigns the sentence position containing the word for word granularity
           [or]  assigns number of sentences in question for question granularity'''
        word_position = 0.
        sent_position = 0.
        
        if self.granularity == 'word': 
            for sent in self.sentences:
                tokens = self.question.tokenize(othertext = sent)
                for token in tokens:
                    self.features[word_position].append({"s_pos": sent_position})
                    word_position += 1.
                    
                sent_position += 1.
                
        if self.granularity == 'question':
            self.features[self.qid].update({"s_pos": len(self.sentences)})  
      
  
    
    def part_of_speech(self, allow = 'all', restrict = None):
        '''builds cumulative parts of speech feature for word granularity
            or total parts of speech for question granularity'''
           
        pos_dict = OrderedDict()
        for sent_parse_dict in self.sparse_mega_dict[self.qid]['sentences']:
            for lst in sent_parse_dict['words']:
                pos_dict.update({(lst[0], lst[1]['CharacterOffsetBegin']):lst[1]['PartOfSpeech']})
        
        word_position = 0.
        pos_occurences_so_far = defaultdict(FreqDist)
        
        if self.granularity == 'word': 
            for word, char_pos in pos_dict:
                pos = pos_dict[(word, char_pos)]
   
                pos_occurences_so_far[pos] += 1.
                word_position = self.qtext.count(" ",0, char_pos) + 1.
                self.features[word_position].update(pos_occurences_so_far)
                
                # restrict or allow only certain NER
                if restrict != None:
                    for item in restrict:
                        self.features[word_position].pop(item)
                if allow != 'all':
                    pos_occurences_allowed = {}
                    for item in allow:
                        pos_occurences_allowed[item] = pos_occurences_so_far[item]
                    pos_occurences_so_far = pos_occurences_allowed
                    self.features[word_position] = pos_occurences_so_far

                
        if self.granularity == 'question':
            for word, char_pos in pos_dict:
                pos_occurences_so_far[pos_dict[(word, char_pos)]] += 1.
                word_position = self.qtext.count(" ",0, char_pos) + 1.
            
            pos = pos_dict[(word, char_pos)]
            # restrict or allow only certain POS
            if restrict != None:
                for item in restrict:
                    pos_occurences_so_far.pop(item)
            if allow != 'all':
                pos_occurences_allowed = {}
                for item in allow:
                    pos_occurences_allowed[item] = pos_occurences_so_far[item]
                pos_occurences_so_far = pos_occurences_allowed
            self.features[self.qid].update(pos_occurences_so_far)



    def NER(self, allow = 'all', restrict = [u'O']):
        '''builds cumulative NER feature for word granularity
            or total NER for question granularity'''
           
        ner_dict = OrderedDict()
        for sent_parse_dict in self.sparse_mega_dict[self.qid]['sentences']:
            for lst in sent_parse_dict['words']:
                ner_dict.update({(lst[0], lst[1]['CharacterOffsetBegin']):lst[1]['NamedEntityTag']})
        
        word_position = 0.
        ner_occurences_so_far = defaultdict(FreqDist)
        
        if self.granularity == 'word': 
            for word, char_pos in ner_dict:
                ner = ner_dict[(word, char_pos)]

                ner_occurences_so_far[ner] += 1.
                word_position = self.qtext.count(" ",0, char_pos) + 1.
                self.features[word_position].update(ner_occurences_so_far)
                
                # restrict or allow only certain NER
                if restrict != None:
                    for item in restrict:
                        self.features[word_position].pop(item)
                if allow != 'all':
                    ner_occurences_allowed = {}
                    for item in allow:
                        ner_occurences_allowed[item] = ner_occurences_so_far[item]
                    ner_occurences_so_far = ner_occurences_allowed
                    self.features[word_position] = ner_occurences_so_far
            
                
        if self.granularity == 'question':
            for word, char_pos in ner_dict:
                ner_occurences_so_far[ner_dict[(word, char_pos)]] += 1.
                word_position = self.qtext.count(" ",0, char_pos) + 1.
            
            ner = ner_dict[(word, char_pos)]
            # restrict or allow only certain NER
            if restrict != None:
                for item in restrict:
                    ner_occurences_so_far.pop(item)
            if allow != 'all':
                ner_occurences_allowed = {}
                for item in allow:
                    ner_occurences_allowed[item] = ner_occurences_so_far[item]
                ner_occurences_so_far = ner_occurences_allowed
            self.features[self.qid].update(ner_occurences_so_far)
                
                
        
        
        
