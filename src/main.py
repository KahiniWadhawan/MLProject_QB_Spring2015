import sys
sys.path.insert(0, '../')

from collections import defaultdict
from csv import DictReader
import random

from FeatureExtractor.final_feature_extractor import FinalFeatureExtractor
from Models.SuperModel import SuperModel
from Validation import Validation


folder_path = "../../data"


def data_import(path):
	"""
	input: a path to the .csv file you want to import
	output: a list of dict whose keys are the names of columns
	"""
	return list(DictReader(open(path,"r")))


def XY_generator(train_or_test,Y_flag=True):
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
	if Y_flag:Y = defaultdict(int)

	count = 0 
	FE = FinalFeatureExtractor()
	for ex in train_or_test:
		count += 1
		#print "count :: ", count
		row_id = ex["id"]
		user_id = ex["user"]
		qid = ex["question"]
		#print "user id , qid :: ", user_id, qid
		FE(user_id,qid)

		X_word_level = FE.pos_feature_vec()
	
		for word_pos, feat_vec in X_word_level.iteritems():
			X_POS[row_id].append(feat_vec)

		X_CO[row_id] = FE.co_feature_vec()
		
		if Y_flag:Y[row_id] = float(ex["position"])
	
	if Y_flag:
		
		return X_POS, X_CO, Y
	else:
		
		return X_POS,X_CO


def train_test_split(percentage=0.75):
	train = data_import(folder_path+"/little_train.csv")
	print "IMPORTED TRAIN DATA"
	X_POS, X_CO, Y = XY_generator(train)
	print "GENERATED FEATURE X_POS, X_CO AND Y"
	ex_ids = X_POS.keys()
	
	train_ids = random.sample(ex_ids,int(len(train)*percentage))
	test_ids = [i for i in ex_ids if i not in train_ids]
	
	train_X_POS = {i:X_POS[i] for i in train_ids}
	train_X_CO = {i:X_CO[i] for i in train_ids}
	train_Y = {i:Y[i] for i in train_ids}

	test_X_POS = {i:X_POS[i] for i in test_ids}
	test_X_CO = {i:X_CO[i] for i in test_ids}
	test_Y = {i:Y[i] for i in test_ids}

	return train_X_POS,train_X_CO,train_Y,test_X_POS,test_X_CO,test_Y


def testing():
	train_X_POS,train_X_CO,train_Y,test_X_POS,test_X_CO,test_Y =  train_test_split()
	
	super_model = SuperModel()
	super_model.fit_co(train_X_CO, train_Y)
 	super_model.fit_pos(train_X_POS, train_Y)

 	predicted_Ys = {}

 	for ex_id in test_Y.keys():
 		predicted_Ys[ex_id] = super_model.predict(test_X_CO[ex_id],test_X_POS[ex_id])
 		
 	V = Validation(test_Y,predicted_Ys)
 	print V.MSE()
 	print V.worst_ten()




def main():
	train = data_import(folder_path+"/little_train.csv")
	print "IMPORTED TRAIN DATA"
	X_POS, X_CO, Y = XY_generator(train)
	print "GENERATED FEATURE X_POS, X_CO AND Y"


 	super_model = SuperModel()
 	super_model.fit_co(X_CO, Y)
 	super_model.fit_pos(X_POS, Y)

 	test = data_import(folder_path+"/little_test.csv")
 	print "IMPORTED TEST DATA"
 	X_POS_test,X_CO_test = XY_generator(test, Y_flag=False)
 	print "GENERATED FEATURE X_POS AND X_CO"

 	print "------"*10
 	print "id,position"
 	for ex_id in X_POS_test.keys():
 		print ex_id + "," + str(super_model.predict(X_CO_test[ex_id], X_POS_test[ex_id]))






if __name__ == "__main__":
	#main()
	testing()
	
	
	




