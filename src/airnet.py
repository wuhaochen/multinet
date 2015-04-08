#!/usr/bin/python

import igraph
import csv

def has_vertex(graph,vertex_name):
    try:
        graph.vs.find(vertex_name)
        return True
    except:
        return False
    return False

def has_edge(graph,source_name,target_name):
    source_index = graph.vs.find(source_name)
    target_index = graph.vs.find(target_name)
    try:
        graph.get_eid(source_index,target_index)
        return True
    except:
        return False
    return False

#@param:
#  filter_func should be a function that:
#    1.Accept an index dictionary and a vector of one csv line as its parameter.
#    2.Return True when the record should be included in the graph.
#  weight_func should be a function similiar to filter_func and return the weight.
def build_airgraph(file_name,filter_func,weight_func,multi_layer=False,layer_s=''):
    index_dict = {}
    airnet = igraph.Graph(directed=True)
    airnet['layers'] = []

    with open(file_name) as airfile:
        airreader = csv.reader(airfile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_NONNUMERIC)
        index_line = airreader.next()

        index = 0
        for item in index_line:
            index_dict[item] = index
            index += 1

        origin = index_dict['ORIGIN']
        dest = index_dict['DEST']

        for line in airreader:
            if not filter_func(index_dict,line):
                continue
            try:
                airnet.vs.find(line[origin])
            except:
                airnet.add_vertex(line[origin])
            try:
                airnet.vs.find(line[dest])
            except:
                airnet.add_vertex(line[dest])

            source = airnet.vs.find(line[origin])
            target = airnet.vs.find(line[dest])
            try:
                airnet.get_eid(source.index,target.index)
            except:
                if multi_layer:
                    airnet.add_edge(source,target,weight={})
                else:
                    airnet.add_edge(source,target,weight=0)                    
            
            eid = airnet.get_eid(source.index,target.index)
            if multi_layer:
                l = index_dict[layer_s]
                if not line[l] in airnet['layers']:
                    airnet['layers'].append(line[l])
                if not airnet.es[eid]['weight'].has_key(line[l]):
                    airnet.es[eid]['weight'][line[l]] = 0
                airnet.es[eid]['weight'][line[l]] += weight_func(index_dict,line)
            else:
                airnet.es[eid]['weight'] += weight_func(index_dict,line)

    return airnet

