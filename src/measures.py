#!/usr/bin/python

import math
import scipy.stats as stats
import matplotlib.pyplot as plt
import copy
import networkx as nx
from networkx.algorithms import bipartite

# Add nodes that in gref to g.
# This function will modify g but not gref.
def fill_nodes(gref,g):
    for node in gref.vs:
        try:
            g.vs.find(node['name'])
        except:
            g.add_vertex(node['name'])

# Add edge that in gref to g.
# This function will modify g but not gref.
def fill_edges(gref,g,w=0):
    fill_nodes(gref,g)
    for edge in gref.es:
        source = g.vs.find(gref.vs[edge.source]['name'])
        target = g.vs.find(gref.vs[edge.target]['name'])
        try:
            eid = g.get_eid(source.index,target.index)
        except:
            g.add_edge(source,target,weight=w)

def corresponding_edge_list(g1,g2):
    weight_list_1 = []
    weight_list_2 = []
    edge_list = []

    for edge in g1.es:
        try:
            source_name = g1.vs[edge.source]['name']
            source = g2.vs.find(source_name)
            target_name = g1.vs[edge.target]['name']
            target = g2.vs.find(target_name)
            eid = g2.get_eid(source.index,target.index)
        except:
            continue
        weight_list_1.append(edge['weight'])
        weight_list_2.append(g2.es[eid]['weight'])
        edge_list.append([source_name,target_name])

    return [weight_list_1,weight_list_2,edge_list]

def corresponding_node_list(g1,g2):
    strength_list_1 = []
    strength_list_2 = []
    node_list = []

    for node in g1.vs:
        try:
            cnode = g2.vs.find(name=node['name'])
        except:
            continue
        strength_list_1.append(node.strength(weights='weight'))
        strength_list_2.append(cnode.strength(weights='weight'))
        node_list.append(node['name'])

    return [strength_list_1,strength_list_2,node_list]

def linear_fit(x,y):
    xbar = float(sum(x))/len(x)
    ybar = float(sum(y))/len(y)

    beta = sum(map(lambda x,y:(x-xbar)*(y-ybar),x,y))/sum(map(lambda x:pow((x-xbar),2),x))
    alpha = ybar-beta*xbar
    return [alpha,beta]

def residuals(x,y):
    [alpha,beta] = linear_fit(x,y)
    yhat = map(lambda x:alpha+beta*x,x)
    return map(lambda x,y:x-y,y,yhat)

def accumulate_SSE(error,edge_list):
    if (len(error) != len(edge_list)):
        raise 'Length of arguments do not match.'

    SSE = {}
    for i in range(len(error)):
        edge = edge_list[i]
        if not SSE.has_key(edge[0]):
            SSE[edge[0]] = 0.0
        if not SSE.has_key(edge[1]):
            SSE[edge[1]] = 0.0
        square_error = pow(error[i],2)
        SSE[edge[0]] += square_error
        SSE[edge[1]] += square_error

    return SSE

def SSE_either(og1,og2):
    g1 = og1.copy()
    g2 = og2.copy()

    fill_edges(g1,g2)
    fill_edges(g2,g1)

    cl = corresponding_edge_list(g1,g2)
    error = residuals(cl[0],cl[1])
    SSE = accumulate_SSE(error,cl[2])

    return SSE

def normalized_SSE_either(og1,og2):
    g1 = og1.copy()
    g2 = og2.copy()

    fill_edges(g1,g2)
    fill_edges(g2,g1)

    cl = corresponding_edge_list(g1,g2)
    error = residuals(cl[0],cl[1])
    SSE = accumulate_SSE(error,cl[2])
    SS = accumulate_SSE(cl[0],cl[2])
    normalized_error = {}
    for key in SSE:
        if SS[key]!=0:
            normalized_error[key] = SSE[key]/SS[key]
    return normalized_error

def correlation_pairs(og1,og2):
    g1 = og1.copy()
    g2 = og2.copy()

    fill_edges(g1,g2)
    fill_edges(g2,g1)

    cl = corresponding_edge_list(g1,g2)
    nempty = pow(len(g1.vs),2)-len(cl[0])

    return stats.pearsonr(cl[0]+[0]*nempty,cl[1]+[0]*nempty)[0]

def correlation_common(og1,og2):
    g1 = og1.copy()
    g2 = og2.copy()

    fill_nodes(g1,g2)
    fill_nodes(g2,g1)

    cl = corresponding_edge_list(g1,g2)
    return stats.pearsonr(cl[0],cl[1])[0]

def correlation_either(og1,og2):
    g1 = og1.copy()
    g2 = og2.copy()

    fill_edges(g1,g2)
    fill_edges(g2,g1)

    cl = corresponding_edge_list(g1,g2)
    return stats.pearsonr(cl[0],cl[1])[0]

def gini(g):
    diff_sum = 0.0
    norm = 4.0 * len(g.es) * len(g.vs)
    for nodei in g.vs:
        for nodej in g.vs:
            diff_sum += abs(nodei.degree() - nodej.degree())
    
    return diff_sum/norm

