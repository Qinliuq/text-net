#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 15 16:18:08 2017

@author: qinliu

This file contains functions related to network generation for a given 
(local/Gutenberg online) text file.
"""

import nltk
import numpy as np
from nltk import word_tokenize
from urllib import request

def generate_net(L,threshold):
    """
    The function takes a tokenized word list and generates a corresponding 
    weighted network.
    
    ******
    Input: 
    L
    The tokenized word list of a book(a python list of word in original order)
    
    threshold
    Bigrams lower than the threshold will be disgarded.
    
    ******
    Output: network.txt
    A .txt file that contains the network generated based on the specified book.
   
    """
    
    bgs = nltk.bigrams(L)
    fdist = nltk.FreqDist(bgs)
    
    bgs_freq = [(k,v) for (k,v) in fdist.items()]
    thresh_bgs_freq = [item for item in bgs_freq if (item[1]>=threshold and item[1]<200)]
    thresh_bgs = [item[0] for item in thresh_bgs_freq]
    words = [item[0] for item in thresh_bgs] + [item[1] for item in thresh_bgs]
    unique = list(set(words))
    
    n = len(unique)
    mat = np.zeros((n,n))
    net = []
    
    for i,word_x in enumerate(unique):
        for j,word_y in enumerate(unique):
            if (word_x,word_y) in thresh_bgs:
                location = thresh_bgs.index((word_x,word_y))
                mat[i][j] = thresh_bgs_freq[location][1]
                net.append((i,j,mat[i][j]))
                print(i,j,mat[i][j])
            else:
                pass
    with open('network.txt','w') as netfile:
        for line in net:
            netfile.write(str(line[0])+','+str(line[1])+','+str(line[2])+'\n')
    with open('unique.txt','w') as textfile:
        for word in unique:
            textfile.write(str(word)+'\n')

def from_gutenberg(file_id,threshold):
    """
    The function generates a weighted network for one Gutenberg project book.
    
    *********
    Input: file_id
    The index of one book in the Gutenberg project. For example,the index for
    Sense and Sensibility by Jane Austen is 21839.
    
    *********
    Output: 
    network.txt
    A .txt file that contains the network generated based on the specified book.
   
    threshold
    Bigrams lower than the threshold will be disgarded.
    """    
    url = 'http://www.gutenberg.org/files/'+str(file_id)+'/'+str(file_id)+'.txt'
    response = request.urlopen(url)
    raw = response.read().decode('utf8')
    txt = word_tokenize(raw)
    L = [word.lower() for word in txt]
    
    generate_net(L,threshold)
    

def from_text(file,threshold):
    """
    The function generates a weighted network for one text file (onely English
    has been tested).
    
    *********
    Input: file
    One plain text file in English.
    
    *********
    Output: 
    network.txt
    A .txt file that contains the network generated based on the specified book.
   
    threshold
    Bigrams lower than the threshold will be disgarded.
    """       
    my_corpus = nltk.corpus.PlaintextCorpusReader(file)
    txt = [item for item in my_corpus.words(file)]
    L = [word.lower() for word in txt]
    
    generate_net(L,threshold)
    
def from_text_cn(file,threshold):
    """
    The function generates a weighted network for one Chinese text file.
    
    *********
    Input: 
    file
    One plain text file in Chinese.
    
    *********
    Output: 
    network.txt
    A .txt file that contains the network generated based on the specified book.
    
    threshold
    Bigrams lower than the threshold will be disgarded.
    """      
    my_corpus = nltk.corpus.PanLexLiteCorpusReader(file)
    phrases = [item for item in my_corpus.words(file)]
    characters = [[char for char in item] for item in phrases]
    
    generate_net(characters,threshold)
