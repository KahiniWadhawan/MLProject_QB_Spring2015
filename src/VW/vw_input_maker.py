# -*- coding: utf-8 -*-

import sqlite3
from csv import DictReader


class Prepare_VW_Input(object):
    '''class to prepare input data for VW'''
    def __init__(self, output_file = '/Volumes/My Passport for Mac/MLProject_Home/data/vw_input.txt', \
    questions_db = '../../../data/quizbowl_buzz.db', question_feat_db = '../../../data/question_features2.db', \
    user_feat_db = '../../../data/quizbowl_user.db', cat_feat_db = '../../../data/quizbowl_category.db', \
    questions_table = 'questions' , question_feat_table = 'sparse_features_word', \
    user_feat_table= 'user_features', cat_feat_table = 'category_all'):
        
        self.output_file = output_file
        
        self.questions_conn = sqlite3.connect(questions_db)
        self.question_feat_conn = sqlite3.connect(question_feat_db)
        self.user_feat_conn = sqlite3.connect(user_feat_db)
        self.cat_feat_conn = sqlite3.connect(cat_feat_db)
        
        self.questions_cur = self.questions_conn.cursor()
        self.question_feat_cur = self.question_feat_conn.cursor()
        self.user_feat_cur = self.user_feat_conn.cursor()
        self.cat_feat_cur = self.cat_feat_conn.cursor()
        
        self.questions_table = questions_table
        self.question_feat_table = question_feat_table
        self.user_feat_table = user_feat_table
        self.cat_feat_table =  cat_feat_table
        
        self.question_features = []
        self.user_features = []
        self.cat_features = []

        self.get_col_names()
        
    def get_col_names(self):
        question_col_query = 'select * from {};'.format(self.question_feat_table)
        c = self.question_feat_cur.execute(question_col_query)
        self.question_col_names = [x[0] for x in c.description]
        
        user_col_query = 'select * from {};'.format(self.user_feat_table)
        c = self.user_feat_cur.execute(user_col_query)
        self.user_col_names = [x[0] for x in c.description]
        
        cat_col_query = 'select * from {};'.format(self.cat_feat_table)
        c = self.cat_feat_cur.execute(cat_col_query)
        self.cat_col_names = [x[0] for x in c.description]
        
    def get_category(self, question_id):
        query = "select category from {} where id = ?;".format(self.questions_table)
        c = self.questions_cur.execute(query,(question_id,))
        result = c.fetchall()
        return result[0][0]

    def get_question_features(self, question_id):
        query = "select * from {} where QuestionID = ?;".format(self.question_feat_table)
        c = self.question_feat_cur.execute(query,(question_id,))
        result = c.fetchall()
        return result
        
    
    def get_user_features(self, user_id, question_id):
        self.user_features = []
        query = "select * from {} where user = ? and category = ?;".format(self.user_feat_table)
        c = self.user_feat_cur.execute(query,(user_id, self.get_category(question_id)))
        result = c.fetchall()
        self.user_features = list(result[0])
        
    def get_cat_features(self, question_id):
        self.cat_features = []
        query = "select * from {} where Question = ?;".format(self.cat_feat_table)
        c = self.cat_feat_cur.execute(query,(question_id,))
        result = c.fetchall()
        self.cat_features = list(result[0])
        
        
    def write_features(self, question_id, user_id, **position):
        result =  self.get_question_features(question_id)
        self.get_user_features(user_id, question_id)
        user_zipped = zip(self.user_col_names, self.user_features)

    
        self.get_cat_features(question_id)
        cat_zipped = zip(self.cat_col_names, self.cat_features)
        
        label = 2

        for word_pos, item in enumerate(result):
            ques_zipped = zip(self.question_col_names, item)
            ques_word_write = ' |Question_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in ques_zipped[2:] if x[1] != 0.])
            user_write =  ' |User_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in user_zipped[2:] if x[1] != 0.])
            cat_write = ' |Category_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in cat_zipped[1:] if x[1] != 0.])
            tag = "'" + str(user) + "_" + str(question) + "_" + str(word_pos)
            
            if position:
                if word_pos == position:
                    label = 1
                if word_pos == -position:
                    label = 3
                    
                label_write = str(label) + " " + tag
            else:
                label_write = tag
                
            
            write_vw = label_write + ques_word_write + user_write + cat_write + "\n"
            with open(self.output_file,'a') as fp:
                fp.write(write_vw)
            

if __name__ == "__main__":
    
    folder_path = '../../../data/'
    train = DictReader(open(folder_path+"train.csv","r"))
    test = DictReader(open(folder_path+"test.csv","r"))
    passed_ids = []
    make_train = False
    make_test = True
    
    if make_train == True:
        output_file = '/Volumes/My Passport for Mac/MLProject_Home/data/vw_input.txt'
        vw = Prepare_VW_Input(output_file)
        count = 0
        for sample in train:
            count += 1
            id = int(sample['id'])
            if count % 1000 == 0:
                print count
            passed_ids.append(id)
            question = int(sample['question'])
            user = int(sample['user'])
            
            position = float(sample['position'])
            vw.write_features(question, user, position = position)
            
    if make_test == True:
        output_file = '/Volumes/My Passport for Mac/MLProject_Home/data/vw_test.txt'
        vw = Prepare_VW_Input(output_file)
        count = 0
        for sample in test:
            count += 1
            id = int(sample['id'])
            if count % 1000 == 0:
                print count
            passed_ids.append(id)
            question = int(sample['question'])
            user = int(sample['user'])
            
            vw.write_features(question, user)
