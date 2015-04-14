import numpy as np
from sklearn.linear_model import SGDClassifier
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

	def fit_pos(self,X,Y):
		"""
		X: feature vectors. This may be WORD level. The index of the feature vectors should 
		    correspond to word_position. 
		Y: labels. Elements are all 1s after the position of buzzing. (e.g. [0,0,0,1,1...])
		"""
		self.position.fit(X,Y)

	def predict_correct(self,X,pos):
		return self.correctness.predict(X,pos)

	def predict_pos(self,X):
		return self.position.predict(X)

	def predict(self,X_co,X_pos):
		"""
		This method first predict position value given X_pos, and feed it to CorrectnessModel.
		CorrectnessModel then predicts the sign. After having pos and sign, this method returns
		pos*sign, which is the final prediction for one example.
		"""
		pos = self.predict_pos(X_pos)
		sign = self.predict_correct(X_co,pos)
		return pos*sign


if __name__ == "__main__":
	# add codes if you want to run some test.
	pass