def sub_layer(og,layer):
    g = nx.DiGraph()
    g.add_nodes_from(og)
    for source,target in og.edges():
        edge = og[source][target]
        if layer in edge['weight']:
            w = edge['weight'][layer]
            g.add_edge(source,target,weight=w)
    return g

def get_layer_list(g):
    return g.graph['layers']
    
def bipartize(g,mode):
    bipartite_graph = nx.Graph()
    layers = get_layer_list(g)
    bipartite_graph.add_nodes_from(layers,bipartite = 0)
    if isinstance(mode,basestring):
        mstr = mode.lower()
        if mstr in set(['nodes','node','vertices','vertex','n','v']):
            bipartite_graph.add_nodes_from(g,bipartite = 1)
            for layer in layers:
                sg = sub_layer(g,layer)
                for node in sg.nodes():
                    w = sg.degree(node,weight='weight')
                    if w > 0:
                        bipartite_graph.add_edge(layer,node,weight=w)
        elif mstr in set(['edges','edge','arcs','arc','e','a']):
            bipartite_graph.add_nodes_from(g.edges(),bipartite = 1)
            for source,target in g.edges():
                layers = g[source][target]['weight']
                for layer in layers:
                    bipartite_graph.add_edge(layer,(source,target),weight=layers[layer])
                    
        else:
            raise "Mode does not exist!"
    else:
        raise "Mode does not exist!"
    return bipartite_graph

def bipartite_sets(bg):
    top = set(n for n,d in bg.nodes(data=True) if d['bipartite']==0)
    bottom = set(bg) - top
    return (top,bottom)

# def bipartize(g,mode):
#     bipartite_graph = nx.Graph()
#     layers = get_layer_list(g)
#     bipartite_graph.add_nodes_from(layers,bipartite = 0)
#     if isinstance(mode,basestring):
#         mstr = mode.lower()
#         if mstr in set(['nodes','node','vertices','vertex','n','v']):
#             bipartite_graph.add_nodes_from(g,bipartite = 1)
#             for layer in layers:
#                 sg = sub_layer(g,layer)
#                 for node in sg.nodes():
#                     w = sg.degree(node,weight='weight')
#                     if w > 0:
#                         bipartite_graph.add_edge(layer,node,weight=w)
#         elif mstr in set(['edges','edge','arcs','arc','e','a']):
#             bipartite_graph.add_nodes_from(g.edges(),bipartite = 1)
#             for layer in layers:
#                 sg = sub_layer(g,layer)
#                 for source,target in sg.edges():
#                     edge = sg[source][target]
#                     bipartite_graph.add_edge(layer,(source,target),weight=edge['weight'])
#         else:
#             raise "Mode does not exist!"
#     else:
#         raise "Mode does not exist!"
#     return bipartite_graph
    
def attach_focus(bg):
    '''
    Given a bipartite network, calculating the focus of the nodes.
    '''
    A = sum(bg[source][target]['weight'] for source,target in bg.edges())

    for n in bg.nodes():
        bg.node[n]['concentration'] = bg.degree(n,'weight')/A

    from scipy.stats import entropy
    from math import log

    for n in bg.nodes():
        pk = []
        qk = []
        for neighbor in bg.neighbors(n):
            pk += [bg[n][neighbor]['weight']]
            qk += [bg.node[neighbor]['concentration']]
            
        # The following two lines get rid of unwanted normalization of qk by entropy function
        pk += [0]
        qk += [1- sum(qk)]
        bg.node[n]['dkl'] = entropy(pk,qk)
        if A == sum(pk) or sum(pk) == 0:
            bg.node[n]['focus'] = 0.0
        else:
            bg.node[n]['focus'] = bg.node[n]['dkl']/log(A/sum(pk))
    
def bipartite(g):
    carriers = []
    for source,target in g.edges():
        edge = g[source][target]
        for key in edge['weight']:
            if not key in carriers:
                carriers.append(key)

    for node in g.node():
        g.node[node]['strength'] = {}
        for carrier in carriers:
            g.node[node]['strength'][carrier] = 0.0

    for source,target in g.edges():
        edge = g[source][target]
        for key in edge['weight']:
            g.node[target]['strength'][key] += edge['weight'][key]
            g.node[source]['strength'][key] += edge['weight'][key]

    with open('bi.txt','w') as f:
        f.write('Node')
        for carrier in carriers:
            f.write(','+carrier)
        f.write('\n')
        for node in g.nodes():
            f.write(node)
            for carrier in carriers:
                f.write(','+str(g.node[node]['strength'][carrier]))
            f.write('\n')

def count_by_layer(g):
    count = {}
    for source,target in g.edges():
        edge = g[source][target]
        for carrier in edge['weight']:
            if not count.has_key(carrier):
                count[carrier] = 0.0
            count[carrier] += edge['weight'][carrier]
    return count

def reduce_to_degree(g):
    for source,target in g.edges():
        edge = g[source][target]
        for carrier in edge['weight']:
            if edge['weight'][carrier] != 0.0:
                edge['weight'][carrier] = 1.0

def count_all(g):
    count = 0
    for source,target in g.edges():
        edge = g[source][target]
        count += edge['weight']
    return count
