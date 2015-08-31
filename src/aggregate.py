#!/usr/bin/python

import itertools
import copy
import math

from geopy.distance import vincenty
geo_dist = lambda x,y:vincenty(x,y).meters

import scipy.cluster.hierarchy as hier

import multinet
import measures

# Return a new igraph object with only specified layers.
def sub_layers(og,layers):
    g = copy.deepcopy(og)
    for source,target in g.edges():
        new_weight = {}
        for key in layers:
            if key in g[source][target]['weight']:
                new_weight[key] = g[source][target]['weight'][key]
        if len(new_weight) == 0:
            g.remove_edge(source,target)
        else:
            g[source][target]['weight'] = new_weight
    g.graph['layers'] = list(layers) 
    return g

def merge_layers(g,layers):
    new_layer = ''
    for layer in layers:
        g.graph['layers'].remove(layer)
        new_layer += layer
        new_layer += ' '
    new_layer = new_layer.strip()
    g.graph['layers'].append(new_layer)

    for source,target in g.edges():
        new_weight = 0.0
        for layer in layers:
            if layer in g[source][target]['weight']:
                new_weight += g[source][target]['weight'].pop(layer)
        if new_weight != 0:
            g[source][target]['weight'][new_layer] = new_weight

    return 0

def aggregate(g,k):
    merge_list = []
    while len(g.graph['layers']) > k:
        min_djs = float('inf')
        min_pair = None
        layer_pairs = itertools.combinations(g.graph['layers'],2)
        for lpair in layer_pairs:
            print lpair
            sub_graph = sub_layers(g,lpair)
            bi_mode = 'e'
            bi_graph = measures.bipartize(sub_graph,bi_mode)
            measures.attach_focus(bi_graph)
            top,bottom = measures.bipartite_sets(bi_graph)
            djs = 0.0
            for layer in top:
                djs += 0.5*bi_graph.node[layer]['dkl']
            if djs < min_djs:
                min_djs = djs
                min_pair = lpair
        merge_layers(g,min_pair)
        merge_list.append([min_pair,min_djs])
    return merge_list

def cluster(g,loc_file_name):
    with open(loc_file_name) as loc_file:
        loc_reader = csv.reader(loc_file)
