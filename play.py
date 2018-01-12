# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

s = open('hw1_example2.txt','r')
s = s.readlines()
num = 5100

A = 0
T = 0
G = 0
C = 0
count = 0

for x in s:
    for y in x:
        if y == 'A':
            A +=1
        elif y == 'C':
            C += 1
        elif y == 'G':
            G += 1
        elif y == 'T':
            T += 1
    count += 1

print (A/num,C/num,G/num,T/num)
        

s = open('hw1_example2_model.txt','r')
s = s.read()
print (len(s))
'''
s = open('hw1_example2_positions.txt','r')
s = s.read()
print (len(s))

s = open('hw1_example2_subsequences.txt','r')
s = s.read()
print (len(s))
'''