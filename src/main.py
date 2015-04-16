from csv import DictReader


folder_path = "../../data"

def data_import(path):
	"""
	input: a path to the .csv file you want to import
	output: a list of dict whose keys are the names of columns
	"""
	return list(DictReader(open(path,"r")))



if __name__ == "__main__":
	pass
