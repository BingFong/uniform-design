# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:06:44 2019

@author: CILAB
"""
#import pandas as pd
import numpy as np
import math
from numpy import genfromtxt

from glob import glob
from os.path import join

def design(table):
    list_columns = [int(x)-1 for x in input('column:').split()]
    print(list_columns, '\n')
    union_table = table[:,list_columns]
    return union_table
    
def table(n, s):
    de_table = np.ndarray((n, s), dtype=np.intp)
    uni_cols = np.ndarray((n, s), dtype=np.intp) #record columns of UDT that after using modulo 
    for i in range(n):
        for j in range(s):
            de_table[i, j] = (i+1) * (j+1)
            uni_cols[i, j] = de_table[i, j] % n
            if uni_cols[i, j] == 0:
                uni_cols[i, j] = n
                
    
    with np.printoptions():
        print("U_{}_{}:".format(n, s))
        print(de_table)
        
    with np.printoptions():
        print("\nU_{}_{} after using modulo:".format(n, s))
        print(uni_cols)
    
    # generate maximum avaible columns of UDT
    col = list() #record avaible columns
    for i in range(n): #compute the greatest common divisor of every column and N(experiment number)
        if math.gcd(i, n) == 1:
            col.append(i)
    
    for i in col:
        if i == 1:
            uni_table = np.array([uni_cols[:,0]])
        else:
            uni_table = np.concatenate((uni_table, np.array([uni_cols[:,i-1]])), axis=0)
            
    uni_table = uni_table.T
    
    with np.printoptions():
        print("\nU_{}_{}:".format(n, len(col)))
        print(uni_table)
        
    return uni_table

def is_default():
#    n = int(input('n = '))
    n = 12
    s = n-1
    return n, s        

if __name__ == '__main__':
    N, S = is_default()
    table = table(N, S)
#    union_table = design(table)
#    print("uniform design table:\n",union_table, '\n')
    
#    scheme = np.ndarray((union_table.shape[0], union_table.shape[1]), dtype='f')
#    for file in glob(join('*.csv')):
#        csv = genfromtxt(file, delimiter = ',', skip_header = 1)
#        for i in range(csv.shape[0]):
#            for j in range(csv.shape[1]):
#                scheme [i, j] = csv[union_table[i, j]-1, j]
    