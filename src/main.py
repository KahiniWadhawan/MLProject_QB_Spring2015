import sys
sys.path.insert(0, '../')

from collections import defaultdict
from csv import DictReader
from FeatureExtractor.final_feature_extractor import FinalFeatureExtractor
import cPickle as pickle


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
	X_CO = defaultdict(list)
	Y = defaultdict(int)

	count = 0 
	FE = FinalFeatureExtractor()
	for ex in train:
		count += 1
		print "count :: ", count
	        row_id = ex["id"]
		user_id = ex["user"]
		qid = ex["question"]
		print "user id , qid :: ", user_id, qid
		FE(user_id,qid)

		X_word_level = FE.pos_feature_vec()
	
		for word_pos, feat_vec in X_word_level.iteritems():
			X_POS[row_id].append(feat_vec)

		X_CO[row_id] = FE.co_feature_vec()
		
		Y[row_id] = float(ex["position"])


	return X_POS, X_CO, Y


if __name__ == "__main__":

	train = data_import(folder_path+"/train.csv")
	X_POS, X_CO, Y = XY_generator(train=train)

	with open('pos_feature_vec_dump.txt', 'wb') as fz:
		pickle.dump(X_POS, fz)

	fz.close()


	with open('co_feature_vec_dump.txt', 'wb') as f:
		pickle.dump(X_CO, f)

	f.close()


