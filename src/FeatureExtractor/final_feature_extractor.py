# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')
import numpy as np
from user import User
from question import Question
#from parent_feature_extractor import FeatureExtractor
from user_features import UserFeatureExtractor
from question_features import QuestionFeatureExtractor
from collections import defaultdict




class FinalFeatureExtractor():

	def __init__(self):
		pass

	def __call__(self, user_id, qid):
                self.user_id = user_id
		self.qid = qid
	
		self.user = User(user_id)
	        self.question = Question(qid)
		

	
	def pos_feature_vec(self):
		"""This method combines user and question
		features and return final feature_vec,
		gives two X feature vec """	
		
		#word - level features for position model	
		q_FE = QuestionFeatureExtractor()
		q_FE(self.question.qid)
		q_FE.caps_cumulative()
		q_FE.sentence_position()
		q_FE.part_of_speech()
		q_FE.NER()


		if not q_FE.features == None:
			X_word_level = q_FE.feat_vectorizer(q_FE.features)
		else:
			print "passed: ", self.question.qid
			return None


		return X_word_level	
		
	def co_feature_vec(self):
		"""This method combines user and question
		features and return final feature_vec,
		gives two X feature vec """	
		
		#question level features for correctness model 
		u_FE = UserFeatureExtractor(self.user_id)
		category = self.question.category
		u_FE.user_category_correctness_ratio(category)
		u_FE.user_category_avg_buzz(category)
	
		X_CO = u_FE.features.values()


		return X_CO	
	
		
			



if __name__ == "__main__":
	#test 
	X_POS = defaultdict(list)
	X_CO = [] 
	
	ex = [(1,2),(1,0)]
	FE = FinalFeatureExtractor()
	for tup in ex: 
		qid = tup[0]
		user_id = tup[1]
		FE(user_id,qid)
		print "hello :: ",qid, user_id 

		X_word_level = FE.pos_feature_vec()
		if X_word_level == None:
			continue
		for word_pos, feat_vec in X_word_level.iteritems():
			X_POS[(qid,user_id)].append(feat_vec)

	
		X_CO.append(FE.co_feature_vec())
	
	print "X_POS :: ", X_POS
	print "X_CO:: ", X_CO
	print "keys :: ", X_POS.keys()
	for val in X_POS.values():
		print "len of x pos words :: ", len(val)
            
