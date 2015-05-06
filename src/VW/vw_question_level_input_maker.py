# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import sqlite3, os
from csv import DictReader
from csv import writer

class Prepare_VW_Input_Position_Model(object):
    '''class to prepare input data for VW'''
    def __init__(self, questions_db = '../../../data/quizbowl_buzz.db', \
    question_feat_db = '../../../data/question_features2_with_text.db', \
    user_feat_db = '../../../data/quizbowl_user.db', cat_feat_db = '../../../data/quizbowl_category.db', \
    questions_table = 'questions' , question_feat_table = 'sparse_features_word', \
    user_feat_table= 'user_features', cat_feat_table = 'category_all',
    user_subcat_feat_table = 'user_only_subcat'):
        
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
        self.user_subcat_feat_table = user_subcat_feat_table
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
    
        user_col_query_subcat = 'select * from {};'.format(self.user_subcat_feat_table)
        d = self.user_feat_cur.execute(user_col_query_subcat)
        self.user_col_names = ['ufeat' + x[0] for x in c.description] + ['cr_' + x[0] for x in d.description][1:]
        
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
    
    def get_user_features(self, user_id, question_id, new_user):
        self.user_features = []
        query = "select * from {} where user = ? and category = ?;".format(self.user_feat_table)
        c = self.user_feat_cur.execute(query,(user_id, self.get_category(question_id)))
        result = c.fetchall()
        
        if new_user == False:
            query = "select * from {} where user = ?;".format(self.user_subcat_feat_table)
            d = self.user_feat_cur.execute(query,(user_id,))
            res2 = d.fetchall()
            
        if new_user == True:
            query = "select * from {} where user = ?;".format(self.user_subcat_feat_table)
            d = self.user_feat_cur.execute(query,(-1,))
            res2 = d.fetchall()
            
        self.user_features = list(result[0]) + list(res2[0])
        
    def get_cat_features(self, question_id):
        self.cat_features = []
        query = "select * from {} where Question = ?;".format(self.cat_feat_table)
        c = self.cat_feat_cur.execute(query,(question_id,))
        result = c.fetchall()
        self.cat_features = list(result[0])
        
    def write_features(self, question_id, user_id, output_file, num_classes, **kwargs):
        
        if kwargs.has_key('new_user'): 
            new_user = True
        else:
            new_user = False
            
        self.get_user_features(user_id, question_id, new_user)
        user_zipped = zip(self.user_col_names, self.user_features)
    
        self.get_cat_features(question_id)
        cat_zipped = zip(self.cat_col_names, self.cat_features)
        
        self.get_question_features(question_id)
        ques_zipped = zip(self.question_col_names, self.question_features)
        
        text_write = ' |Text_Features ' + ' '.join([(str(x[1])) for x in ques_zipped[2:] if x[0] == 'text_so_far'])
        ques_write = ' |Question_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in ques_zipped[2:] if (x[0] != 'text_so_far' and x[1] != 0.)])
        user_write =  ' |User_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in user_zipped[2:] if x[1] != 0.])
        cat_write = ' |Category_Features ' + ' '.join([(x[0] + ":" + str(x[1])) for x in cat_zipped[1:] if x[1] != 0.])
        tag = "'" + str(user) + "_" + str(question)
        
        
            
        if kwargs.has_key('position'):
            label = str(position)
            label_write = label + " " + tag
        
        if kwargs.has_key('id'):
            tag = "'" + str(id)
            label_write = tag
        
        if kwargs.has_key('id') and kwargs.has_key('position'):
            label = str(position)
            tag = "'" + str(id)
            label_write = label + " " + tag
            


        write_vw = label_write + text_write + ques_write + user_write + cat_write + "\n"
        with open(output_file,'a') as fp:
            fp.write(write_vw)
           
        

def make_validation_guess_file(id, position, output_file):   
    if not os.path.exists(output_file):
        w = writer(open(output_file, 'wb'))
        w.writerow(["id", "position"])
        w.writerow([id, position])
    else:
        w = writer(open(output_file, 'a'))
        w.writerow([id, position])

if __name__ == "__main__":
    folder_path = '../../../data/'
    train = DictReader(open(folder_path+"train.csv","r"))
    test = DictReader(open(folder_path+"test.csv","r"))
    passed_ids = []
    make_train = True
    make_test = True
    val_offset = 2
    val_percent = 4
    
    output_folder = '/Volumes/My Passport for Mac/MLProject_Home/data/trial6/'
    train_users = []
    for sample in train:
        train_users.append(int(sample['user']))
    
    train = DictReader(open(folder_path+"train.csv","r"))
    if make_train == True:
        vw = Prepare_VW_Input_Position_Model()
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
            
            vw.write_features(question, user, output_file = output_folder + 'vw_pos_all_train.txt', num_classes = 3, position = position)
            if (count + val_offset) % val_percent == 0:
                vw.write_features(question, user, output_file = output_folder + 'vw_pos_validation.txt', num_classes = 3, id = id, position = position)
                make_validation_guess_file(id, position, output_file = output_folder + 'val_guesses.csv')
            else:
                vw.write_features(question, user, output_file = output_folder + 'vw_pos_train.txt', num_classes = 3, position = position)            
     
    if make_test == True:
        vw = Prepare_VW_Input_Position_Model()
        count = 0
        for sample in test:
            count += 1
            id = int(sample['id'])
            if count % 1000 == 0:
                print count
            passed_ids.append(id)
            question = int(sample['question'])
            user = int(sample['user'])
            
            if user not in train_users:
                vw.write_features(question, user, output_file = output_folder + 'vw_pos_test.txt', num_classes = 3, id = id, new_user = True)
            else:
                vw.write_features(question, user, output_file = output_folder + 'vw_pos_test.txt', num_classes = 3, id = id)


