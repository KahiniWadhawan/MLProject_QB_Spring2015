# -*- coding: utf-8 -*-
import cPickle as pickle

with open('../../../data/stanford_parse_dump.txt', 'r') as fp:
    f = fp.read()
    len_file = len(f)
    
sparse_mega_dict = {}
with open('../../../data/stanford_parse_dump.txt', 'r') as fp:
    while fp.tell() < len_file:
        sparse_dict = pickle.load(fp)
        print fp.tell()
        sparse_mega_dict.update(sparse_dict)