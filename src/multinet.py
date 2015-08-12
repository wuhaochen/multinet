#!/usr/bin/python

import networkx as nx
import csv

class MultiplexGraph(nx.DiGraph):
    layers = []

#@param:
#  filter_func should be a function that:
#    1.Accept an index dictionary and a vector of one csv line as its parameter.
#    2.Return True when the record should be included in the graph.
#  weight_func should be a function similiar to filter_func and return the weight.
def graph_from_csv(file_name,filter_func,weight_func,multi_layer=False,layer_s='',ow='ORIGIN',dw='DEST'):
    index_dict = {}
    g = nx.DiGraph()
    g.graph['layers'] = []

    if type(weight_func) == str:
        import weight
        weight_func = weight.weight_from_string(weight_func)

    if type(layer_s) == str:
        import layer
        layer_func = layer.layer_from_string(layer_s)
    else:
        layer_func = layer_s
        
    with open(file_name) as netfile:
        netreader = csv.reader(netfile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_NONNUMERIC)
        index_line = netreader.next()

        index = 0
        for item in index_line:
            index_dict[item] = index
            index += 1

        origin_index = index_dict[ow]
        dest_index = index_dict[dw]

        for line in netreader:
            if not filter_func(index_dict,line):
                continue

            origin = line[origin_index]
            dest = line[dest_index]
            
            g.add_node(origin)
            g.add_node(dest)

            g.add_edge(origin,dest)

            if not g[origin][dest].has_key('weight'):
                if multi_layer:
                    g[origin][dest]['weight'] = dict()
                else:
                    g[origin][dest]['weight'] = 0.0
            
            if multi_layer:
                layer = layer_func(index_dict,line)
                if not layer in g.graph['layers']:
                    g.graph['layers'].append(layer)
                if not g[origin][dest]['weight'].has_key(layer):
                    g[origin][dest]['weight'][layer] = 0.0
                g[origin][dest]['weight'][layer] += weight_func(index_dict,line)
            else:
                g[origin][dest]['weight'] += weight_func(index_dict,line)

    return g

