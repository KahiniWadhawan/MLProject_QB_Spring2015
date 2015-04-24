# -*- coding: utf-8 -*-
import numpy as np
from user import User
from question import Question
from collections import defaultdict
import sqlite3

    
class CategoryFeatureExtractor():
	def __init__(self, user_id, qid):
        	self.user = User(user_id)
	        self.question = Question(qid)
        	self.user_id = self.user.user_id
		self.features = defaultdict(list)

	
	def cat_subcat(self):
		conn = sqlite3.connect('../../../data/quizbowl_category.db')
	        cur = conn.cursor()
		query = "select * from category_all where Question = ?;"
		print self.question.qid
	        c = cur.execute(query,(self.question.qid,))
        	res = c.fetchall()[0]
		#print list(res)
		self.features["cat_subcat"] = list(res) 
		conn.close()



if __name__ == "__main__":
	cat_f = CategoryFeatureExtractor(1,5)
	cat_f.cat_subcat()
	print len(cat_f.features.values()[0])

    
