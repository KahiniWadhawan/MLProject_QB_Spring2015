
from sklearn.linear_model import SGDClassifier


class PositionModel:

	def __init__(self,classifier=SGDClassifier(loss='log',penalty='l2',shuffle=True)):
		self.clf = classifier

	def fit(self,X_dict,Y_dict):
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
		
		Xs = []
		Ys = []
		Y_generator = lambda length,pos: [0 if i < pos-1 else 1 for i in range(length)]

		for key in X_dict.keys():

			X = X_dict[key]
			len_question = len(X)

			Y = Y_generator(len_question,abs(Y_dict[key]))
			Xs += X
			Ys += Y

		self.clf.fit(Xs,Ys)

	def predict(self,X):
		"""
		This method returns the index of label with the highest confidence
		(index = word_position).
		So when using this method, fix the pair of question_id and user_id,
		otherwise this method returns meaningless result.
		"""
		labels = self.clf.decision_function(X)
		return list(labels).index(max(labels))

if __name__ == "__main__":
	pos = PositionModel()
	X = {(1,1):[[1,2,3],
				[3,2,4],
				[7,6,9]],

		 (5,8):[[6,2,3],
				[5,2,4],
				[2,6,9]]}
				
	Y = {(1,1):-1,(5,8):2}
	pos.fit(X,Y)

	print pos.predict([[4,5,2],
				 	   [7,1,1],
				 	   [8,8,4]])











	