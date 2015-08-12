#!/usr/bin/python

import filters
import weight
import layer
import multinet

import random
import matplotlib.pyplot as plt
import networkx as nx

from main import default_path
from main import comtrade_path

def g_katrina():
    airfile = default_path + 'T2005.csv'
    filt_r = filters.regular_filter()
    filt8 = filters.build_and_filter(MONTH=8)
    filt_8 = filters.combine_filters_and(filt_r,filt8)
    filt9 = filters.build_and_filter(MONTH=9)
    filt_9 = filters.combine_filters_and(filt_r,filt9)
    weightf = weight.weight_from_string('PASSENGERS')

    g8 = multinet.graph_from_csv(airfile,filt_8,weightf)
    g9 = multinet.graph_from_csv(airfile,filt_9,weightf)

    return [g8,g9]

def g_by_month(year,month):
    airfile = default_path + 'T' + str(year) +'.csv'
    filt_r = filters.regular_filter()
    filt_m = filters.build_and_filter(MONTH=month)
    filt = filters.combine_filters_and(filt_r,filt_m)
    weightf = weight.weight_from_string('PASSENGERS')

    return multinet.graph_from_csv(airfile,filt,weightf)

def mg_by_year(year):
    airfile = default_path + 'T' + str(year) + '.csv'
    filt = filters.regular_filter()
    weightf = weight.weight_from_string('PASSENGERS')
    layerf = layer.layer_from_string('CARRIER')
    return multinet.graph_from_csv(airfile,filt,weightf,True,'CARRIER')

def mg_all_by_year(year):
    airfile = default_path + 'T' + str(year) + '.csv'
    filt = filters.cargo_filter()
    weightf = weight.weight_from_string('DEPARTURES_PERFORMED')
    return multinet.graph_from_csv(airfile,filt,weightf,True,'CARRIER')
    
def mg_by_year_comtrade(year):
    comfile = comtrade_path + 'C' + str(year) + '.csv'
    filt = lambda x,y:True
    weightf = weight.weight_from_string('v')
    layerf = layer.layer_from_string('hs6')
    return multinet.graph_from_csv(comfile,filt,weightf,True,'hs6',ow='i',dw='j')

def subgraph_edges(airfile,l):
    filt_r = filters.regular_filter()
    filt_l = filters.build_in_and_filter(CARRIER=l)
    filt = filters.combine_filters_and(filt_l,filt_r)
    weight = weight.weight_from_string('PASSENGERS')

    g = multinet.graph_from_csv(airfile,filt,weight,True,'CARRIER')
    
    subgraph_edges = []
    for source,target in g.edges():
        edge = g[source][target]
        if len(edge['weight']) == len(l):
            subgraph_edges.append(edge)

    subgraph_nodes = {}
    for edge in subgraph_edges:
        subgraph_nodes[edge.source] = True
        subgraph_nodes[edge.target] = True

    subgraph = nx.DiGraph()
    for node in subgraph_nodes:
        subgraph.add_vertex(g.vs[node]['name'])
    for edge in subgraph_edges:
        source = g.vs[edge.source]['name']
        target = g.vs[edge.target]['name']
        subgraph.add_edge(source,target,weight=edge['weight'])

    return subgraph

def subgraph_nodes(airfile,l):
    filt_r = filters.regular_filter()
    filt_l = filters.build_in_and_filter(CARRIER=l)
    filt = filters.combine_filters_and(filt_l,filt_r)
    weightf = weight.weight_from_string('PASSENGERS')

    g = multinet.graph_from_csv(airfile,filt,weightf,True,'CARRIER')

    for node in g.vs:
        node['strength'] = {}

    for edge in g.es:
        source = g.vs[edge.source]
        target = g.vs[edge.target]
        for carrier in edge['weight']:
            if not source['strength'].has_key(carrier):
                source['strength'][carrier] = 0
            if not target['strength'].has_key(carrier):
                target['strength'][carrier] = 0
            source['strength'][carrier] += edge['weight'][carrier]
            target['strength'][carrier] += edge['weight'][carrier]

    subgraph_nodes = []
    for node in g.vs:
        if len(node['strength']) == len(l):
            subgraph_nodes.append(node.index)

    subgraph_edges = []
    for edge in g.es:
        if edge.source in subgraph_nodes and edge.target in subgraph_nodes:
            subgraph_edges.append(edge)

    subgraph = igraph.Graph(directed = True)
    for node in subgraph_nodes:
        subgraph.add_vertex(g.vs[node]['name'],strength=g.vs[node]['strength'] )
    for edge in subgraph_edges:
        source = g.vs[edge.source]['name']
        target = g.vs[edge.target]['name']
        subgraph.add_edge(source,target,weight=edge['weight'])

    return subgraph

def get_carriers(g):
    carriers = []
    for edge in g.es:
        for key in edge['weight']:
            if not key in carriers:
                carriers.append(key)
    return carriers

# def rewire_layer(g,nround):
#     carriers = get_carriers(g)
#     for carrier in carriers:
#         for i in range(nround):
#             redge = random.sample(g.es,1)[0]
#             if redge['weight'].has_key(carrier):
#                 nodes = random.sample(g.vs,2)
#                 source = nodes[0]
#                 target = nodes[1]
#                 try:
#                     eid = g.get_eid(source.index,target.index)
#                 except:
#                     g.add_edge(source,target)
#                     eid = g.get_eid(source.index,target.index)
#                     g.es[eid]['weight'] = {}
#                 if not g.es[eid]['weight'].has_key(carrier):
#                     g.es[eid]['weight'][carrier] = 0.0
#                 weight = redge['weight'][carrier]
#                 redge['weight'][carrier] = g.es[eid]['weight'][carrier]
#                 g.es[eid]['weight'][carrier] = weight
                
# def rewire_node(g,nround):
#     carriers = get_carriers(g)
#     for edge in g.es:
#         for i in range(nround):
#             candidates = random.sample(carriers,2)
#             if not edge['weight'].has_key(candidates[0]):
#                 edge['weight'][candidates[0]] = 0.0
#             if not edge['weight'].has_key(candidates[1]):
#                 edge['weight'][candidates[1]] = 0.0

#             weight = edge['weight'][candidates[0]]
#             edge['weight'][candidates[0]] = edge['weight'][candidates[1]]
#             edge['weight'][candidates[1]] = weight

