# -*- coding: utf-8 -*-
import sys, time
import cPickle as pickle
import sqlite3, string
sys.path.insert(0, '../')
from question import Question
from collections import defaultdict, OrderedDict
from csv import DictReader


class DB_Question_Features(object):
    def __init__(self, granularity = 'word'):
        self.granularity = granularity
        self.column_names = []
        with open("../../../data/sparse_mega_dict2.txt", "r") as fp:
            self.sparse_mega_dict = pickle.load(fp)
    
    def __call__(self, qid):
        self.question = Question(qid)
        self.qid = int(qid)
        self.qtext = self.question.text
        self.features = defaultdict(dict)
        self.conn = sqlite3.connect('../../../data/question_features2.db')
        self.cur = self.conn.cursor()
        self.create_table()
        self.sqlite_keywords = ['IN', 'IS', 'BY', 'TO', 'ON', 'OF', 'TO', 'SET']
        self.punctuation_dict = {}
       
    def create_table(self):
        query  = 'CREATE TABLE IF NOT EXISTS sparse_features_word  (QuestionID INT NOT NULL , WordPosition INT NOT NULL, PRIMARY KEY (QuestionID, WordPosition));'
        self.cur.execute(query,)
        
    def add_column(self, column_name):
        print "adding column", column_name
        try:
            query = 'ALTER TABLE sparse_features_word ADD {} INT NOT NULL DEFAULT 0;'.format(column_name)
            self.cur.execute(query,)
            self.column_names.append(column_name)
        except:
            pass
        
    def insert_row(self, qid, word_pos, sparse_dict):
        print "inserting_row", qid, word_pos
        try:
            for column_name in sparse_dict.keys():
                if column_name not in self.column_names:
                    self.add_column(column_name)
                    
            query = 'INSERT INTO sparse_features_word (QuestionID, WordPosition, {}) VALUES ({});'.\
            format(', '.join('{}'.format(key) for key in sparse_dict), '?,'*(len(sparse_dict)-1) + '?,?,?')
            
            self.cur.execute(query, (qid, word_pos) + tuple(sparse_dict.values()))
        except sqlite3.IntegrityError:
            self.update_value(qid, word_pos, sparse_dict)
            pass

            
        
    def update_value(self, qid, word_pos, sparse_dict):
        print "updating_row", qid, word_pos
        for column_name in sparse_dict.keys():
            if column_name not in self.column_names:
                self.add_column(column_name)
                
        query = 'UPDATE sparse_features_word SET {} WHERE QuestionID =? AND WordPosition =?'.\
        format(', '.join('{}=?'.format(key) for key in sparse_dict))
        
        self.cur.execute(query,tuple(sparse_dict.values()) +(qid, word_pos))
        
        
    def sparse_features_sql(self):
        '''builds cumulative parts of speech feature for word granularity
            or total parts of speech for question granularity'''
        #print self.qid
        sparse_dict = defaultdict(int)
        
        if not self.sparse_mega_dict.has_key(self.qid):
            return
            
        
        for sent_parse_dict in self.sparse_mega_dict[self.qid]['sentences']:
            for lst in sent_parse_dict['words']:
                char_pos = lst[1]['CharacterOffsetBegin']
                word_position = self.qtext.count(" ",0, int(char_pos))
                
                pos = lst[1]['PartOfSpeech']
                
                if pos in self.sqlite_keywords:
                    pos = "k_" + pos
                else:
                    if pos[0] in string.punctuation:
                        if len(pos) == 1:
                            pos = "k_" + str(ord(pos))
                        else:
                            new_pos = ord(pos[0])
                            for i in pos[1:]:
                                new_pos += ord(i)
                            pos = "k_" + str(new_pos)
                        
                sparse_dict[pos] += 1.
                print "calling insert from sparse_features_sql"
                self.insert_row(self.qid, word_position, sparse_dict)
                
                ner = lst[1]['NamedEntityTag']
                
                if ner in self.sqlite_keywords or ner in string.punctuation:
                    ner = "k_" + ner
                else:
                    if ner[0] in string.punctuation:
                        if len(ner) == 1:
                            ner = "k_" + str(ord(ner))
                        else:
                            new_ner = ord(ner[0])
                            for i in ner[1:]:
                                new_ner += ord(i)
                            ner = "k_" + str(new_ner)
                            
                sparse_dict[ner] += 1.
                print "updating from sparse_features_sql"
                self.update_value(self.qid, word_position, sparse_dict)
        #print sparse_dict
                
              
if __name__ == "__main__":
    train = list(DictReader(open('../../../data/'+"little_questions.csv","r")))
    print "IMPORTED TRAIN DATA"
    sp = DB_Question_Features()
    for item in train:
        #print item['question']
        start_time = time.clock()
        qid = item['id']
        sp(qid)
        sp.sparse_features_sql()
        end_time = time.clock()
        print qid, " : ", ":: time: ", end_time - start_time
        
    sp.conn.close()
