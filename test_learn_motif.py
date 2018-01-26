# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:20:54 2018
@author: Alex
"""

import argparse, os, sys
import numpy as np

class MEME():
    def __init__(self):
        self.motif = {}
        self.background = {}
        self.s = open('hw1_example2.txt','r')
        self.s = self.s.readlines()
        self.W = 10 # width of proposed motif subsequence
        self.L = len(self.s[0])-1 # Length of each sequence
        self.n = len(self.s)
        self.m = self.L-self.W+1 #possible starting points
        self.z = [[0]*(self.m)] #matrix for motif starts, values are binary
        self.zt = [[0]*(self.m)]
        self.p = [] #current best probability
        self.pt = [] #probability table -temporary
        self.delta_p = np.zeros((4,self.W+1))
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
        self.pt = np.ones((4,W+1))
        for num, x in enumerate(self.s[0]):
            if num < start or num >= start + W:
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
        self.pt[0][0] = (bA+1)/(m+3)
        self.pt[1][0] = (bT+1)/(m+3)
        self.pt[2][0] = (bG+1)/(m+3)
        self.pt[3][0] = (bC +1)/(m+3)        
        
    def pz_max(self): #if the temp p-matrix "pt" is better than "p", update "p"
        if self.p is []:
            self.p = np.ones((4,self.W+1))
        p_transp = np.transpose(self.p)
        pt_transp = np.transpose(self.pt)
        p_score = 0
        pt_score = 0
        
        for a in p_transp[1:]:
            p_score += max(a)
            
        for b in pt_transp[1:]:
            pt_score += max(b)
            
        if pt_score > p_score:
            self.p = np.array(self.pt)
            self.z = np.array(self.zt)
            
    def z_set(self,e_temp, y, prob):
        if prob is self.pt:
            prob = self.zt
        else:
            prob = self.z
        W = self.W
        L = self.L
        e_max = np.argmax(e_temp)
        prev_e = np.argmax(prob[y])
        prob[y][prev_e] = 0
        prob[y][e_max] = 1
        self.motif[y] = self.s[y][e_max:(e_max+W)]
        if e_max == 0:
            self.background[y] = self.s[y][e_max+W:L]
        elif e_max > 0:
            self.background[y] = self.s[y][0:e_max] + self.s[y][e_max+W:L]
    
    
        
    def expectation(self,y,i,prob):
        e_temp = [] #Expectation values of EM algorithm
        for x,j in enumerate(i):
            W = self.W
            e_score = 1
            for ind, c in enumerate(self.s[y][:self.m]):
                if ind < x or ind > (x+W):
                    if c == 'A':
                        e_score = e_score*prob[0][0]
                    elif c == 'T':
                        e_score = e_score*prob[1][0]
                    elif c == 'G':
                        e_score = e_score*prob[2][0]
                    elif c == 'C':
                        e_score = e_score*prob[3][0]
                elif ind > x and ind < (x+W):
                    if c == 'A':
                        e_score = e_score*prob[0][ind-x]
                    elif c == 'T':
                        e_score = e_score*prob[1][ind-x]
                    elif c == 'G':
                        e_score = e_score*prob[2][ind-x]
                    elif c == 'C':
                        e_score = e_score*prob[3][ind-x]
            e_temp.append(e_score)
        self.z_set(e_temp, y, prob)
        
    def maximization(self,y,seq, prob):
        W = self.W
        if seq is self.background:
            A = 0
            T = 0
            G = 0
            C = 0
            total = 0
            for seq_num in range(y):
                if prob is self.pt:
                    seq_num += 1
                current = seq[seq_num]
                for x in current:
                    if x == 'A':
                        A += 1
                    elif x == 'T':
                        T += 1
                    elif x == 'G':
                        G += 1
                    elif x == 'C':
                        C += 1
                    total += 1
            
            prob[0][0] = (A+1)/(total+3)
            prob[1][0] = (T+1)/(total+3)
            prob[2][0] = (G+1)/(total+3)
            prob[3][0] = (C+1)/(total+3)
        elif seq is self.motif:
            matrix_count = np.zeros((5,W)) #matrix counting A T G C & total
            for seq_num in range(y):
                if prob is self.pt:
                    seq_num += 1
                current = seq[seq_num]
                for motif_pos,x in enumerate(current):
                    if x == 'A':
                        matrix_count[0][motif_pos] += 1
                    elif x == 'T':
                        matrix_count[1][motif_pos] += 1
                    elif x == 'G':
                        matrix_count[2][motif_pos] += 1
                    elif x == 'C':
                        matrix_count[3][motif_pos] += 1
                    matrix_count[4][motif_pos] += 1
            for x in range(4):
                for stat in range(self.W): #stat is the index of next p_value
                    p_val = (matrix_count[x][stat]+1)/(matrix_count[4][stat]+4)
                    self.delta_p[x][stat+1] = abs(1-(prob[x][stat+1]/p_val))
                    prob[x][stat+1] = p_val
                    
    def percent_stats(self):
        run = True
        stop_row =[]
        for row in self.delta_p:
            stop_row.append(max(row))
        if max(stop_row) <= .005:
            run = False
        return run
            
    def OOPS_start(self):
        m = self.m
        for start in range(m):
            self.p_start(start)
            if start > 0:
                self.zt[0][np.argmax(self.zt[0])] = 0
                self.zt[0][start] = 1
            else:
                self.zt[0][start] = 1
            for y,i in enumerate(self.s[1:]):
                y += 1
                if start < 1:
                    self.zt.append([0]*m)
                self.expectation(y,i,self.pt)
                self.maximization(y,self.motif, self.pt)
                self.maximization(y,self.background, self.pt)
            self.pz_max()
        print ('starting position decided')
        print (self.p)
        
    def OOPS_complete(self):
        run = True
        while run:
            for y,i in enumerate(self.s):
                self.expectation(y,i,self.p)
                self.maximization(y,self.motif,self.p)
                self.maximization(y,self.background, self.p)
                run = self.percent_stats()
            
                
    def OOPS(self):
        self.OOPS_start()
        #self.OOPS_complete()
            
        
meme = MEME()
meme.OOPS()
        
