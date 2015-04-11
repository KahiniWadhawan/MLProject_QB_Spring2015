# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 16:26:47 2015

@author: manjhunathkr
"""
import sqlite3, os
from matplotlib import pyplot as plt


class Exploration(object):
    def __init__(self):
        os.chdir('../../data')
        self.conn = sqlite3.connect('quizbowl_buzz3.db')
        self.cur = self.conn.cursor()
    
    def ques_per_cat(self):
        query = "select category, count(*) as count from questions where usage != 'test' group by category order by count DESC "
        c = self.cur.execute(query,)
        data = c.fetchall()
        X = [z[0] for z in data]
        Y = [z[1] for z in data]
        plt.bar(range(len(Y)), Y, align='center')
        plt.xticks(range(len(X)), X, size='small', rotation='vertical')
        plt.title("Questions per Category")
        plt.show()
        
        print "\n\n"

    def user_per_cat(self):
        query = "select category, count(distinct user) as count from questions q JOIN train t ON q.id = t.id where usage != 'test'  group by category order by count DESC "
        c = self.cur.execute(query,)
        data = c.fetchall()
        X = [z[0] for z in data]
        Y = [z[1] for z in data]
        plt.bar(range(len(Y)), Y, align='center')
        plt.xticks(range(len(X)), X, size='small', rotation='vertical')
        plt.title("Unique users per Category")
        plt.show()
        #print c.fetchall()
        print "\n\n"
        
    def cat_avg_buzz_pos(self):
        query = "select category, avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.id where usage != 'test'  group by category order by avg_buzz DESC "
        c = self.cur.execute(query,)
        data = c.fetchall()
        X = [z[0] for z in data]
        Y = [z[1] for z in data]
        plt.bar(range(len(Y)), Y, align='center')
        plt.xticks(range(len(X)), X, size='small', rotation='vertical')
        plt.title("Avg. Buzz position per Category")
        plt.show()
        #print c.fetchall()
        print "\n\n"
        
    def user_avg_buzz_pos(self):
        query = "select user, avg(abs(position)) as avg_buzz from questions q JOIN train t ON q.id = t.id where usage != 'test'  group by user order by avg_buzz DESC"
        c = self.cur.execute(query,)
        data = c.fetchall()
        X = [z[0] for z in data]
        Y = [z[1] for z in data]
        plt.bar(range(len(Y)), Y, align='center')
        plt.xticks(range(len(X)), X, size='small', rotation='vertical')
        plt.title("Avg. Buzz position per User")
        plt.show()
        #print c.fetchall()
        print "\n\n"
        
    def cat_correctness_ratio(self):
        query = "select category, (sum(CASE WHEN position > 0 THEN 1.0 ELSE 0.0 END)/count(t.id)) as cor_ratio from questions q JOIN train t ON q.id = t.id where usage != 'test'  group by category order by cor_ratio DESC "
        c = self.cur.execute(query,)
        data = c.fetchall()
        X = [z[0] for z in data]
        Y = [z[1] for z in data]
        plt.bar(range(len(Y)), Y, align='center')
        plt.xticks(range(len(X)), X, size='small', rotation='vertical')
        plt.title("Correctness ratio per Category")
        plt.show()
        #print c.fetchall()
        print "\n\n"
        
if __name__ == "__main__":
    e = Exploration()
    e.ques_per_cat()
    e.user_per_cat()
    e.cat_avg_buzz_pos()
    e.user_avg_buzz_pos()
    e.cat_correctness_ratio()