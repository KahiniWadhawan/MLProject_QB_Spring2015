import numpy as np
import sqlite3
from csv import DictReader

"""
Scratch Pad

>>> a = np.array([1,2,3])
>>> b = np.array([4,5,6])
>>> np.concatenate((a,b))
array([1, 2, 3, 4, 5, 6])

"""
categories = ['Earth Science', 'Biology', 'Literature', 'Astronomy',
		  'Fine Arts', 'Other', 'Social Studies', 'Mathematics',
		  'Chemistry', 'Physics', 'History']

def dictionarize(name,vector):
	d = {}
	for i in range(len(vector)):
		d[name+":"+str(i)] = vector[i]

	return d

class FeatureExtractor:
	"""
	This class FeatureExtractor is used to extract features
	of ONE question from questions.csv file. In other words, 
	this class gives us only an X vector (not Y)

	I am not sure if this works for both classification and 
	regression tasks since both may need different features.
	"""
	def __init__(self):
		pass

	def __call__(self,question,vocab,user):
		#print "question :: ", question
		self.question = question
		self.vocab = vocab
		#kahini 
		self.user = user

	def u_subcat(self):
		"""
		This gives user sub-category cor_ratio for each question   
		"""
		conn = sqlite3.connect('../data/quizbowl_user.db')
		cur = conn.cursor()
		query = "select * from u_subcat where user = ? and question = ? ;"
		#print "hello :: " , self.question[0]
		c = cur.execute(query,(self.user, self.question["id"])) 
		#c = cur.execute(query,(self.question,))
		res = c.fetchall()[0]
		#print "user features :: ", res
		vector = list(res)[2:]
		#print "cat and feat :: ", self.question["id"], self.question["category"], vector
		conn.close()
		return dictionarize("u_subcat", vector)



	def user_features(self):
		"""
		This gives user category cor_ratio an avg buzz 
		"""
		conn = sqlite3.connect('../data/quizbowl_user.db')
		cur = conn.cursor()
		query = "select * from user_features where user = ? and category = ? ;"
		#print "hello :: " , self.question[0]
		c = cur.execute(query,(self.user, self.question["category"])) 
		#c = cur.execute(query,(self.question,))
		res = c.fetchall()[0]
		#print "user features :: ", res
		vector = list(res)[2:]
		#print "cat and feat :: ", self.question["id"], self.question["category"], vector
		conn.close()
		return dictionarize("user_features", vector)

	def f(self,a,N):
    		return np.argsort(a)[::-1][:N]

	def top_subcat_cor_ratio(self,top=4):
		
		conn = sqlite3.connect('../data/quizbowl_category.db')
		cur = conn.cursor()
		cat =  self.question["category"].replace(" ","")
		table = "cat_" + cat
		query = "select * from " + table +  " where Question = ?"
		c = cur.execute(query,(self.question["id"],)) 
		res = c.fetchall()[0]
		#print "res :: ", res 
		vector = list(res)[1:]
		#sorted(vector, reverse = True)
		#t =  f(vector,top)
		top_topics = [cat + "_" + str(e) for e in self.f(vector,top)] 
		#print top_topics
	
		#cor ratio of top subcat 
		conn = sqlite3.connect('../data/quizbowl_user.db')
		cur = conn.cursor()
		cols = " " 
		for i in xrange(len(top_topics)):
			if i == 0:
				cols += top_topics[i]
			else:
				cols += ", " + top_topics[i]

		query = "select " + cols +  " from user_only_subcat where user = ?"
		#print "query :::", query
		c = cur.execute(query,(self.user,)) 
		res = c.fetchall()[0]
		vector = list(res)
		#print vector	
		conn.close()
	
		return dictionarize("top_subcat_cor_ratio", vector)

	def user_only_subcat(self):
		"""
		This gives user category cor_ratio an avg buzz 
		"""
		conn = sqlite3.connect('../data/quizbowl_user.db')
		cur = conn.cursor()
		query = "select * from user_only_subcat where user = ? ;"
		#print "hello :: " , self.question[0]
		c = cur.execute(query,(self.user,)) 
		#c = cur.execute(query,(self.question,))
		res = c.fetchall()[0]
		#print "user features :: ", res
		vector = list(res)[1:]
		#print "vector :: ",vector
		conn.close()
		return dictionarize("user_only_subcat", vector)



	def category(self):
		"""
		this method returns a numpy array with only one entry = 1
		whose index corresponds to a position of a given question's genre
		in a list, genres.
		"""
		conn = sqlite3.connect('../data/quizbowl_category.db')
		cur = conn.cursor()
		query = "select * from category_all where Question = ?;"
		#print "hello :: " , self.question[0]
		c = cur.execute(query,(self.question["id"],)) 
		#c = cur.execute(query,(self.question,))
		res = c.fetchall()[0]
		vector = list(res)[1:]
		conn.close()
		return dictionarize("category", vector)


		#vector = np.zeros(len(categories))
		#vector[categories.index(self.question["category"])] = 1
		#return vector

	def text_length(self):
		return dictionarize("text_length", [len(self.question["text"])])

	def number_of_words(self):
		return dictionarize("number_of_words",[len(eval(self.question["words"]).values())])

	def bag_of_words(self):
		d = {}
		words = eval(self.question["words"]).values()
		for w in words:
			d[w] = d.get(w, 0) + 1
		return d
		
		



	def extract(self):
		# this method should return a numpy array as a X vector
		# concatenating feature vectors from other methods using
		# np.concatenate()
							  
		#return np.array(self.category()+self.text_length()+\
		#				self.number_of_words()+self.user_features()+\
		#				self.top_subcat_cor_ratio())
		d_all = {}
		for d in [self.category(),self.text_length(),self.number_of_words(),\
				  self.user_features(),self.top_subcat_cor_ratio(),self.bag_of_words()]:
			d_all.update(d)

		return d_all

if __name__ == "__main__":
	questions = list(DictReader(open("../data"+"/questions.csv","r")))
	FE = FeatureExtractor()
	FE(questions[10],"43","")
	print FE.extract()
	
	


