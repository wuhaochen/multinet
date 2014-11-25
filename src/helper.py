#!/usr/bin/python

from filters import *
import igraph

def g_katrina():
    airfile = default_path + 'T2005.csv'
    filt8 = build_and_filter(MONTH='8',CLASS='F')
    filt9 = build_and_filter(MONTH='9',CLASS='F')
    weight = weight_from_string('PASSENGERS')

    g8 = build_airgraph(airfile,filt8,weight)
    g9 = build_airgraph(airfile,filt9,weight)

    return [g8,g9]

def subgraph_edges(airfile,l):
    filt_c = build_and_filter(CLASS='F')
    filt_l = build_in_and_filter(CARRIER=l)
    filt_r = build_nand_filter(DEPARTURES_SCHEDULED='0.00')
    filt = combine_filters_and(filt_c,filt_l,filt_r)
    weight = weight_from_string('PASSENGERS')

    g = build_airgraph(airfile,filt,weight,True,'CARRIER')
    
    subgraph_edges = []
    for edge in g.es:
        if len(edge['weight']) == len(l):
            subgraph_edges.append(edge)

    subgraph_nodes = {}
    for edge in subgraph_edges:
        subgraph_nodes[edge.source] = True
        subgraph_nodes[edge.target] = True

    subgraph = igraph.Graph(directed = True)
    for node in subgraph_nodes:
        subgraph.add_vertex(g.vs[node]['name'])
    for edge in subgraph_edges:
        source = g.vs[edge.source]['name']
        target = g.vs[edge.target]['name']
        subgraph.add_edge(source,target,weight=edge['weight'])

    return subgraph

def subgraph_nodes(airfile,l):
    filt_c = build_and_filter(CLASS='F')
    filt_l = build_in_and_filter(CARRIER=l)
    filt_r = build_nand_filter(DEPARTURES_SCHEDULED='0.00')
    filt = combine_filters_and(filt_c,filt_l,filt_r)
    weight = weight_from_string('PASSENGERS')

    g = build_airgraph(airfile,filt,weight,True,'CARRIER')

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
