#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:20:09 2017

@author: qinliu
"""

import generate_net as gn
import community as cm

"""
Generate a network from gutenberg online sources. "1" is the id of
The Declaration of Independence. "10" is the threshold which means
we only consider words appears more than 10 times.

This line could run hours long. 10 is proper threshold, but if one wants
an fine network, the threshold should be lower.

Output: 'network.txt' (numbers),'unique.txt'(words)
"""
gn.from_gutenberg(1,10) 



"""
Find communities in a network. The 'network.txt' is the output file from gn functions.

The function community() works better but cost much longer (>48 hrs on a workstation).
"""
cm.community_fast_file('network.txt')




"""
Find similar context words for an input word based on community structure. 

One community could contain ambiguous words and other non-specific words like 'the','of'

The output here for the following line:
 [['supreme'],
 ['government'],
 ['most'],
 ['legislature'],
 ['president'],
 ['congress'],
 ['united'],
 ['at'],
 ['world'],
 ['union'],
 ['people'],
 ['same'],
 ['from'],
 ['under'],
 ['senate'],
 ['law'],
 ['first'],
 ['on']]
There're still some non-specific words, primarily because:
    1. The Declaration of Independence is a short file. 
    The algorithm works better on large text bodies.
    2. A threshold value embedded in the script. The value is set
    purely based on my experience.
"""
cm.similar_context('law','network.txt')

"""
Find ambiguous words. Didn't find any in The Declaration of Independence.

Could find some in large files, but works very slow.
"""
cm.ambgt_dectect('network.txt')


