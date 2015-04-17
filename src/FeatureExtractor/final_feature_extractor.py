# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')
import numpy as np
from user import User
from question import Question
#from parent_feature_extractor import FeatureExtractor
from user_features import UserFeatureExtractor
from question_features import QuestionFeatureExtractor




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
		q_FE = QuestionFeatureExtractor(self.question.qid)
		q_FE.caps_cumulative()
		q_FE.sentence_position()

				
		X_word_level = q_FE.features
		#X_POS[(self.qid, self.user_id)].append


		return X_POS	
		
	def co_feature_vec(self):
		"""This method combines user and question
		features and return final feature_vec,
		gives two X feature vec """	
		
		#question level features for correctness model 
		u_FE = UserFeatureExtractor()
		question.get_info()
		category = question.category
		u_FE.user_category_correctness_ratio(category)
		u_FE.user_category_avg_buzz(category)
	
		X_CO = u_FE.features.values()


		return X_CO	
	
		
			



if __name__ == "__main__":
	#test 
	qid, user_id = 1,2
	FE = FinalFeatureExtractor()
	FE(user_id,qid)


	X_word_level = FE.pos_feature_vec()
	X_POS = defaultdict(list)
	for word_pos, feat_vec in X_word_level.iteritems():
			X_POS[(qid,user_id)].append(feat_vec)


	X_CO = FE.co_feature_vec()

	print "X_POS :: ", X_POS
	print "X_CO:: ", X_CO

            
