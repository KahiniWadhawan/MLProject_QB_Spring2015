import numpy as np

categories = ['Earth Science', 'Biology', 'Literature', 'Astronomy',
		  'Fine Arts', 'Other', 'Social Studies', 'Mathematics',
		  'Chemistry', 'Physics', 'History']

class FeatureExtractor:
	"""
	This class FeatureExtractor is used to extract features
	of ONE question from questions.csv file. In other words, 
	this class gives us only an X vector (not Y)

	I am not sure if this works for both classification and 
	regression tasks since both may need different features.
	"""
 	def __init__(self,qid,answer,category,text):
		self.qid = qid 
		self.answer = answer 
		self.category = category
		self.text = text

	def tokenize(self,remove_stopwords=False):
		"""
		This method tokenizes the question text. It is
		method that can give all tokens, tokens w/o 
		stopwords or tokens only with important keywords. 
 		"""

		text = self.text
		tokens = [] 
		return tokens 
		

	def get_sentences():
		"""
		This method gives out list of sentences from 
		question text. The index of sentence in the 
		list is the sentence position. 
		"""
		sentences = [] 
		return sentences 
