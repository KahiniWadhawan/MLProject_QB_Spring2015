from __future__ import division
import math
import numpy as np

class Validation:

	def __init__(self,true_Ys,predicted_Ys):
		
		self.true = true_Ys
		self.predicted = predicted_Ys

	def RMSE(self):
		""" Root Mean Square Error"""
		return math.sqrt(sum([(y1-y2)**2 for (y1,y2) in zip(self.true,self.predicted)])/len(self.true))

	def Correctness(self):
		result = [1 if np.sign(x) == np.sign(y) else 0 for x,y in zip(self.true,self.predicted)]
		return sum(result)/len(result)

	def Correctness_sign(self):
		true_plus = [t for t in self.true if np.sign(t) > 0]
		predict_plus = [p for p in self.predicted if np.sign(p) > 0]
		print "Ratio of plus in true values:",len(true_plus)/len(self.true)
		print "Ratio of plus in predicted values:",len(predict_plus)/len(self.predicted)

	




if __name__ == "__main__":

	a = {"a":10,"b":25,"c":-45}
	b = {"a":17,"b":20,"c":-40}
	V = Validation(a,b)
	print V.RMSE()
	
