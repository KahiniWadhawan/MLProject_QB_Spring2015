import os
from csv import DictReader

folder_path = "../../drivers"

class DataManipulation(object):

    def __init__(self, folder_path="../../drivers"):
        # input: the path of the data folder
        self.folder_path = folder_path   

    def data_driver(self,name="1"):
        # input: the name of a driver (string)
        # output: a dictionary whose key is a trip and value is a list of coordinates (tuple)
        #         so overall 200 trips

        self.trips = {}
        path = self.folder_path+"/"+str(name)+"/"

        for f in os.listdir(path):
            data = list(DictReader(open(path+f,"r")))
            x_y = [(float(e["x"]),float(e["y"])) for e in data]
            self.trips[f[:-4]] = x_y

        return self.trips

    def data_all(self):
        # this method imports all data so may take some time 
        # output -> dict of dict: {drive1:{trip1:[(x1,y1),(x2,y2),...],trip2:[...]},driver2:...}
        self.all = {}

        for driver in os.listdir():
            self.all[driver] = self.data_driver(name=driver)

        return self.all
   
    def plot_helper(self,trip="1"):
        driver = self.data_driver(name="1")
        x = [x for x,y in driver[trip]]
        y = [y for x,y in driver[trip]]
        return x,y

def main():
    Data = DataManipulation(folder_path)
    driver_trip =  Data.data_driver("1")
    x_y = driver_trip["1"] # notice that when you access a dict, key is a string ("1", "2", etc.)
    print x_y  	


if __name__ == "__main__":
	main()