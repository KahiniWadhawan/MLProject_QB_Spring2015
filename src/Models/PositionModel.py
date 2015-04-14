from sklearn.linear_model import SGDClassifier


class PositionModel:

	def __init__(self,classifier=SGDClassifier(loss='log',penalty='l2',shuffle=True)):
		self.clf = classifier

	def fit(self,features,labels):
		self.clf.fit(features,labels)

	def predict(self,features):
		"""
		This method returns the index of label with the highest confidence
		(index = word_position).
		So when using this method, fix the pair of question_id and user_id,
		otherwise this method returns meaningless result.
		"""
		labels = self.clf.decision_function(features)
		print labels
		return list(labels).index(max(labels))

if __name__ == "__main__":
	X = [[1,1],
		 [2,1],
		 [1,4],
		 [5,6],
		 [4,4],
		 [3,7]]

	Y = [0,0,0,1,1,1]

	test = [[1,3],
		    [2,3],
		    [2,4],
		    [6,8],
		    [4,4],
		    [5,7]]

	pos = PositionModel()
	pos.fit(X,Y)

	print pos.predict(test)

