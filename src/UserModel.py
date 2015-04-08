from sklearn import svm
from sklearn.linear_model import Ridge

class User:
	"""
	An instance of this class User has two attributes, clf and reg.
	clf: Classifier object (default = SVM) 
	reg: Regression object (default = Ridge Linear Regression)

	"""
	def __init__(self,Classifier=svm.SVC(),Regression=Ridge()):
		self.clf = Classifier
		self.reg = Regression

	def fit_classifier(self,X,Y):
		self.clf.fit(X,Y)

	def fit_regression(self,X,Y):
		self.reg.fit(X,Y)

	def predict(self,X):
	
		sign = self.clf.predict(X)
	
		if sign[0] > 0:
			sign = ""
		else:
			sign = "-"
		pos = self.reg.predict(X)

		return str(sign)+str(pos)
