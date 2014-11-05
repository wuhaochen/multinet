#!/usr/bin/python

import math
import scipy.stats as stats
import matplotlib.pyplot as plt

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

def attach_focus_edges(g):
    carriers = []
    for edge in g.es:
	for key in edge['weight']:
            if not key in carriers:
                carriers.append(key)

    total = {}
    All = 0
    for airline in carriers:
	total[airline] = 0
    for edge in g.es:
	edge['total'] = 0
    for edge in g.es:
	for key in edge['weight']:
            edge['total'] += edge['weight'][key]
            total[key] += edge['weight'][key]
            All += edge['weight'][key]
    
    for edge in g.es:
	r = edge['total']/All
	edge['focus'] = 0.0
	for key in edge['weight']:
            if edge['weight'][key] != 0:
                q = edge['weight'][key]/total[key]
                edge['focus'] += q*math.log(q/r)

    focus = {}
    for carrier in carriers:
        if total[carrier] != 0:
            q = total[carrier]/All
            focus[carrier] = 0.0
            for edge in g.es:
                if edge['weight'].has_key(carrier) and edge['weight'][carrier]!=0:
                    r = edge['weight'][carrier]/edge['total']
                    focus[carrier] += r*math.log(r/q)

    return focus

def attach_focus_nodes(g):
    carriers = []
    for edge in g.es:
	for key in edge['weight']:
            if not key in carriers:
                carriers.append(key)

    total = {}
    All = 0
    for airline in carriers:
	total[airline] = 0
    for node in g.vs:
        node['in_total'] = 0
        node['out_total'] = 0
        node['weight'] = [{},{},{}]
    for edge in g.es:
	for key in edge['weight']:
            if not g.vs[edge.target]['weight'][0].has_key(key):
                g.vs[edge.target]['weight'][0][key] = 0
            if not g.vs[edge.target]['weight'][2].has_key(key):
                g.vs[edge.target]['weight'][2][key] = 0
            g.vs[edge.target]['weight'][0][key] += edge['weight'][key]
            g.vs[edge.target]['weight'][2][key] += edge['weight'][key]
            if not g.vs[edge.source]['weight'][1].has_key(key):
                g.vs[edge.source]['weight'][1][key] = 0
            if not g.vs[edge.source]['weight'][2].has_key(key):
                g.vs[edge.source]['weight'][2][key] = 0
            g.vs[edge.source]['weight'][1][key] += edge['weight'][key]
            g.vs[edge.source]['weight'][2][key] += edge['weight'][key]
            
            g.vs[edge.target]['in_total'] += edge['weight'][key]
            g.vs[edge.source]['out_total'] += edge['weight'][key]
            total[key] += edge['weight'][key]
            All += edge['weight'][key]
    
    for node in g.vs:
        ri = node['in_total']/All
        ro = node['out_total']/All
        r = ri+ro
        node['in_focus'] = 0.0
        node['out_focus'] = 0.0
        node['focus'] = 0.0
        for key in node['weight'][0]:
            if node['weight'][0][key] != 0:
                qi = node['weight'][0][key]/total[key]
                node['in_focus'] += qi*math.log(qi/ri)
        for key in node['weight'][1]:
            if node['weight'][1][key] != 0:
                qo = node['weight'][1][key]/total[key]
                node['out_focus'] += qo*math.log(qo/ro)
        for key in node['weight'][2]:
            if node['weight'][2][key] != 0:
                q = node['weight'][2][key]/total[key]
                node['focus'] += q*math.log(q/r)


    focus = [{},{},{}]
    for carrier in carriers:
        if total[carrier] != 0:
            q = total[carrier]/All
            focus[0][carrier] = 0.0
            focus[1][carrier] = 0.0
            focus[2][carrier] = 0.0
            for node in g.vs:
                if node['weight'][0].has_key(carrier) and node['weight'][0][carrier]!=0:
                    ri = node['weight'][0][carrier]/node['in_total']
                    focus[0][carrier] += ri*math.log(ri/q)
                if node['weight'][1].has_key(carrier) and node['weight'][1][carrier]!=0:
                    ro = node['weight'][1][carrier]/node['out_total']
                    focus[1][carrier] += ro*math.log(ro/q)
                if node['weight'][2].has_key(carrier) and node['weight'][2][carrier]!=0:
                    r = node['weight'][2][carrier]/(node['in_total']+node['out_total'])
                    focus[2][carrier] += r*math.log(r/q)

    return focus
