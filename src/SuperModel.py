import numpy as np
from sklearn.linear_model import SGDClassifier


class SuperModel:
	def __init__(self):
		self.correctness = CorrectnessModel()
		self.position = PositionModel()

	def fit_co(self,X,Y):
		self.correctness.fit(X,Y)

	def fit_pos(self,X,Y):
		self.position.fit(X,Y)

	def predict_correct(self,X):
		return self.correctness.predict(X)

	def pos_probability(self,X):
		return self.position.probability(X)


class CorrectnessModel:
	
	def __init__(self,Classifier_co=SGDClassifier(loss='log',penalty='l2',shuffle=True)):
		self.clf_co = Classifier_co

	def fit(self,X,Y):
		self.clf_co.fit(X,Y)

	def predict(self,X):
		return self.clf_co.predict(X)

class PositionModel:
	
	def __init__(self,Classifier_pos=SGDClassifier(loss='log',penalty='l2',shuffle=True)):
		self.clf_pos = Classifier_pos

	def fit(self,X,Y):
		self.clf_pos.fit(X,Y)

	def predict(self,X):
		return self.clf_pos.predict(X)

	def probability(self,X):
		"""
		This method gives the probability that the label is '1' given
		the example X.
		"""
		d = self.clf_pos.decision_function(X)[0]
		return np.exp(d) / (1 + np.exp(d))

if __name__ == "__main__":

	Pos = PositionModel()

	X = [[0,0,0,2,3],
		 [0,0,1,2,5],
		 [1,2,0,0,1],
		 [2,3,1,0,0],
		 [8,0,1,0,0],
		 [1,1,1,3,6]]

	Y = [0,0,1,1,1,0]

	Pos.fit(X, Y)

	T = [1,0,2,1,1]
	print Pos.predict(T)
	print Pos.probability(T)
