from CorrectnessModel import CorrectnessModel
from PositionModel import PositionModel


class SuperModel:
	"""
	This SuperModel class combines CorrectnessModel and PositionModel.
	You need to feed them differently, i.e. CorrectnessModel may need 
	question level features while PositionModel may need word level features.
	"""
	def __init__(self):
		self.correctness = CorrectnessModel()
		self.position = PositionModel()

	def fit_co(self,X,Y):
		"""
		X: feature vectors. This may be questions level.
		Y: labels, which indicate whether user answered the question correctly or not.
		"""
		self.correctness.fit(X,Y)

	def fit_pos(self,X_dict,Y_dict):
		"""
		input:
			X_dict:   a dictionary whose key is a tuple of (q_id,user_id) and value is
					  a matrix of word level training data
					  Example:
					    (q_id = 1, user_id = 3) -> [[1,1,2], (word_position = 1)
					    							[4,2,4], (word_position = 2)
					    							[8,2,3]] (word_position = 3)
			Y_dict:   a dictionary whose key is a tuple of (q_id,user_id) and value is
					  position of buzzing.
					  Example:
					  	(q_id = 1, user_id = 3) -> -70

		"""
		self.position.fit(X_dict,Y_dict)

	def predict_correct(self,X):
		return self.correctness.predict(X)

	def predict_pos(self,X):
		return self.position.predict(X)

	def predict(self,X_co,X_pos):
		"""
		This method first predict position value given X_pos, and feed it to CorrectnessModel.
		CorrectnessModel then predicts the sign. After having pos and sign, this method returns
		pos*sign, which is the final prediction for one example.
		"""
		pos = self.predict_pos(X_pos)
		sign = self.predict_correct(X_co)[0]
		return pos*sign


if __name__ == "__main__":
	# add codes if you want to run some test.
	pass
