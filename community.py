#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 12 11:24:10 2017

@author: Qin Liu

The file contains functions related to get communities from a given network.
Packages bct (Brain Connectivity Toolbox) and networkx are required.

"""

import networkx as nx
import csv
import bct
import sys

#sys.path.append('/Users/qinliu/Desktop/2017')

def community(file):
    """
    *******
    The function uses Girvan-Newman algorithm to get communities from a given network.
    Packages bct (Brain Connectivity Toolbox) and networkx are required. Slow (>48 hrs
    for one book) but accurate than community_fast() function.

    *******
    input: file
        .txt file that contains the network.
        format: u,v,weight
    *******
    output: 
    communities: 
        N*1 np.ndarray
    Q-metric: 
        the measure of modularity for networks
    """
    
    net = generate_netx(file)
    n_edges = nx.number_of_edges(net)
    Q_best = 0
    while n_edges > 1:
        #Calculate the betweenness for each edge. The output is a dictionary.
        edge_betweenness = nx.edge_betweenness_centrality(net,weight='weight')
        #get the edge(s) with max edge betweenness and remove it(them)
        max_values = max(edge_betweenness.values())
        for key,value in edge_betweenness.items():
            if float(value) == max_values:
                net.remove_edge(key[0],key[1])
        n_edges = nx.number_of_edges(net)
        #transform the network into a numpy array
        AM = nx.to_numpy_matrix(net)
        #utilize bct.modularity_dir() function to get community structure and calculate the Q-metric
        #for current network
        [ci,Q] = bct.modularity_dir(AM)
        #update the best Q value if needed
        if Q>Q_best:
            Q_best = Q
            ci_best = ci
        else:
            pass
    
    words = print_com('unique.txt')
    ci_best = [[words[i] for i in ci] for ci in ci_best]
    
    return ci_best,Q_best

def community_fast_file(file):
    """
    *******
    The function uses Girvan-Newman algorithm to get communities from a given 
    network file.
    It works faster than community() function and bct package is not required.


    *******
    input: file
        .txt file that contains the network.
        format: u,v,weight
    *******
    output: 
    communities: N*1 np.ndarray
    Maximized Q-metric: the measure of modularity for networks
    """
    
    net = generate_netx(file)
    [ci_best,Q_best]=community_fast_net(net)
    
    words = print_com('unique.txt')
    ci_best = [[words[i][0] for i in ci] for ci in ci_best]
    
    return ci_best, Q_best

def community_fast_net(net):
    """
    *******
    The function uses Girvan-Newman algorithm to get communities from a given 
    networkx net.
    It works faster than community() function and bct package is not required.


    *******
    input: file
        .txt file that contains the network.
        format: u,v,weight
    *******
    output: 
    communities: N*1 np.ndarray
    Maximized Q-metric: the measure of modularity for networks
    """
        
    n_edges = nx.number_of_edges(net)
    n_nodes = nx.number_of_nodes(net)
    n_components = nx.connected_components(net)
    adj_mat = nx.adj_matrix(net)
    #print(type(adj_mat))
    Q = 0
    Q_best = 0
    ci_best = []
    
    weighted_n_edges = 0
    for i in range(n_nodes):
        for j in range(n_nodes):
            weighted_n_edges += adj_mat[i,j]/2.0
    
    weighted_degree = {}
    tmp_mat = adj_mat.sum(axis = 1)
    #print(type(tmp_mat))
    for i in range(n_nodes):
        nodes = net.nodes()
        weighted_degree[nodes[i]] = tmp_mat[i,0]
    
    while n_edges > 1:
        #Calculate the betweenness for each edge. The output is a dictionary.
        edge_betweenness = nx.edge_betweenness_centrality(net,weight='weight')
        #get the edge(s) with max edge betweenness and remove it(them)
        max_values = max(edge_betweenness.values())
        for key,value in edge_betweenness.items():
            if float(value) == max_values:
                net.remove_edge(key[0],key[1])
        #update the number of edges, nodes and components
        n_edges = nx.number_of_edges(net)
        n_nodes = nx.number_of_nodes(net)
        n_components = nx.connected_components(net)
        #temporary degree distribution
        tmp_degree = {}
        adj_mat = nx.adjacency_matrix(net)
        tmp_mat = adj_mat.sum(axis = 1)
        for i in range(n_nodes):
            nodes = net.nodes()
            tmp_degree[nodes[i]] = tmp_mat[i,0]
        #loop through current components to calculate the Q
        for i in n_components:
            n_edge_com = 0
            rand = 0
            for j in i:
                #current total weighted edges within the component
                n_edge_com += tmp_degree[j] #current degree on j node
                #original total weighted edges within the component
                rand += weighted_degree[j] #original degree on j node
            #for the definition of Q, see https://en.wikipedia.org/wiki/Modularity_(networks)
            Q += (float(n_edge_com) - float(rand*rand)/float(2*weighted_n_edges))
        Q = Q/float(2*weighted_n_edges)
        
        if Q>Q_best:
            Q_best = Q
            ci_best = [ci for ci in nx.connected_components(net)]
        else:
            pass

    return ci_best,Q_best

def similar_context(word,file):
    """
    *******
    The function gets words in similar context with the input word.

    *******
    input: 
    word: 
        specified word
    
    file:
        .txt file that contains the network.
        format: u,v,weight
    *******
    output: 
    context:
        a list of words
    """    
    words = print_com('unique.txt')
    words = [i[0] for i in words]
    ind = words.index(word)
    net = generate_netx(file) 
    word_centrality = nx.betweenness_centrality(net)
    print(word_centrality)       
    [ci,Q]=community_fast_net(net)
    for comm in ci:
        if ind in comm:
            context = comm
    else:
        pass
    
    context = list(context)
    print(context)
    non_specific = []
    for i in context:
        #print(i)
        if word_centrality.get(i) > 0.01:
            print(i)
            non_specific.append(i)
        else:
            pass
    
    context = list(set(context)-set(non_specific))
    words = print_com('unique.txt')
    context = [words[i] for i in context]
    
    return context

def ambgt_dectect(file):
    """
    *******
    The function detects ambiguous words in a file. (The threshold used in the 
    script seems very import on the accuracy. Still trying to find a proper value.)

    *******
    input: file
        .txt file that contains the network.
        format: u,v,weight
    *******
    output: 
    candidates:
        a list of words that are potentiolly ambiguous.
    """
    
    net = generate_netx(file)
    word_centrality = nx.betweenness_centrality(net)
    [ci_org,Q_org] = community_fast_net(net)
    candidates = []
    #thresh = 0.5
    for key,value in word_centrality.items():
        if float(value) > 0.5:
        #the threshold 0.5 is set based on experience.
            net_tmp = net
            net_tmp.remove_node(key)
            [ci,Q]=community_fast_net(net_tmp)
            if (Q-Q_org) > 0.01:
                candidates.append(key)
            else:
                pass
    
    return candidates



def generate_netx(file):
    """
    *******
    The function generates a networkx network from file.


    *******
    input: file
        .txt file that contains the network.
        format: u,v,weight
    *******
    output: 
    net:
        networkx net
    """
    
    f = csv.reader(open(file))
    net = nx.Graph()
    for edge in f:
        net.add_edge(int(edge[0]),int(edge[1]),weight=float(edge[2]))
    #n_communities = nx.number_connected_components(net) networkx community finding algorithm, didnt work well.

    return net

def print_com(file):
    f = csv.reader(open(file))
    com = []
    for line in f:
        com.append(line)
        
    return com