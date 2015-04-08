from csv import DictReader
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
	input: a user's id
		   training set
		   all questions

    output: a list of tuple consisting of a dictioanry of a question
    		and a position at which the user answered the question.
    		[(question1,position1),(question2,position2),....
    		This gives us questions a specific user answered and positions
	"""
	positions = [] 
	question_id = [] # storing question id

	for t in train:
		if t["user"] == user:
			positions.append(t["position"])
			question_id.append(t["question"])

	assert len(positions) > 0, "seems like there is no user named:%s"%user
	qs = [] # storing an actual question object (dict)

	for q in questions:
		if q["id"] in question_id:
			qs.append(q)

	return zip(qs,positions)


if __name__ == "__main__":
	train = data_import(folder_path+"/train.csv")
	questions = data_import(folder_path+"/questions.csv")
	eg_0 = user_examples("0", train, questions)
	print len(eg_0)
	print eg_0[2]

	FE = FeatureExtractor(questions[1000])
	print FE.category()


