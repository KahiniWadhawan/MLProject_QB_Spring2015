import sys
sys.path.insert(0, '../')

from collections import defaultdict
from csv import DictReader
from FeatureExtractor.final_feature_extractor import FinalFeatureExtractor
import cPickle as pickle
from Models.SuperModel import SuperModel


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





if __name__ == "__main__":
	train = data_import(folder_path+"/little_train.csv")
	print "IMPORTED TRAIN DATA"
	X_POS, X_CO, Y = XY_generator(train)
	print "GENERATED FEATURE X_POS, X_CO AND Y"

	#with open('pos_feature_vec_dump.txt', 'wb') as fz:
	#	pickle.dump(X_POS, fz)
	#with open('co_feature_vec_dump.txt', 'wb') as f:
	#	pickle.dump(X_CO, f)
	#with open('y_dump.txt', 'wb') as fy:
	#	pickle.dump(Y, fy)

	#with open('pos_feature_vec_dump.txt', 'rb') as f:
 	#	X_POS = pickle.load(f)
 	#with open('co_feature_vec_dump.txt', 'rb') as f:
 	#	X_CO = pickle.load(f)
 	#with open('y_dump.txt', 'rb') as f:
 	#	Y = pickle.load(f)


 	super_model = SuperModel()
 	super_model.fit_co(X_CO, Y)
 	super_model.fit_pos(X_POS, Y)

 	test = data_import(folder_path+"/little_test.csv")
 	print "IMPORTED TEST DATA"
 	X_POS_test,X_CO_test = XY_generator(test, Y_flag=False)
 	print "GENERATED FEATURE X_POS AND X_CO"

 	for ex_id in X_POS_test.keys():
 		print ex_id + "," + str(super_model.predict(X_CO_test, X_POS_test))




