import numpy as np
from csv import DictReader

from UserModel import User
from Features import FeatureExtractor

folder_path = "../data"

def data_import(path):
	"""
	input: a path to the .csv file you want to import
	output: a list of dict whose keys are the names of columns
	"""
	return list(DictReader(open(path,"r")))

def user_examples(user,train,questions):
	"""
	inputs: a user's id
		   training set
		   all questions

	# below may change
    output: a list of tuple consisting of a dictioanry of a question
    		and a position at which the user answered the question.
    		[(question1,position1),(question2,position2),....
    		This gives us questions a specific user answered and positions
	"""
	positions = [] 
	question_id = [] # storing question id

	for t in train:
		if t["user"] == user:
			positions.append(float(t["position"]))
			question_id.append(t["question"])

	assert len(positions) > 0, "seems like there is no user named:%s"%user
	qs = [] # storing an actual question object (dict)
	
	for q in questions:
		if q["id"] in question_id:
			qs.append(q)

	return qs,positions

def XY_generator(user,train,questions):
	"""
	inputs: a user's id
		    training set
		    all questions

	outputs:
		X, a list of numpy arrays.
			Example -> ([[1,2,3,4],
						 [5,6,7,8],
						 [9,10,11,12]])
		Y, a list of answering positions  of a user 
		    with respect to each question 
		    Example -> ([60.21, 93.32, -56.89,...])

	"""
	X = []
	Y = []
	qs,Y = user_examples(user, train, questions)

	FE = FeatureExtractor()
	for q in qs:
		FE(q) # feed this FeatureExtractor with a question data
		X.append(FE.extract())

	return X,Y

if __name__ == "__main__":
	train = data_import(folder_path+"/train.csv")
	questions = data_import(folder_path+"/questions.csv")
	X,Y = XY_generator(user="4", train=train, questions=questions)
	
	Y_cls = map(np.sign,Y)
	Y_reg = map(abs,Y)

	user = User()
	user.fit_classifier(X, Y_cls)
	user.fit_regression(X, Y_reg)

	# test code below 
	FE = FeatureExtractor()
	test = data_import(folder_path+"/test.csv")
	qs_for_user = [t["question"] for t in test if t["user"] == "4"]

	for q in questions:
		if q["id"] in qs_for_user:
			FE(q)
			X = FE.extract()
			print user.predict(X)



