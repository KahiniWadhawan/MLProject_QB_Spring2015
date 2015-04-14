# -*- coding: utf-8 -*-
import sqlite3, sys
import cPickle as pickle

class StanfordParser(object):
    def __init__(self, parser_path, parser_dir):
        self.parser_path = parser_path
        self.parser_dir = parser_dir
        
        sys.path.append(self.parser_path)
        from corenlp import StanfordCoreNLP
        self.parser = StanfordCoreNLP(self.parser_path + self.parser_dir)
        
    def parser(self, qtext):
        return self.raw_parse(qtext)
        
        

if __name__ == "__main__":
    conn = sqlite3.connect('/Users/manjhunathkr/Documents/MLProject_Home/data/quizbowl_buzz.db')
    cur = conn.cursor()

    s = StanfordParser('/Users/manjhunathkr/Documents/corenlp-python/', 'stanford-corenlp-full-2014-08-27')
    query = "select id, text from questions"
    c = cur.execute(query,)
    all_questions =  c.fetchall()
    print "questions fetched"
    
    pointer_id = 0
    print "started"
    count = pointer_id
    with open("/Users/manjhunathkr/Documents/MLProject_Home/data/stanford_parse_dump.txt", "a") as fp:
        for ID, qtext in all_questions:
            if ID < pointer_id:
                continue
            sparse_output = {}
            sparse = s.parser.raw_parse(qtext)
            print count
            sparse_output.update({ID: sparse})
            count += 1
            pickle.dump(sparse_output, fp)
        