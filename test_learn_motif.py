# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:20:54 2018
@author: Alex
"""

import argparse, os, sys
import numpy as np

class MEME():
    def __init__(self):
        self.s = open('hw1_example2.txt','r')
        self.s = self.s.readlines()
        self.W = 10 # width of proposed motif subsequence
        self.L = len(self.s[0])-1 # Length of each sequence
        self.n = len(self.s)
        self.m = self.L-self.W+1 #possible starting points
        self.z = [[0]*self.L] #where the motif actually starts, values are binary
        self.zt = [[0]*self.L]
        self.p = [[],[],[],[]] #current best probability
        self.pt = [[],[],[],[]] #probability table -temporary
        self.best_start = 0
    
    def start_score(self, x, ptx):
        if x == 'A':
            self.pt[0][ptx] = .7
            self.pt[1][ptx] = .1
            self.pt[2][ptx] = .1
            self.pt[3][ptx] = .1
            
        elif x == 'T':
            self.pt[0][ptx] = .1
            self.pt[1][ptx] = .7
            self.pt[2][ptx] = .1
            self.pt[3][ptx] = .1
            
        elif x == 'G':
            self.pt[0][ptx] = .1
            self.pt[1][ptx] = .1
            self.pt[2][ptx] = .7
            self.pt[3][ptx] = .1   
            
        elif x == 'C':
            self.pt[0][ptx] = .1
            self.pt[1][ptx] = .1
            self.pt[2][ptx] = .1
            self.pt[3][ptx] = .7
    
    def p_start(self,start):
        bA = 0
        bT = 0
        bG = 0
        bC = 0
        ptx = 0
        W = self.W
        m = self.m
        for x in self.pt:
            x = [0]*(W+1)
        
        for num, x in enumerate(self.s[0]):
            if num < start or num > start + W:
                if x == 'A':
                    bA += 1
                elif x == 'T':
                    bT += 1
                elif x == 'G':
                    bG += 1
                elif x == 'C':
                    bC += 1
            elif num >= start and num <= start + W:
                ptx += 1
                self.start_score(x,ptx)
        
        self.pt[0][0] = (bA+1)/(m+4)
        self.pt[1][0] = (bT+1)/(m+4)
        self.pt[2][0] = (bG+1)/(m+4)
        self.pt[3][0] = (bC +1)/(m+4)        
        
    def pz_max(self): #if the temp p matrix pt is better than p, update
        p_transp = np.transpose(self.p)
        pt_transp = np.transpose(self.pt)
        p_score = 0
        pt_score = 0
        for a,b in p_transp,pt_transp:
            p_score += max(a)
            pt_score += max(b)
            
        if pt_score > p_score:
            self.p = np.array(self.pt)
            self.z = np.array(self.zt)
    
    def expectation(self, x, y):
        '''motif = self.s[y][x:(x+self.W)]
        if x == 0:
            background = self.s[y][x+self.W:self.L]
        elif x > 0:
            background = self.s[y][0:x] + self.s[y][x+self.W:self.L]'''
        W = self.W
        e_score = 1
        for ind, c in enumerate(self.s[y]):
            if ind < x or ind > (x+W):
                if c == 'A':
                    e_score = e_score*self.pt[0][0]
                elif c == 'T':
                    e_score = e_score*self.pt[1][0]
                elif c == 'G':
                    e_score = e_score*self.pt[2][0]
                elif c == 'C':
                    e_score = e_score*self.pt[3][0]
            elif ind > x and ind < (x+W):
                if c == 'A':
                    e_score = e_score*self.pt[0][ind-x]
                elif c == 'T':
                    e_score = e_score*self.pt[1][ind-x]
                elif c == 'G':
                    e_score = e_score*self.pt[2][ind-x]
                elif c == 'C':
                    e_score = e_score*self.pt[3][ind-x]
       
        return e_score
            
    def OOPs_start(self):
        for start in range(self.m):
            if start > 0:
                self.zt[0][start-1] = 0
                self.zt[0][start] = 1
            else:
                self.zt[0][start] = 1
            self.p_start(start)
            for y,i in enumerate(self.s[1:][:self.m]):
                e_temp = [] #Expectation values of EM algorithm
                if start < 1:
                    self.zt.append([0]*(self.L))
                for x,j in enumerate(i):
                    e_temp.append(self.expectation(x,y))
            self.pz_max(self.pt)
                
        
