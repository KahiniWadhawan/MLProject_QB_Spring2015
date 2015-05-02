from sklearn.linear_model import Ridge,Lasso,SGDClassifier
from sklearn import svm
from sklearn.svm import SVR


class User:
	"""
	An instance of this class User has two attributes, clf and reg.
	clf: Classifier object (default = Stochastic Gradient Decsent Logreg) 
	reg: Regression object (default = Ridge Linear Regression)
	Classifier=SGDClassifier(loss='log', penalty='l2', shuffle=True)
	Classifier=svm.SVC()
	SVR(kernel='rbf')
	"""
	def __init__(self,Classifier=SGDClassifier(loss='hinge', penalty='l2', shuffle=True),
				 Regression=Lasso()):
		self.clf = Classifier
		self.reg = Regression
		self.one_class = False

	def fit_classifier(self,X,Y):
		if len(set(Y)) == 1:
			self.one_class = True
			self.Y = Y
		else:
			self.clf.fit(X,Y)

	def fit_regression(self,X,Y):
		self.reg.fit(X,Y)

	def predict(self,X):

		if self.one_class:
			sign = self.Y
		else:
			sign = self.clf.predict(X)
		
		if sign[0] > 0:
			sign = 1.0
		else:
			sign = -1.0
		pos = self.reg.predict(X)

		return sign*pos
	def regression_only_predict(self,X):
		return self.reg.predict(X)
