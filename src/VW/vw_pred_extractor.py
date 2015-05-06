# -*- coding: utf-8 -*-
from collections import defaultdict
from csv import writer
import cPickle as pickle
import re

class WritePredictions(object):
    ''' class to write predictions from VW output'''
    def __init__(self, folder_path, predictions):
        self.predictions = predictions
        self.folder_path = folder_path
        self.get_first_index()
        self.get_count()
        self.guesses = {}
        
    def get_count(self):
        self.count_1 = {}
        self.count_2 = {}
        self.count_3 = {}
        
        for item in predictions:
            self.count_1[item] = predictions[item].values().count(1)
            self.count_2[item] = predictions[item].values().count(2)
            self.count_3[item] = predictions[item].values().count(3)
        
    def get_first_index(self):
        self.index_1 = {}
        self.index_2 = {}
        self.index_3 = {}
        for item in self.predictions:
            if 1 in self.predictions[item].values():
                self.index_1[item] = self.predictions[item].values().index(1)

            else:
                self.index_1[item] = len(self.predictions[item])
                
            if 2 in self.predictions[item].values():
                self.index_2[item] = self.predictions[item].values().index(2)

            else:
                self.index_2[item] = len(self.predictions[item])
                
            if 3 in self.predictions[item].values():
                self.index_3[item] = self.predictions[item].values().index(3)

            else:
                self.index_3[item] = len(self.predictions[item])

    def write_predictions_based_on_first_index(self):
        for item in self.predictions:
            if self.index_1[item] < self.index_3[item]:
                self.guesses[item] = self.index_1[item]
            elif self.index_3[item] < self.index_1[item]:
                self.guesses[item] = -self.index_3[item]
            else:
                self.guesses[item] = len(self.predictions[item]) -1
                
        w = writer(open(self.folder_path + 'guesses_first_index.csv', 'wb'))
        w.writerow(["id", "position"])
        for key, value in self.guesses.items():
            w.writerow([key, value])
            
    def write_predictions_based_on_count(self):
        for item in self.predictions:
            if self.count_1[item] > self.count_3[item]:
                self.guesses[item] = self.index_1[item]
            elif self.count_3[item] > self.count_1[item]:
                self.guesses[item] = -self.index_3[item]
            else:
                self.guesses[item] = len(self.predictions[item]) -1

        
                
        w = writer(open(self.folder_path + 'guesses_count.csv', 'wb'))
        w.writerow(["id", "position"])
        sorted_keys = sorted(self.guesses.keys())
        for key in sorted_keys:
            w.writerow([key, self.guesses[key]])



if __name__ == "__main__":
    
    folder_path = '../../../predictions/vw_trial8/'
    pred_file_name = 'pred_pos_validation_ngram2.txt'
    predictions = defaultdict(dict)
    
    with open(folder_path+ pred_file_name, 'r') as fp:
        for line in fp:
            res =  line.split()
            predicted_label = float(res[0])
            predicted_id = res[1].split('_')
            predictions[int(predicted_id[0])][int(predicted_id[1])] = predicted_label


            
            
    with open(folder_path + re.sub('.txt', '.pkl', pred_file_name), 'w') as fp:
        pickle.dump(predictions, fp)
        
    wp = WritePredictions(folder_path, predictions)
    wp.write_predictions_based_on_count()