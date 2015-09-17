#!/usr/bin/python

import math
import scipy.stats as stats
import matplotlib.pyplot as plt
import copy
import itertools
import networkx as nx
from networkx.algorithms import bipartite

layer_prefix = 'Layer_'
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
    prefix = lambda x: layer_prefix + str(x)
    layer_names = map(prefix,layers)
    bipartite_graph.add_nodes_from(layer_names,bipartite = 0)
    if isinstance(mode,basestring):
        mstr = mode.lower()
        if mstr in set(['nodes','node','vertices','vertex','n','v']):
            bipartite_graph.add_nodes_from(g,bipartite = 1)
            for layer in layers:
                sg = sub_layer(g,layer)
                for node in sg.nodes():
                    w = sg.degree(node,weight='weight')
                    if w > 0:
                        bipartite_graph.add_edge(prefix(layer),node,weight=w)
        elif mstr in set(['edges','edge','arcs','arc','e','a']):
            bipartite_graph.add_nodes_from(g.edges(),bipartite = 1)
            for source,target in g.edges():
                layers = g[source][target]['weight']
                for layer in layers:
                    bipartite_graph.add_edge(prefix(layer),(source,target),weight=layers[layer])
                    
        else:
            raise "Mode does not exist!"
    else:
        raise "Mode must be string!"
    return bipartite_graph

def bipartite_sets(bg):
    top = set(n for n,d in bg.nodes(data=True) if d['bipartite']==0)
    bottom = set(bg) - top
    return (top,bottom)

def reconstruct_from_bipartite(bg):
    top,bottom = bipartite_sets(bg)
    mg = nx.DiGraph()

    remove_prefix = lambda x: x[len(layer_prefix):]
    layers = map(remove_prefix,list(top))
    mg.graph['layers'] = layers

    for nodes in bottom:
        mg.add_nodes_from(nodes)
        source = nodes[0]
        target = nodes[1]
        mg.add_edge(source,target,weight={})
        for layer in bg[nodes]:
            layer = remove_prefix(layer)
            mg[source][target]['weight'][layer] = 1.0

    return mg

def multiplex_configuration(mg):
    bg = bipartize(mg,'e')
    top,bottom = bipartite_sets(bg)

    top = list(top)
    bottom = list(bottom)

    degree_getter = lambda x: bg.degree(x)
    dtop = map(degree_getter,top)
    dbottom = map(degree_getter,bottom)

    rbg = nx.bipartite_configuration_model(dtop,dbottom,create_using=nx.Graph())
    rtop,rbottom = bipartite_sets(rbg)

    keys = list(rtop)+list(rbottom)
    values = list(top)+list(bottom)
    mapping = dict(zip(keys,values))

    nrbg = nx.relabel_nodes(rbg,mapping)
    nmg = reconstruct_from_bipartite(nrbg)

    return nmg

def all_pairs_shortest_paths(g,nl):
    shortest_paths = {}
    layers = get_layer_list(g)
    nodes = g.nodes()
    for pair in itertools.permutations(nodes,2):
        shortest_paths[pair] = float('inf')

    from aggregate import sub_layers
    for subnet in itertools.combinations(layers,nl):
        sg = sub_layers(g,subnet)
        length = nx.all_pairs_shortest_path_length(sg)
        for src in length:
            for dst in length[src]:
                if src == dst:
                    continue
                if length[src][dst] < shortest_paths[(src,dst)]:
                    shortest_paths[(src,dst)] = length[src][dst]

    return shortest_paths

def two_layer_one_way(mg,layers):
    if len(layers) != 2:
        raise "Can only handle 2 layers situation."
    nodes_list = list(mg)
    upper = layers[0]
    lower = layers[1]
    upper_nodes = ['Upper_'+x for x in nodes_list]
    lower_nodes = ['Lower_'+x for x in nodes_list]

    ng = nx.DiGraph()
    ng.add_nodes_from(upper_nodes)
    ng.add_nodes_from(lower_nodes)
    for node in nodes_list:
        ng.add_edge('Upper_'+node,'Lower_'+node)

    for source,target in mg.edges():
        if mg[source][target]['weight'].has_key(upper):
            ng.add_edge('Upper_'+source,'Upper_'+target)
        if mg[source][target]['weight'].has_key(lower):
            ng.add_edge('Lower_'+source,'Lower_'+target)

    return ng
    
