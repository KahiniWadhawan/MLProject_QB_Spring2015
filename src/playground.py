from csv import DictReader
from collections import defaultdict
from networkx.algorithms import bipartite
import networkx as nx

folder_path = "../data"

def data_import(path):
	"""
	input: a path to the .csv file you want to import
	output: a list of dict whose keys are the names of columns
	"""
	return list(DictReader(open(path,"r")))

def user_category_edges(train,question,user):
	
	categories = defaultdict(int)

	for t in train:
		if t["user"] == user:
			for q in question:
				if q["id"] == t["question"]:
					categories[q["category"]] += 1
					break
	return categories

def Bipartite(user,category,edge_list):

    B = nx.Graph() # Bipartite Graph
    B.add_nodes_from(user,bipartite=0)
    B.add_nodes_from(category,bipartite=1)
    B.add_edges_from(edge_list)

    return B

def get_edges():
	users = set()
	category = set()
	edges = []

	with open("user_categories.txt","r") as f:
		for e in f.readlines():
			print e
			u,c,w = e.split(",")
			users.add(u)
			category.add(c)
			edges.append((u,c,int(w)))

	return list(users),list(category),edges

def my_weight(G, u, v, weight='weight'):
    w = 0
    for nbr in set(G[u]) & set(G[v]):
        w += G.edge[u][nbr].get(weight, 1) + G.edge[v][nbr].get(weight, 1)
    return w


def main1():
	users,categories,edges = get_edges()
	non_weighted_e = [(e[0],e[1]) for e in edges]
	B = Bipartite(users,categories,non_weighted_e)

	for u,v in B.edges():
		for e in edges:
			if (e[0] == u) and (e[1] == v):
				w = e[2]
		B.edge[u][v]["weight"] = w

	projected_B = bipartite.generic_weighted_projected_graph(B,users,weight_function=my_weight)

	with open("projected_user.txt","w") as f:
		for i,j in projected_B.edges_iter():
			f.write(str(i)+ "," + str(j) +","+ str(projected_B[i][j]["weight"]) +"\n")


def main2():
	train = data_import(folder_path+"/train.csv")
	question = data_import(folder_path+"/questions.csv")

	users = set()

	for t in train:
		users.add(t["user"])

	with open("user_categories.txt","w") as f:
		for u in users:
			result = user_category_edges(train, question, u)
			for k in result.keys():
				f.write(u+","+k+","+str(result[k])+"\n")


if __name__ == "__main__":
	main1()
	




