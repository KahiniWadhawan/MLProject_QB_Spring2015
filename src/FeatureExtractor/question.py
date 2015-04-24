import numpy as np
import nltk
import sqlite3
import re
import string


stopwords = set(nltk.corpus.stopwords.words())



class Question(object):
    """
    This class is used to extract question level features
    of ONE question from questions.csv file.

    """
    def __init__(self, qid):
        self.conn = sqlite3.connect('../../../data/quizbowl_buzz.db')
        self.cur = self.conn.cursor()
        self.qid = qid
        conn = sqlite3.connect('../../../data/quizbowl_buzz.db')
        cur = conn.cursor()

        query = "select text,answer,category,words from questions where id =? "
        c = self.cur.execute(query,(qid,))
        info = c.fetchall()
        self.text = info[0][0]
        self.answer = info[0][1]
        self.category = info[0][2]
        self.words = info[0]
        self.conn.close()
        
    def __call__(self,qid):
        self.qid = qid
        query = "select text,answer,category,words from questions where id =? "
        c = self.cur.execute(query,(qid,))
        info = c.fetchall()
        self.text = info[0][0]
        self.answer = info[0][1]
        self.category = info[0][2]
        self.words = info[0]


    def tokenize(self,remove_stopwords=False, **othertext):
        """
        This method tokenizes the question text. It
        can give all tokens, tokens w/o stopwords
        or tokens that are only with important keywords.
        This gives the same as self.words, if used with
        remove_stopwords True
        """
    	if othertext:
    	    text = othertext['othertext']
    	else:
    	    text = self.text
    	    
    	tokens = []
    	#text = text.translate(None).lower()
    	text = re.sub('[%s]' % re.escape(string.punctuation), '', text.lower())
    	temp_tokens = text.split()
    	#remove stopwords
    	if remove_stopwords == True:
    	    for word in temp_tokens:
    	        if word in stopwords:
    	            pass
    	        else:
    	            tokens.append(word)
    	else:
    	    tokens = temp_tokens
    	return tokens

    def get_sentences(self):
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
    ques = Question()
    ques(1)
    ques.get_info()
    print "question text :: ", ques.text
    print "question ans :: ", ques.answer
    print "question cat :: ", ques.category
    print "question words :: ", ques.words

    print "sent :: ", len(ques.get_sentences())
    print "tokens :: ", ques.tokenize(True), len(ques.tokenize(True))
