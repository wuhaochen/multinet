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
        g[source][target]['weight'] = new_weight
    g['layers'] = list(layers) 
    return g

def merge_layers(g,layers):
    new_layer = ''
    for layer in layers:
        g['layers'].remove(layer)
        new_layer += layer
        new_layer += ' '
    new_layer = new_layer.strip()
    g['layers'].append(new_layer)

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
    while len(g['layers']) > k:
        min_dkl = float('inf')
        min_pair = None
        layer_pairs = itertools.combinations(g['layers'],2)
        for lpair in layer_pairs:
            print lpair
            sub_graph = sub_layers(g,lpair)
            dkl = 0.0
            focus = measures.attach_focus_edges(sub_graph,False)
            for layer in focus:
                dkl += math.log(1+(sub_graph['total'][layer])) * focus[layer]
#            dkl = sum(attach_focus_edges(sub_graph,False).values())
#            dkl = sum(attach_focus_nodes(sub_graph,False)[2].values())
            if dkl < min_dkl:
                min_dkl = dkl
                min_pair = lpair
        merge_layers(g,min_pair)
        merge_list.append([min_pair,min_dkl])
    return merge_list

def cluster(g,loc_file_name):
    with open(loc_file_name) as loc_file:
        loc_reader = csv.reader(loc_file)
