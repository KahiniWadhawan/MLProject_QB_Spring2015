import numpy as np
from csv import DictReader
from nltk.tag import pos_tag
from collections import defaultdict

from UserModel import User
from Features import FeatureExtractor
from Validation import Validation
from sklearn.feature_extraction import DictVectorizer
 
import random

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
		if t["user"] == str(user):
			pos_qid.append((float(t["position"]),t["question"]))

	assert len(pos_qid) > 0, "seems like there is no user named:%s"%user
	qs_pos = []


	for q in questions:
		for i,(pos,qid) in enumerate(pos_qid):
			if q["id"] == qid:
				qs_pos.append((q,pos))

	return zip(*qs_pos)

def user_examples_all(rowid,train,questions):
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
		if t["id"] == str(rowid):
			pos_qid.append((float(t["position"]),t["question"]))
			print "entered"
		#print "pos_qid :: ", pos_qid

	assert len(pos_qid) > 0, "seems like there is no user named:%s"%user
	qs_pos = []


	for q in questions:
		for i,(pos,qid) in enumerate(pos_qid):
			if q["id"] == qid:
				qs_pos.append((q,pos))
				
	print "qs_pos :: ", qs_pos

	return zip(*qs_pos)



#kahini 
def q_data_all(qid, questions):

	qs = {}
	for q in questions:
		if q["id"] == qid:
			qs = q

	#print "inside q_data_all ::", qs	

	return qs


def XY_generator(user,train,questions,vocab):
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
		FE(q,vocab) # feed this FeatureExtractor with a question data
		X.append(FE.extract())

	return X,Y

def XY_generator_all(train,questions,vocab):
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
	Xs = []
	Ys = []
	#qs,Y = user_examples(user, train, questions)
	count = 0	
	FE = FeatureExtractor()
	for ex in train:
		count += 1 
		#print "processing ex ", count
		user = ex["user"]
		rowid = ex["id"]
		qid = ex["question"]
		#res = user_examples_all(rowid, train, questions)
		q = q_data_all(qid, questions)
		#print "res :: ",res 
		#q = ex["question"]
		FE(q,vocab,user) # feed this FeatureExtractor with a question data
		Xs.append(FE.extract())
		Ys.append(float(ex["position"]))	
	print "lens x y ::", len(Xs), len(Ys)
		
	return Xs,Ys



def X_generator(qid,question,vocab,user):
	FE = FeatureExtractor()
	for q in question:
		if q["id"] == qid:
			FE(q,vocab,user)
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
		output = float(UserGroup[u].regression_only_predict(X))
		signs.append(np.sign(output))
		positions.append(abs(output))

	return most_common(signs)*np.average(positions)

def train_test_split(percentage=0.75):
	print "in train_test_split"
	train = data_import(folder_path+"/train.csv")
	#little data - kahini 
	#train = train[:200]	
	train_splited = random.sample(train,int(len(train)*percentage))
	train_id = []
	for ts in train_splited:
		train_id.append(ts["id"])

	test_splited = []
	for t in train:
		if t["id"] not in train_id:
			test_splited.append(t)
	
	#print train_splited
	return train_splited,test_splited

def main(train=None,test=None):
	train = data_import(folder_path+"/train.csv")
	questions = data_import(folder_path+"/questions.csv")

	vocab = None
	
	#training model - kahini
	print "training model started"
	X,Y = XY_generator_all(train,questions,vocab)
	user = User()

	vect = DictVectorizer()
	X_train = vect.fit_transform(x for x in X)

	user.fit_regression(X_train, Y)
	print "training model finished"


	test = data_import(folder_path+"/test.csv")

	test_splitted = [{"id":t["id"],"question":t["question"],"user":t["user"]} for t in test]
	print "size of test_splitted :: ", len(test_splitted)
	#test_Ys = [float(t["position"]) for t in test]
	#test_splitted = test

	
	print "Going to predict...."
	test_Xs = []
	t_ids = []

	for t in test_splitted:
		
		user_id = t["user"]
		test_Xs.append(X_generator(t["question"], questions,vocab,user_id))
		t_ids.append(t["id"])

	test_Xs_vectorized = vect.transform(x for x in test_Xs)
	predict_Y = user.regression_only_predict(test_Xs_vectorized)

	for i,y in zip(t_ids,predict_Y):
		print str(i)+","+str(y)


		
	#V = Validation(test_Ys,predict_Y)
	#print "V.RMSE():",V.RMSE()
	#print "V.Correctness():",V.Correctness()
	#V.Correctness_sign()


	





if __name__ == "__main__":
	train,test = train_test_split()
	main(train, test)
