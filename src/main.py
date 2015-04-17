import sys
sys.path.insert(0, '../')

from collections import defaultdict
from csv import DictReader
from FeatureExtractor.final_feature_extractor import FinalFeatureExtractor

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
                X_POS is a dict:- key: (qid,uid), value: matrix 
			of word level features for each entry in 
			train & test 
		
		X_CO is conventional feature vec


		Y, a list of answering positions  of a user 
		    with respect to each question 
		    Example -> ([60.21, 93.32, -56.89,...])

	"""
	X_POS = defaultdict(list)
	X_CO = []
	Y = []
	#qs,Y = user_examples(user, train, questions)

	FE = FinalFeatureExtractor()
	for ex in train:
		user_id = ex["user"]
		qid = ex["question"]
		FE(user_id,qid)

		X_word_level = FE.pos_feature_vec() #you will get 2 X
	
		for word_pos, feat_vec in X_word_level.iteritems():
			X_POS[(qid,user_id)].append(feat_vec)


		X_CO.append(FE.co_feature_vec())
		
		Y.append(ex["position"])  


	return X_POS, X_CO, Y


if __name__ == "__main__":

	train = data_import(folder_path+"/train.csv")
	#questions = data_import(folder_path+"/questions.csv")
	X,Y = XY_generator(train=train)



