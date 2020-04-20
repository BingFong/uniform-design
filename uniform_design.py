# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 18:06:44 2019

@author: CILAB
"""
#import pandas as pd
import math
from glob import glob
from os.path import join

import numpy as np
from numpy import genfromtxt

#def design(table):
#    list_columns = [int(x)-1 for x in input('column:').split()]
#    print(list_columns, '\n')
#    uniform_table = table[:, list_columns]
#    return uniform_table

def udt_combination():
    """ different combinations of UDT columns """
    global N, S
    
    rows = int(math.factorial(N)/ (math.factorial(S) * math.factorial(N-S)))
    columns = np.zeros((rows, S), dtype=np.intp)
    col_list = list()

    for i in range(S):
        col_list.append(i)

    col_count = 0
    while col_list[S-1] < N: #while the last element smaller than N, meaning end of the loop
        columns[col_count] = col_list
        col_count += 1
        print(col_list)

        col_list[-1] += 1

        if col_list[S-1] == N:
            for i in reversed(range(S-1)):
                if col_list[i]+1 <= N-S+i:
                    col_list[i] += 1
                    while i < (S-1):
                        col_list[i+1] = col_list[i]+1
                        i += 1
                    break;
    return columns
    

def uniform_design_table(modulo_table):
    """ generate default and modulo table """
    global N
    col = list() #record avaible columns

    for i in range(N): #compute greatest common divisor of every column and N(experiment number)
        if math.gcd(i, N) == 1:
            col.append(i)

    for i in col:
        if i == 1:
            uni_table = np.array([modulo_table[:, 0]])
        else:
            uni_table = np.concatenate((uni_table, np.array([modulo_table[:, i-1]])), axis=0)

    uni_table = uni_table.T

    with np.printoptions():
        print("\nU({},{}):".format(N, len(col)))
        print(uni_table)

    return uni_table

def table():
    """ generate default and modulo table """
    global N
    default_table = np.zeros((N, N-1), dtype=np.intp) #default uniform design table
    modulo_table = np.zeros((N, N-1), dtype=np.intp) #record columns of UDT that after modulo operation
    for i in range(N):
        for j in range(N-1):
            default_table[i, j] = (i+1) * (j+1)
            modulo_table[i, j] = default_table[i, j] % N #modulo operation
            if modulo_table[i, j] == 0:
                modulo_table[i, j] = N

    with np.printoptions():
        print("U({},{}):".format(N, N-1))
        print(default_table)

    with np.printoptions():
        print("\nU({},{}) after using modulo:".format(N, N-1))
        print(modulo_table)

    return default_table, modulo_table

if __name__ == '__main__':
    N = 9
    S = 5
    DEFAULT_TABLE, MODULO_TABLE = table()
    UDT = uniform_design_table(MODULO_TABLE)
    UDT_COMBINATION = udt_combination()

#    uniform_table = design(table)
#    print("uniform design table:\n",uniform_table, '\n')

#    scheme = np.ndarray((uniform_table.shape[0], uniform_table.shape[1]), dtype='f')
#    for file in glob(join('*.csv')):
#        csv = genfromtxt(file, delimiter = ',', skip_header = 1)
#        for i in range(csv.shape[0]):
#            for j in range(csv.shape[1]):
#                scheme [i, j] = csv[uniform_table[i, j]-1, j]
