import numpy as np
from csv import DictReader
from nltk.tag import pos_tag
from collections import defaultdict

from UserModel import User
from Features import FeatureExtractor
from Validation import Validation

import random

folder_path = "../data"


class Questions:

	def __init__(self,questions):
		self.Qs = questions

	def __iter__(self):
		return self.Qs

	def vocabulary_nouns(self):
		vocab_noun = set()
		i = 0
		for q in self.Qs:
			print i
			vocab = eval(q["words"]).values()
			tagged = pos_tag(vocab)
			propernouns = [word for word,pos in tagged if pos == 'NNP']
			vocab_noun = vocab_noun.union(set(propernouns))
			i += 1
		return list(vocab_noun)

	def vocabulary_no_stopwords(self):
		vocab = set()
		i = 0
		for q in self.Qs:
			print i
			vocab = vocab.union(set(eval(q["words"]).values()))
			i += 1
		return list(vocab)

def cluster_import(path):

	clusters = defaultdict(list)
	user_cluster = defaultdict(int)

	with open(path,"r") as f:
		for e in f.readlines():
			e = map(int,e.split(","))
			clusters[e[1]].append(e[0])
			user_cluster[e[0]] = e[1]
	return clusters,user_cluster


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
		FE(q,vocab,user) # feed this FeatureExtractor with a question data
		X.append(FE.extract())

	return X,Y

def X_generator(user,qid,question,vocab):
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
	train = data_import(folder_path+"/train.csv")
	
	train_splited = random.sample(train,int(len(train)*percentage))
	train_id = []
	for ts in train_splited:
		train_id.append(ts["id"])

	test_splited = []
	for t in train:
		if t["id"] not in train_id:
			test_splited.append(t)
	
	return train_splited,test_splited

def main(train=None,test=None):
	#train = data_import(folder_path+"/train.csv")
	questions = data_import(folder_path+"/questions.csv")

	#clusters,user_cluster = cluster_import("user_cluster.txt")

	
	
	"""
	Q = Questions(questions)
	print Q.vocabulary_no_stopwords()
	print len(Q.vocabulary_no_stopwords())
	nouns = Q.vocabulary_no_stopwords()
	with open("words.txt","w") as f:
		for n in nouns:
			f.write(n+"\n")
	"""
	vocab = set()
	#with open("words.txt","r") as f:
	#	for e in f.readlines():
	#		vocab.add(unicode(e[:-2]))

	vocab = list(vocab)
	
	user_ids = users(train)
	UserGroup = {}

	
	#for c in clusters.keys():
	#	user_c = User()
	#	Xs = []
	#	Y_cls_s = []
	#	Y_reg_s = []
	#	
	#	for u in clusters[c]:
	#		
	#		if str(u) not in user_ids:
	#			continue
	#		X,Y = XY_generator(u,train,questions)
	#		Y_cls = map(np.sign,Y)
	#		Y_reg = map(abs,Y)
	#		Xs += X
	#		Y_cls_s += Y_cls
	#		Y_reg_s += Y_reg
	#	
	#	user_c.fit_classifier(Xs, Y_cls_s)
	#	user_c.fit_regression(Xs, Y_reg_s)
	#	UserGroup[c] = user_c


	for u in user_ids:
		X,Y = XY_generator(u,train,questions,vocab)
		#Y_cls = map(np.sign,Y)
		#Y_reg = map(abs,Y)
		user = User()
		#user.fit_classifier(X, Y_cls)
		#user.fit_regression(X, Y_reg)
		user.fit_regression(X, Y)
		UserGroup[u] = user

	#test = data_import(folder_path+"/test.csv")

	test_splitted = [{"id":t["id"],"question":t["question"],"user":t["user"]} for t in test]
	test_Ys = [float(t["position"]) for t in test]

	predict_Y = []
	print "Going to predict...."
	for t in test_splitted:
		if t["user"] in UserGroup.keys():
		#if t["user"] in user_cluster.keys():
			#result = UserGroup[user_cluster[t["user"]]].predict(X_generator(t["question"], questions,vocab))
			result = UserGroup[t["user"]].regression_only_predict(X_generator(t["user"],t["question"], questions,vocab))
			predict_Y.append(result)
			print t["id"] +","+ str(result)
		else:
			result = ensemble(UserGroup,X_generator(t["user"],t["question"], questions,vocab))
			predict_Y.append(result)
			print t["id"] +","+ str(result)
	
	V = Validation(test_Ys,predict_Y)
	print "V.RMSE():",V.RMSE()
	print "V.Correctness():",V.Correctness()
	#V.Correctness_sign()


	





if __name__ == "__main__":
	train,test = train_test_split()
	main(train, test)
