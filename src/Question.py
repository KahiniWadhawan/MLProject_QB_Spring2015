import numpy as np


class Question:
	"""
	This class is used to extract question level features
	of ONE question from questions.csv file.

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
