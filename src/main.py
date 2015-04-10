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

	pos_qid = []
	for t in train:
		if t["user"] == user:
			pos_qid.append((float(t["position"]),t["question"]))

	assert len(pos_qid) > 0, "seems like there is no user named:%s"%user
	qs_pos = []


	for q in questions:
		for i,(pos,qid) in enumerate(pos_qid):
			if q["id"] == qid:
				qs_pos.append((q,pos))

	return zip(*qs_pos)

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
	#print "qs:",len(qs)
	#print "Y:",len(Y)
	FE = FeatureExtractor()
	for q in qs:
		FE(q) # feed this FeatureExtractor with a question data
		X.append(FE.extract())

	return X,Y

def X_generator(qid,question):
	FE = FeatureExtractor()
	for q in question:
		if q["id"] == qid:
			FE(q)
			return FE.extract()


def users(samples):
	"""
	From sample set, extract user ids 
	"""
	user_ids = set()

	for s in samples:
		user_ids.add(s["user"])
	
	return user_ids

def ensemble(UserGroup,X):

	most_common = lambda lst: max(set(lst), key=lst.count)

	signs = []
	positions = []
	for u in UserGroup.keys():
		output = float(UserGroup[u].predict(X))
		signs.append(np.sign(output))
		positions.append(abs(output))

	return most_common(signs)*np.average(positions)





if __name__ == "__main__":
	train = data_import(folder_path+"/train.csv")
	questions = data_import(folder_path+"/questions.csv")

	user_ids = users(train)
	UserGroup = {}
	# user 0,100
	#X,Y = XY_generator("100",train,questions)

	
	
	for u in user_ids:
		X,Y = XY_generator(u,train,questions)
		Y_cls = map(np.sign,Y)
		Y_reg = map(abs,Y)
		user = User()
		user.fit_classifier(X, Y_cls)
		user.fit_regression(X, Y_reg)
		UserGroup[u] = user

	test = data_import(folder_path+"/test.csv")
	for t in test:
		if t["user"] in UserGroup.keys():
			result = UserGroup[t["user"]].predict(X_generator(t["question"], questions))
			print t["id"] +","+ str(result)
		else:
			result = ensemble(UserGroup,X_generator(t["question"], questions))
			print t["id"] +","+ str(result)

	



