import numpy as np
import nltk
import sqlite3


stopwords = set(nltk.corpus.stopwords.words())



class Question:
	"""
	This class is used to extract question level features
	of ONE question from questions.csv file.

	"""
 	def __init__(self,qid,answer,category,text):

		self.qid = qid
		
		#call get info to get other fields 
		info = get_info(self.qid)

 		self.text = info["text"]
		self.answer = info["answer"]
		self.category = info["category"]
		self.words = info["words"]

			
	def get_info(self,qid):
		"""This method will return info of question like 
		text, answer, category and words. It return info 
		dict that has string text as key and its actual value, 
		string answer as key and value, string category as key 
		and value and string words as key and value(words dict) """
		
		info = {}
		
		#connect database
		conn = sqlite3.connect('quizbowl_buzz.db')
		c = conn.cursor()
		
		#get question text 
		query = "select text from questions where id = " + qid 		
		text = cur.execute(query)
		info["text"] = text		

		#get answer 
		query = "select answer from questions where id = " + qid 		
		answer = cur.execute(query)
		info["answer"] = answer	

		#get category 
		query = "select category from questions where id = " + qid 		
		category = cur.execute(query)
		info["category"] = category	

		#get words 
		query = "select words from questions where id = " + qid 		
		words = cur.execute(query)
		info["words"] = words
	
		return info


	def tokenize(self,remove_stopwords=False):
		"""
		This method tokenizes the question text. It
		can give all tokens, tokens w/o stopwords 
		or tokens that are only with important keywords. 
 		"""
		text = self.text
		tokens = [] 

 		text = text.translate(None, string.punctuation).lower()
		#ques = re.sub('[%s]' % re.escape(string.punctuation), '', ques)

		temp_tokens = text.split()
		
		#remove stopwords 
		if remove_stopwords == True:
			for word in temp_tokens:
				if word in stopwords:
					pass
				else:
					tokens.append(word)
		else:
			tokens = temp_tokens()

		return tokens 
		

	def get_sentences():
		"""
		This method gives out list of sentences from 
		question text. The index of sentence in the 
		list is the sentence position. 
		"""

		#separates an article into sentences 
		sentence_finder = re.compile(r"""
	        # Split sentences on whitespace between them.
        	(?:               # Group for two positive lookbehinds.
	          (?<=[.!?])      # Either an end of sentence punct,
        	| (?<=[.!?]['"])  # or end of sentence punct and quote.
	        )                 # End group of two positive lookbehinds.
        	(?<!  Mr\.   )    # Don't end sentence on "Mr."
	        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        	(?<!  Jr\.   )    # Don't end sentence on "Jr."
	        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        	(?<!  Prof\. )    # Don't end sentence on "Prof."
	        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        	(?<!  U\.S\.   )    # Don't end sentence on "U.S"
	        \s+               # Split on whitespace between sentences.
        	""", 
	        re.IGNORECASE | re.VERBOSE)

		sentences = []

		sentences = sentence_finder.split(self.text)
		 
		return sentences 


		
