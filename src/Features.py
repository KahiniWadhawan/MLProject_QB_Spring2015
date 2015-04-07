
number_of genre = 11

class FeatureExtractor:
	"""
	This class FeatureExtractor is used to extract features
	of ONE question from questions.csv file. In other words, 
	this class gives us only an X vector (not Y)

	I am not sure if this works for both classification and 
	regression tasks since both may need different features.
	"""
	def __init__(self,question):
		self.questions = question
	
	def extract():
		# this method should return a numpy array as a X vector
		pass