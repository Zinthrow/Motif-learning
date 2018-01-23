# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 11:20:54 2018

@author: Alex
"""
import argparse, os, sys
import numpy as np

class MEME(self):
    def __init__(self):
        self.s = open('hw1_example2.txt','r')
        self.s = s.readlines()
        self.W = 10 # width of proposed motif subsequence
        self.L = len(s[0])-1 # Length of each sequence
        self.n = len(s)
        self.m = L-W+1 #possible starting points
        self.z = [[0]*L] #where the motif actually starts, values are binary
        self.zt = [[0]*L]
        self.p = [[],[],[],[]]
        self.pt = [[],[],[],[]]
        self.best_start = 0
    
    def letter_score(self, x, ptx):
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
                letter_score(x,ptx)
        
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
            self.p = self.pt
            self.z = self.zt
    def OOPs_start(self):
        for start in range(m):
            
            p_start(start)
            for i in s[1:][:m]:
                for j in i:
            pz_max(pt)
                
        
        