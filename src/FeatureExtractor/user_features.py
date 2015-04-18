# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')
import numpy as np
from user import User
import sqlite3
from collections import defaultdict


class UserFeatureExtractor():

   def __init__(self, user_id):
    	self.user = User(user_id)
        #self.question = Question(qid)
        self.user_id = self.user.user_id
	self.features =  defaultdict(list)


   def user_category_correctness_ratio(self,category):
	conn = sqlite3.connect('../../data/quizbowl_buzz.db')
        cur = conn.cursor()
	query = "select (sum(CASE WHEN position > 0 THEN 1.0 ELSE 0.0 END)/count(t.question)) as cor_ratio from questions q JOIN train t ON q.id = t.question where category = ? and user = ? order by cor_ratio DESC "
        c = cur.execute(query,(category,self.user_id))
        cor_ratio = c.fetchall()[0][0]
	if cor_ratio == None:
		#user is new, assign avg - change it later 
		cor_ratio = 80
	self.features["u_c_cor_ratio"] = cor_ratio 
	conn.close()
        

   def user_category_avg_buzz(self,category):
	conn = sqlite3.connect('../../data/quizbowl_buzz.db')
        cur = conn.cursor()
	query = "select avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.question where category = ? and user = ? group by user order by avg_buzz DESC"
        c = cur.execute(query,(category,self.user_id))
	res = c.fetchall()
	if len(res) == 0:
	#user is new, assign avg - change it later 
		avg_buzz = 80
	else:
		avg_buzz = res[0][0]
        self.features["u_c_avg_buzz"] = avg_buzz 
	conn.close()


if __name__ == "__main__":
	user_f = UserFeatureExtractor(318)
	user_f.user_category_avg_buzz("Fine Arts")
        user_f.user_category_correctness_ratio("Fine Arts")

	print "features :: ", user_f.features
	
        


