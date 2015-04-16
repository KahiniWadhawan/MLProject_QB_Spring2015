import sys
sys.path.insert(0, '../')

import numpy as np
from csv import DictReader
from UserModel import User
from Features import FeatureExtractor

folder_path = "../../data"


def data_import(path):
	"""
	input: a path to the .csv file you want to import
	output: a list of dict whose keys are the names of columns
	"""
	return list(DictReader(open(path,"r")))


def XY_generator(train):
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
	#qs,Y = user_examples(user, train, questions)

	FE = FinalFeatureExtractor()
	for ex in train:
		user_id = ex["user"]
		qid = ex["question"]
		FE(user_id,qid)

		X.append(FE.feature_vec())
		Y.append(ex["position"])  


	return X,Y


if __name__ == "__main__":

	train = data_import(folder_path+"/train.csv")
	#questions = data_import(folder_path+"/questions.csv")
	X,Y = XY_generator(train=train)



