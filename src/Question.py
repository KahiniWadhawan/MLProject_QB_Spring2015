import numpy as np
import nltk
import sqlite3


stopwords = set(nltk.corpus.stopwords.words())



class Question:
	"""
	This class is used to extract question level features
	of ONE question from questions.csv file.

	"""
 	def __init__(self,qid):

		self.qid = qid
		
			
	def get_info(self):
		"""This method will return info of question like 
		text, answer, category and words as a dict."""
		
		info = {}
		qid = self.qid
		
		#connect database
		conn = sqlite3.connect('../../data/quizbowl_buzz.db')
		cur = conn.cursor()
		
		query = "select text,answer,category,words from questions where id =? " 		
		c = cur.execute(query,(qid,))
		res = c.fetchall()
		info["text"] = res[0][0]
		info["answer"] = res[0][1]
		info["category"] = res[0][2]
		info["words"] = res[0][3]

		self.text = info["text"]
		self.answer = info["answer"]
		self.category = info["category"]
		self.words = info["words"]
		conn.close()
	
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


	

if __name__ == "__main__":
	ques = Question(1)
	ques.get_info()
	print "question text :: ", ques.text


	
	
