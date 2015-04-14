import numpy as np
from sklearn.linear_model import SGDClassifier
from CorrectnessModel import CorrectnessModel
from PositionModel import PositionModel


class SuperModel:
	def __init__(self):
		self.correctness = CorrectnessModel()
		self.position = PositionModel()

	def fit_co(self,X,Y):
		self.correctness.fit(X,Y)

	def fit_pos(self,X,Y):
		self.position.fit(X,Y)

	def predict_correct(self,X,pos):
		return self.correctness.predict(X,pos)

	def predict_pos(self,X):
		return self.position.predict(X)

	def predict(self,X_co,X_pos):
		pos = self.predict_pos(X_pos)
		sign = self.predict_correct(X_co,pos)
		return pos*sign


if __name__ == "__main__":
