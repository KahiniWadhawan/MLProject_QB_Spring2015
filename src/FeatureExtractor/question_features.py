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
        with open("../../data/sparse_mega_dict2.txt", "r") as fp:
            self.sparse_mega_dict = pickle.load(fp)
    
    def __call__(self, qid):
        self.question = Question(qid)
        self.qid = int(qid)
        self.qtext = self.question.text
        #self.answer = self.question.answer
        #self.category = self.question.category
        #self.sentences = self.question.get_sentences()
        #self.tokens = self.question.tokenize()
        self.features = defaultdict(dict)
        
    def feat_vectorizer(self, dict_of_dict):
        for item in dict_of_dict:
            dict_of_dict[item] = dict_of_dict[item].values()
        return dict_of_dict

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
                    self.features[word_position].update({"s_pos": sent_position})
                    word_position += 1.
                    
                sent_position += 1.
                
        if self.granularity == 'question':
            self.features[self.qid].update({"s_pos": len(self.sentences)})  
      
  
    
    def sparse_features(self):
        '''builds cumulative parts of speech feature for word granularity
            or total parts of speech for question granularity'''
        print self.qid
        sparse_dict = OrderedDict()
        
        if not self.sparse_mega_dict.has_key(self.qid):
            self.features = None
            return
            
            
        for sent_parse_dict in self.sparse_mega_dict[self.qid]['sentences']:
            for lst in sent_parse_dict['words']:
                sparse_dict.update({(lst[0], lst[1]['CharacterOffsetBegin']):(lst[1]['PartOfSpeech'], lst[1]['NamedEntityTag']) })

        
        word_position = 0.
        pos_occurences_so_far = {u'CC':0,u'CD':0,u'DT':0,u'EX':0,u'FW':0,u'IN':0,\
        u'JJ':0,u'JJR':0,u'JJS':0,u'LS':0,u'MD':0,u'NN':0,u'NNS':0,u'NNP':0,u'NNPS':0,\
        u'PDT':0,u'PRP':0,u'PRP$':0,u'RB':0,u'RBR':0,u'RBS':0,u'RP':0,u'SYM':0,\
        u'TO':0,u'UH':0,u'VB':0,u'VBD':0,u'VBG':0,u'VBN':0,u'VBP':0,u'VBZ':0,\
        u'WDT':0,u'WP$':0,u'WRB':0, u'POS': 0, u'WP': 0, u',': 0, u'!':0, u'"':0, \
        u'#':0, u'$':0, u'%':0, u'&':0, u'\\':0, u'\'':0, u'(':0, u')':0, u'*':0,\
        u'+':0, u'-':0, u'.':0, u'/':0, u':':0, u';':0, u'<':0, u'>':0, u'=':0, \
        u'?': 0, u'@':0, u'[':0, u']':0, u'^':0, u'_':0, u'~':0, u'{':0, u'}':0, u'|':0,\
        u'``':0, u"''": 0, u'-LRB-':0, u'O':0}
        
        ner_occurences_so_far =  { u'PERSON':0,u'LOCATION':0,u'ORGANIZATION':0, u'MISC':0,\
        u'DATE': 0, u'TIME':0, 'DURATION':0, u'SET':0, \
        u'MONEY':0, 'PERCENT':0, u'NUMBER':0, u'ORDINAL':0,\
        u'O':0 }
        
        if self.granularity == 'word': 
            for word, char_pos in sparse_dict:
                pos, ner = sparse_dict[(word, char_pos)]
                if not pos_occurences_so_far.has_key(pos):
                    pos = u'O'
                if not ner_occurences_so_far.has_key(ner):
                    ner = u'O'
                pos_occurences_so_far[pos] += 1.
                ner_occurences_so_far[ner] += 1.
                word_position = self.qtext.count(" ",0, int(char_pos))
                self.features[word_position].update(pos_occurences_so_far)
                self.features[word_position].update(ner_occurences_so_far)
            print self.features
            print "\n\n\n"
                
        if self.granularity == 'question':
            for word, char_pos in sparse_dict:
                pos, ner = sparse_dict[(word, char_pos)]
                if not pos_occurences_so_far.has_key(pos):
                    pos = u'O'
                if not ner_occurences_so_far.has_key(ner):
                    ner = u'O'
                pos_occurences_so_far[pos] += 1.
                ner_occurences_so_far[ner] += 1.

            
            self.features[self.qid].update(pos_occurences_so_far)
            self.features[self.qid].update(ner_occurences_so_far)
            


    def NER(self, allow = 'all', restrict = None):
        '''builds cumulative NER feature for word granularity
            or total NER for question granularity'''
           
        ner_dict = OrderedDict()
        
        if not self.sparse_mega_dict.has_key(self.qid):
            self.features = None
            return
            
        for sent_parse_dict in self.sparse_mega_dict[self.qid]['sentences']:
            for lst in sent_parse_dict['words']:
                ner_dict.update({(lst[0], lst[1]['CharacterOffsetBegin']):lst[1]['NamedEntityTag']})
        
        word_position = 0.
        ner_occurences_so_far =  {u'PERSON':0,u'LOCATION':0,u'ORGANIZATION':0, u'MISC':0,\
                                  u'DATE': 0, u'TIME':0, 'DURATION':0, u'SET':0, \
                                  u'MONEY':0, 'PERCENT':0, u'NUMBER':0, u'ORDINAL':0,\
                                  u'O':0}
        
        if self.granularity == 'word': 
            for word, char_pos in ner_dict:
                ner = ner_dict[(word, char_pos)]

                ner_occurences_so_far[ner] += 1.
                word_position = self.qtext.count(" ",0, int(char_pos)) + 1.
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
                word_position = self.qtext.count(" ",0, int(char_pos)) + 1.
            
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
                
                
        
        
        
