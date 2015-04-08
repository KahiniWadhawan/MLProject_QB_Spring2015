import numpy as np

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

	def __call__(self,question):
		self.question = question

	def category(self):
		"""
		this method returns a numpy array with only one entry = 1
		whose index corresponds to a position of a given question's genre
		in a list, genres.
		"""
		vector = np.zeros(len(categories))
		vector[categories.index(self.question["category"])] = 1
		return vector

	def extract(self):
		# this method should return a numpy array as a X vector
		# concatenating feature vectors from other methods using
		# np.concatenate()
		return self.category()

