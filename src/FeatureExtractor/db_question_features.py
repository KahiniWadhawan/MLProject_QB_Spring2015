# -*- coding: utf-8 -*-
import sys, time, re
import cPickle as pickle
import sqlite3, string
sys.path.insert(0, '../')
from question import Question
from collections import defaultdict
from csv import DictReader
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


#with open("../../../data/sparse_mega_dict2.txt", "r") as fp:
#            k_sparse_mega_dict = pickle.load(fp)

passed_ids = []
column_names = []
class DB_Question_Features(object):
    def __init__(self, qid, granularity = 'word'):
        self.granularity = granularity
        self.column_names = []
        self.question = Question(qid)
        self.qid = int(qid)
        self.qtext = self.question.text
        self.features = defaultdict(dict)
        self.conn = sqlite3.connect('../../../data/question_features2_with_text.db')
        self.cur = self.conn.cursor()
        self.create_table()
        self.sqlite_keywords = ['IN', 'IS', 'BY', 'TO', 'ON', 'OF', 'TO', 'SET']
        self.sparse_dict = defaultdict(int)
        self.stemmer = PorterStemmer()
        self.punct_table = string.maketrans("","")
        self.punctuations = string.punctuation
        self.pattern = r'[\!\"\#\$\%\&\\\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\\\]\^\_\`\{\|\}\~]'
        self.stop_words = stopwords.words('english')
       
    def create_table(self):
        query  = 'CREATE TABLE IF NOT EXISTS sparse_features_word  (QuestionID INT NOT NULL , WordPosition INT NOT NULL, PRIMARY KEY (QuestionID, WordPosition));'
        self.cur.execute(query,)
        self.conn.commit()     
        
    def add_column(self, column_name):
        try:
            if column_name != 'text_so_far':
                query = 'ALTER TABLE sparse_features_word ADD {} INT NOT NULL DEFAULT 0;'.format(column_name)
            else:
                query = 'ALTER TABLE sparse_features_word ADD {} TEXT NOT NULL DEFAULT "";'.format(column_name)
            
            self.cur.execute(query,)
            self.conn.commit()
            column_names.append(column_name)
        except:
            column_names.append(column_name)
            pass
        
        
    def insert_row(self, word_pos):
        try:
            for column_name in self.sparse_dict.keys():
                if column_name not in column_names:
                    self.add_column(column_name)
                    
            query = 'INSERT INTO sparse_features_word (QuestionID, WordPosition, {}) VALUES ({});'.\
            format(', '.join('{}'.format(key) for key in self.sparse_dict), '?,'*(len(self.sparse_dict)-1) + '?,?,?')
            
            self.cur.execute(query, (self.qid, word_pos) + tuple(self.sparse_dict.values()))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.update_value(word_pos)
            pass
            
        
    def update_value(self, word_pos):
        for column_name in self.sparse_dict.keys():
            if column_name not in column_names:
                self.add_column(column_name)
                
        query = 'UPDATE sparse_features_word SET {} WHERE QuestionID =? AND WordPosition =?'.\
        format(', '.join('{}=?'.format(key) for key in self.sparse_dict))

        self.cur.execute(query,tuple(self.sparse_dict.values()) +(self.qid, word_pos))
        self.conn.commit()
        
        
    def sparse_features_sql(self):
        '''builds cumulative parts of speech feature for word granularity
            or total parts of speech for question granularity'''

        
        if not k_sparse_mega_dict.has_key(self.qid):
            passed_ids.append(self.qid)
            return
            
        
        for sent_parse_dict in k_sparse_mega_dict[self.qid]['sentences']:
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
                        
                self.sparse_dict[pos] += 1.
                self.insert_row(word_position)
                
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
                            
                self.sparse_dict[ner] += 1.
                self.update_value(word_position)
        
    def count_caps(self):
        '''counts number of caps, number of caps leaving out continuous caps in text at word level'''
        prev = -2.
        for word_position, word in enumerate(self.qtext.split()):  
            if word[0].isupper():
                self.sparse_dict['count_of_caps'] += 1.
                if prev != word_position - 1:
                    self.sparse_dict['c_of_caps_ignore_cont'] += 1.
                prev = word_position

            self.update_value(word_position)
            #print word, word_position, self.sparse_dict['count_of_caps'], self.sparse_dict['c_of_caps_ignore_cont']
            
    def unigram_count(self):
        self.sparse_dict = defaultdict(int)
        qtext = re.sub(self.pattern, '', self.qtext)
        qtext_split = [self.stemmer.stem(word.lower()) for word in qtext.split()]
        for word_position, word in enumerate(qtext_split):
            text_so_far = ' '.join(qtext_split[:word_position + 1])
            self.sparse_dict['text_so_far'] = text_so_far

            print word_position, text_so_far
            #self.update_value(word_position)
                
              
if __name__ == "__main__":
    train = list(DictReader(open('../../../data/'+"questions.csv","r")))
    print "IMPORTED TRAIN DATA"
    count = 0
    for item in train:
        count += 1
        start_time = time.clock()
        qid = item['id']

        sp = DB_Question_Features(qid)
        #sp.sparse_features_sql()
        #sp.count_caps()
        sp.unigram_count()
        end_time = time.clock()
        break
        print "count: ", count, "id: ", qid, " : ", ":: time: ", end_time - start_time
        
    sp.conn.close()
    print "passed_ids_len: ", len(passed_ids)
    with open("passed_ids_sql.txt", "w") as fp:
        pickle.dump(passed_ids, fp)