def one_hop_shortest_path(g):
    shortest_paths = {}
    layers = get_layer_list(g)
    nodes = g.nodes()
    for pair in itertools.permutations(nodes,2):
        shortest_paths[pair] = float('inf')

    from aggregate import sub_layers
    for subnet in itertools.combinations(layers,1):
        sg = sub_layers(g,subnet)
        length = nx.all_pairs_shortest_path_length(sg)
        for src in length:
            for dst in length[src]:
                if src == dst:
                    continue
                if length[src][dst] < shortest_paths[(src,dst)]:
                    shortest_paths[(src,dst)] = length[src][dst]
        
    for subnet in itertools.combinations(layers,2):
        upper = subnet[0]
        lower = subnet[1]
        ng = two_layer_one_way(g,[upper,lower])
        length = nx.all_pairs_shortest_path_length(ng)
        for src in length:
            for dst in length[src]:
                #In the same layer.
                if src[0] == dst[0]:
                    continue
                osrc = src[6:]
                odst = dst[6:]
                if osrc == odst:
                    continue
                # -1 for inter layer hop.
                if length[src][dst]-1 < shortest_paths[(osrc,odst)]:
                    shortest_paths[(osrc,odst)] = length[src][dst]-1

        ng = two_layer_one_way(g,[lower,upper])
        length = nx.all_pairs_shortest_path_length(ng)

        for src in length:
            for dst in length[src]:
                #In the same layer.
                if src[0] == dst[0]:
                    continue
                osrc = src[6:]
                odst = dst[6:]
                if osrc == odst:
                    continue
                # -1 for inter layer hop.
                if length[src][dst]-1 < shortest_paths[(osrc,odst)]:
                    shortest_paths[(osrc,odst)] = length[src][dst]-1

    return shortest_paths

def one_hop_shortest_path_combinations(g):
    shortest_paths = {}
    shortest_combinations = {}
    layers = get_layer_list(g)
    nodes = g.nodes()
    for pair in itertools.permutations(nodes,2):
        shortest_paths[pair] = float('inf')

    from aggregate import sub_layers
    for subnet in itertools.combinations(layers,1):
        sg = sub_layers(g,subnet)
        length = nx.all_pairs_shortest_path_length(sg)
        for src in length:
            for dst in length[src]:
                if src == dst:
                    continue
                if length[src][dst] == shortest_paths[(src,dst)]:
                    shortest_combinations[(src,dst)].append(subnet)
                if length[src][dst] < shortest_paths[(src,dst)]:
                    shortest_paths[(src,dst)] = length[src][dst]
                    shortest_combinations[(src,dst)] = [subnet]
        
    for subnet in itertools.combinations(layers,2):
        upper = subnet[0]
        lower = subnet[1]
        ng = two_layer_one_way(g,[upper,lower])
        length = nx.all_pairs_shortest_path_length(ng)
        for src in length:
            for dst in length[src]:
                #In the same layer.
                if src[0] == dst[0]:
                    continue
                osrc = src[6:]
                odst = dst[6:]
                if osrc == odst:
                    continue
                # -1 for inter layer hop.
                if length[src][dst]-1 == shortest_paths[(osrc,odst)]:
                    shortest_combinations[(osrc,odst)].append(subnet)
                if length[src][dst]-1 < shortest_paths[(osrc,odst)]:
                    shortest_paths[(osrc,odst)] = length[src][dst]-1
                    shortest_combinations[(osrc,odst)] = [subnet]

        ng = two_layer_one_way(g,[lower,upper])
        length = nx.all_pairs_shortest_path_length(ng)

        for src in length:
            for dst in length[src]:
                #In the same layer.
                if src[0] == dst[0]:
                    continue
                osrc = src[6:]
                odst = dst[6:]
                if osrc == odst:
                    continue
                # -1 for inter layer hop.
                if length[src][dst]-1 == shortest_paths[(osrc,odst)]:
                    shortest_combinations[(osrc,odst)].append(subnet)
                if length[src][dst]-1 < shortest_paths[(osrc,odst)]:
                    shortest_paths[(osrc,odst)] = length[src][dst]-1
                    shortest_combinations[(osrc,odst)] = [subnet]

    return shortest_combinations

def attach_focus(bg,weighted=True):
    '''
    Given a bipartite network, calculating the focus of the nodes.
    '''
    if weighted:
        A = sum(bg[source][target]['weight'] for source,target in bg.edges())
    else:
        A = bg.number_of_edges()

    for n in bg.nodes():
        if weighted:
            bg.node[n]['concentration'] = bg.degree(n,'weight')/A
        else:
            bg.node[n]['concentration'] = bg.degree(n)/A

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
