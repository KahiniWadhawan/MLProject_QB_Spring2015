# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')
import numpy as np
from user import User
#from question import Question
#from parent_feature_extractor import FeatureExtractor
import sqlite3

 
#class UserFeatureExtractor(FeatureExtractor):
class UserFeatureExtractor():

   def __init__(self, user_id):
    	self.user = User(user_id)
        #self.question = Question(qid)
        self.user_id = self.user.user_id
	self.features =  defaultdict(list)


   def user_category_correctness_ratio(self,category):
	
	conn = sqlite3.connect('../../../data/quizbowl_buzz.db')
        cur = conn.cursor()
	query = "select (sum(CASE WHEN position > 0 THEN 1.0 ELSE 0.0 END)/count(t.question)) as cor_ratio from questions q JOIN train t ON q.id = t.question where usage != ? and category = ? and user = ? order by cor_ratio DESC "
        c = cur.execute(query,("test",category,self.user_id))
        cor_ratio = c.fetchall()[0][0]
	conn.close()
	self.features["u_c_cor_ratio"] = cor_ratio 

        
	#return cor_ratio	
        

   def user_category_avg_buzz(self,category):
	
	conn = sqlite3.connect('../../../data/quizbowl_buzz.db')
        cur = conn.cursor()
	query = "select avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.question where usage != ? and category = ? and user = ? group by user order by avg_buzz DESC"
        c = cur.execute(query,("test",category,self.user_id))
	avg_buzz = c.fetchall()[0][0]
	conn.close()
        self.features["u_c_avg_buzz"] = avg_buzz 

	#return avg_buzz


if __name__ == "__main__":
	user_f = UserFeatureExtractor(0)
	avg_buzz = user_f.user_category_avg_buzz("Fine Arts")
	print "question text :: ", avg_buzz

        cor_ratio = user_f.user_category_correctness_ratio("Fine Arts")
	print "cor ratio :: ", cor_ratio

	
        


