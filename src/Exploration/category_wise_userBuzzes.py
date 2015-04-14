import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


def get_info(cat):
			
	#connect database
	conn = sqlite3.connect('../../../quizbowl_buzz.db')
	cur = conn.cursor()
	
	query = "select user, avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.id where usage != ? and category = ? group by user order by avg_buzz DESC"

	ans = cur.execute(query,("test",cat))
	avg_buzz = ans.fetchall()
	
	print len(avg_buzz)
	
	return avg_buzz

categories = ['Earth Science', 'Biology', 'Literature', 'Astronomy',
		  'Fine Arts', 'Other', 'Social Studies', 'Mathematics',
		  'Chemistry', 'Physics', 'History']

for cat in categories: 

	avg_buzz = get_info(cat)

	listx = []
	listy = []
	count = 0

	for tup in avg_buzz:
		listx.append(count)
		listy.append(tup[1])
		count += 1


	#plotting plot from x & y lists
	#plt.plot(listx,listy)
	#plt.scatter(listx,listy,c='green', alpha=0.5)
	plt.title("Normal dist - avg-buzz per user " + cat )

	plt.xlabel('avg buzz pos for a user', fontsize=18, color='red')
	plt.ylabel('frequency/no. of users for a avg buzz pos', fontsize=18, color='red')
	plt.hist(listy)
	plt.show()

