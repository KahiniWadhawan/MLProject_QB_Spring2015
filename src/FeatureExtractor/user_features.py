# -*- coding: utf-8 -*-

import numpy as np
from user import User
from question import Question
from parent_feature_extractor import FeatureExtractor
 
class UserFeatureExtractor(FeatureExtractor):
    def __init__(self, user_id):
        self.user = User(user_id)
        #self.question = Question(qid)
        self.user_id = self.user.user_id


    def user_category_correctness_ratio(self,user_id,category):
	
	conn = sqlite3.connect('../../../data/quizbowl_buzz.db')
        cur = conn.cursor()
	query = "select (sum(CASE WHEN position > 0 THEN 1.0 ELSE 0.0 END)/count(t.question)) as cor_ratio from questions q JOIN train t ON q.id = t.question where usage != ? and category = ? and user = ? order by cor_ratio DESC "
        c = cur.execute(query,("test",category,user_id))
        cor_ratio = c.fetchall()[0][0]
       	print "cor_ratio :: ", cor_ratio
	conn.close()
        
	return cor_ratio	
        

    def user_category_avg_buzz(self,user_id,category):
	
	conn = sqlite3.connect('../../../data/quizbowl_buzz.db')
        cur = conn.cursor()
	query = "select avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.question where usage != ? and category = ? and user = ? group by user order by avg_buzz DESC"
        c = cur.execute(query,("test",category,user_id))
	avg_buzz = c.fetchall()[0][0]
       	print "avg_buzz :: ", avg_buzz
	conn.close()
        
	return avg_buzz	
        


