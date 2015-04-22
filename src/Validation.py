from __future__ import division
import math

class Validation:

	def __init__(self,true_Ys,predicted_Ys):
		"""
		input: true_Ys -> a dictionary whose key is example id and value is 
						  correct Y value.
		       predicted_Ys -> the same as one above except values are predicted.
		"""
		self.true = true_Ys
		self.predicted = predicted_Ys

	def RMSE(self):
		""" Root Mean Square Error"""

		p = [] # predicted values
		t = [] # true values

		for k in self.true.keys():
			p.append(self.predicted[k])
			t.append(self.true[k])

		return math.sqrt(sum([(y1-y2)**2 for (y1,y2) in zip(p,t)])/len(t))

	def worst_ten(self):
		return sorted([(k,(self.predicted[k]-self.true[k])**2)for k in self.true.keys()],
					  key= lambda (k,diffence):diffence,)[-10:]





if __name__ == "__main__":

	a = {"a":10,"b":25,"c":-45}
	b = {"a":17,"b":20,"c":-40}
	V = Validation(a,b)
	print V.MSE()
	print V.worst_ten()
