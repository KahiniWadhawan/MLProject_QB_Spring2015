import numpy as np
import sqlite3
from csv import DictReader

"""
Scratch Pad

>>> a = np.array([1,2,3])
>>> b = np.array([4,5,6])
>>> np.concatenate((a,b))
array([1, 2, 3, 4, 5, 6])

"""
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
	def __init__(self):
		pass

	def __call__(self,question,vocab):
		self.question = question
		self.vocab = vocab

	def category(self):
		"""
		this method returns a numpy array with only one entry = 1
		whose index corresponds to a position of a given question's genre
		in a list, genres.
		"""
		conn = sqlite3.connect('../data/quizbowl_category.db')
		cur = conn.cursor()
		query = "select * from category_all where Question = ?;"
		c = cur.execute(query,(self.question["id"],))
		res = c.fetchall()[0]
		vector = list(res)[1:]
		conn.close()
		return vector


		#vector = np.zeros(len(categories))
		#vector[categories.index(self.question["category"])] = 1
		#return vector

	def text_length(self):
		return [len(self.question["text"])]

	def number_of_words(self):
		return [len(eval(self.question["words"]).values())]

	def bag_of_words(self):
		
		words = eval(self.question["words"]).values()
		vector = list(np.zeros(len(self.vocab)))

		for w in words:
			if w in self.vocab:
				vector[self.vocab.index(w)]+=1

		return vector
		
		



	def extract(self):
		# this method should return a numpy array as a X vector
		# concatenating feature vectors from other methods using
		# np.concatenate()
							  
		return np.array(self.category()+self.text_length()+self.number_of_words())

if __name__ == "__main__":
	questions = list(DictReader(open("../data"+"/questions.csv","r")))
	FE = FeatureExtractor()
	FE(questions[10])
	print len(FE.extract())

	


