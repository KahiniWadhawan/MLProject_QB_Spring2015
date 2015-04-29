# -*- coding: utf-8 -*-

import sqlite3, os
from csv import DictReader
from collections import defaultdict

class Prepare_VW_Input_Correctness_Model(object):
    '''class to prepare input data for VW'''
    def __init__(self, questions_db = '../../../data/quizbowl_buzz.db', \
    question_feat_db = '../../../data/question_features2.db', \
    user_feat_db = '../../../data/quizbowl_user.db', cat_feat_db = '../../../data/quizbowl_category.db', \
    questions_table = 'questions' , question_feat_table = 'sparse_features_word', \
    user_feat_table= 'user_features', cat_feat_table = 'category_all'):
        
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
        self.question_features = result[-1]  
    
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
        
    def write_features(self, question_id, user_id, output_folder, output_file, **kwargs):       
        self.get_user_features(user_id, question_id)
        user_zipped = zip(self.user_col_names, self.user_features)
    
        self.get_cat_features(question_id)
        cat_zipped = zip(self.cat_col_names, self.cat_features)
        
        self.get_question_features(question_id)
        ques_zipped = zip(self.question_col_names, self.question_features)
        
        ques_write = ' |Question_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in ques_zipped[2:] if x[1] != 0.])
        user_write =  ' |User_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in user_zipped[2:] if x[1] != 0.])
        cat_write = ' |Category_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in cat_zipped[1:] if x[1] != 0.])
        tag = "'" + str(user) + "_" + str(question)
            
        if kwargs.has_key('position'):
            if position >= 0:
                label = 1
            else:
                label = 3

            label_write = str(label) + " " + tag
        elif kwargs.has_key('id'):
            tag = "'" + str(id)
            label_write = tag
        else:
            label_write = tag

        write_vw = label_write + ques_write + user_write + cat_write + "\n"
        with open(output_folder +  output_file,'a') as fp:
            fp.write(write_vw)
           
        if not os.path.exists(output_folder + "user_train_data/"):
            os.mkdir(output_folder + "user_train_data/")

        user_dir_path = output_folder + "user_train_data/" + "user_" + str(user_id) + '/'
        if not os.path.exists(user_dir_path):
            os.mkdir(user_dir_path)
        with open(user_dir_path + output_file,'a') as fp:
            fp.write(write_vw)


if __name__ == "__main__":
    folder_path = '../../../data/'
    train = DictReader(open(folder_path+"train.csv","r"))
    test = DictReader(open(folder_path+"test.csv","r"))
    passed_ids = []
    make_train = True
    make_test = True
    val_offset = 2
    val_percent = 4
    
    output_folder = '/Volumes/My Passport for Mac/MLProject_Home/data/trial1/'
    
    user_total_count = defaultdict(int)
    user_train_count = defaultdict(int)
    for sample in train:
        user_total_count[int(sample['user'])] += 1.
    
    train = DictReader(open(folder_path+"train.csv","r"))
    if make_train == True:       
        vw = Prepare_VW_Input_Correctness_Model()
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
            if (user_train_count[user] > (user_total_count[user] * 0.75)):
                vw.write_features(question, user, output_folder = output_folder, output_file = 'vw_cor_validation.txt', id = id)  
            else:        
                vw.write_features(question, user, output_folder = output_folder, output_file = 'vw_cor_train.txt', position = position)            
                user_train_count[user] += 1.
                
                
    if make_test == True:
        vw = Prepare_VW_Input_Correctness_Model()
        count = 0
        for sample in test:
            count += 1
            id = int(sample['id'])
            if count % 1000 == 0:
                print count
            passed_ids.append(id)
            question = int(sample['question'])
            user = int(sample['user'])
            
            vw.write_features(question, user, output_folder = output_folder, output_file = 'vw_cor_test.txt', id = id)
