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
import cmath

#def design(table):
#    list_columns = [int(x)-1 for x in input('column:').split()]
#    print(list_columns, '\n')
#    uniform_table = table[:, list_columns]
#    return uniform_table

def cd2_evaluate(udt, udt_combination, N, S):
    """ CD2 """
    record = np.ndarray((udt_combination.shape[0],), dtype=np.complex_)
    print(record.shape)
    for i in range(udt_combination.shape[0]):
        udt_cd2 = np.reshape(udt[:, udt_combination[i, 0]], (N, 1))
        for j in range(1, S):
            udt_cd2 = np.append(udt_cd2, np.reshape(udt[:, udt_combination[i, j]], (N, 1)), axis=1)
    
        with np.printoptions():
            print("\nudt_cd2_{}".format(i))
            print(udt_cd2)
        
        p1 = math.pow((13/12), S)
        p2 = p3 = 0
        f2 = f3 = 1

        for m in range(N):
            for n in range(S):
                f2 *= (1 + 0.5*(abs(udt_cd2[m, n] - 0.5)) - 0.5*(math.pow(abs(udt_cd2[m, n] - 0.5), 2)))
            p2 += f2
            f2 = 1
        p2 = 2/N*p2
                    
        for m in range(N):
            for k in range(N):
                for n in range(S):
                    f3 *= (1 + 0.5*(abs(udt_cd2[m, n] - 0.5)) + 0.5*(abs(udt_cd2[k, n] - 0.5)) - 0.5*(abs(udt_cd2[m, n] - udt_cd2[k, n])))
                p3 += f3
                f3 = 1
        p3 = 1/(N*N)*p3
        
        cd2 = cmath.sqrt(p1-p2+p3)
        print(cd2)
        record[i] = cd2

    print('min cd2:', min(record))
    with np.printoptions():
#            print("\nudt_cd2_{}".format(np.argmin(record)))
            print(udt_combination[np.argmin(record)])
    
                
def udt_combination():
    """ different combinations of UDT columns """
    global S
    
    udt_col = udt.shape[1]
    
    max_rows = int(math.factorial(udt_col) / (math.factorial(S) * math.factorial(udt_col-S)))
    columns = np.zeros((max_rows, S), dtype=np.intp)
    col_list = list(range(S))

    count = 0
    while col_list[S-1] < udt.shape[1]: #stop when combinations genarated
        columns[count] = col_list
        count += 1
        print('col_list', col_list)

        col_list[-1] += 1

        if col_list[S-1] == udt.shape[1]:
            for i in reversed(range(S-1)):
                if col_list[i]+1 <= udt.shape[1]-S+i:
                    col_list[i] += 1
                    while i < (S-1):
                        col_list[i+1] = col_list[i]+1
                        i += 1
                    break;
    return columns
    

def uniform_design_table(modulo_table):
    """ generate UDT """
    global N
    col = list() 

    for i in range(N):
        if math.gcd(i, N) == 1:
            col.append(i-1)
    uni_table = modulo_table[:, col]

    with np.printoptions():
        print("\nU({},{}) UDT:".format(N, len(col)))
        print(uni_table, '\n')

    return uni_table


def table():
    """ generate default and modulo table """
    global N
    default_table = np.zeros((N, N-1), dtype=np.intp) #default uniform design table
    modulo_table = np.zeros((N, N-1), dtype=np.intp) #record cols of UDT after modulo operation
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
    N = 7
    S = 4
    default_table, modulo_table = table()
    udt = uniform_design_table(modulo_table)
    udt_combination = udt_combination()
    
    cd2_evaluate(udt, udt_combination, N, S)

    
            
#    uniform_table = design(table)
#    print("uniform design table:\n",uniform_table, '\n')

#    scheme = np.ndarray((uniform_table.shape[0], uniform_table.shape[1]), dtype='f')
#    for file in glob(join('*.csv')):
#        csv = genfromtxt(file, delimiter = ',', skip_header = 1)
#        for i in range(csv.shape[0]):
#            for j in range(csv.shape[1]):
#                scheme [i, j] = csv[uniform_table[i, j]-1, j]
