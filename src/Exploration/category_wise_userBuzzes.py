import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sqlite3


def get_info():
			
	#connect database
	conn = sqlite3.connect('quizbowl_buzz.db')
	cur = conn.cursor()
	
	query = "select user, avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.id where usage = ? and category = ? group by user order by avg_buzz DESC"

	ans = cur.execute(query,("train","Earth Science"))
	avg_buzz = ans.fetchall()
	
	print avg_buzz
	return avg_buzz



avg_buzz = get_info()

listx = []
listy = []
count = 0

for tup in avg_buzz:
	listx.append(count)
	listy.append(tup[1])
	count += 1


#plotting plot from x & y lists
#plt.plot(listx,listy)
plt.scatter(listx,listy,c='green', alpha=0.5)
plt.title("avg-buzz per user Earth Science")

plt.xlabel('user id', fontsize=18, color='black')
plt.ylabel('avg buzz', fontsize=18, color='black')
plt.show()

