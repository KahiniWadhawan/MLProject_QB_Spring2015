from csv import DictReader
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

filename = "/Users/maverickreclci/Desktop/drivers/3612/1.csv"

def data_import(filename):
        # input: the location of .csv file as a string. E.g."drivers/1/1.csv"
        # output: a list of tuple, [(x1,y1),(x2,y2),....]
        data = list(DictReader(open(filename,"r")))
        x = [(float(e["x"])) for e in data]
	y = [(float(e["y"])) for e in data]
        return x,y

x_y_lists = data_import(filename)
listx = x_y_lists[0]
listy = x_y_lists[1]

#plotting plot from x & y lists
plt.plot(listx,listy)
#plt.scatter(listx,listy,c='green', alpha=0.5)


plt.xlabel('x-coordinate', fontsize=18, color='black')
plt.ylabel('y-coordinate', fontsize=18, color='black')
plt.show()



