import dit
import itertools
import multinet as mn

from collections import Counter


def extract_count(g, layers, ignore_self_loop=True):
    c = Counter()
    for u,v in g.edges():
        if ignore_self_loop and u == v:
            continue
        word = ''
        for layer in layers:
            if layer in g[u][v]['multiplex']:
                word += '1'
            else:
                word += '0'
        c[word] += 1

    nnode = g.number_of_nodes()
    nedge = g.number_of_edges()

    if ignore_self_loop:
        total_position = nnode*(nnode-1)
    else:
        total_position = nnode*nnode

    if g.is_directed():
        non_edge = total_position-nedge
    else:
        non_edge = total_position/2-nedge

    word = '0'*len(layers)
    c[word] += non_edge
    return c
        
def mutual_information(g,layers):
    counts = extract_count(g,layers)
    total = float(sum(counts.values()))
    probs = map(lambda x:x/total,counts.values())
    dist = dit.Distribution(counts.keys(),probs)

    if len(layers) == 2:
        return dit.shannon.mutual_information(dist,[0],[1])
    else:
        raise Exception("Not implemented.")

def intersect(mgs, prefixs):
    if len(mgs) != len(prefixs):
        raise Exception("Length does not match.'")
    if len(mgs) < 1:
        return None

    directed = mgs[0].is_directed()
    if directed:
        g = mn.DiMultinet()
    else:
        g = mn.Multinet()
    nodes = set(mgs[0].nodes())
    for mg in mgs:
        nodes &= set(mg.nodes())
    g.add_nodes_from(nodes)
    
    for i,mg in enumerate(mgs):
        for u,v in mg.edges():
            if u in nodes and v in nodes:
                for layer in mg[u][v]['multiplex']:
                    g.add_edge(u,v,prefixs[i]+layer,mg[u][v]['multiplex'][layer])
    return g


def jaccard_distance(g,layer1,layer2):
    counts = extract_count(g,(layer1,layer2))
    union = counts['01'] + counts['10'] + counts['11']
    if union == 0:
        return 0.0
    return float(counts['11'])/union


def hamming_distance(g,layer1,layer2):
    counts = extract_count(g,(layer1,layer2))
    return counts['01'] + counts['10']


def union(mgs,prefixs):
    if len(mgs) != len(prefixs):
        raise Exception("Length does not match.'")
    if len(mgs) < 1:
        return None

    directed = mgs[0].is_directed()
    if directed:
        g = mn.DiMultinet()
    else:
        g = mn.Multinet()

    nodes = set()
    for mg in mgs:
        nodes |= set(mg.nodes())
    g.add_nodes_from(nodes)
    
    for i,mg in enumerate(mgs):
        for u,v in mg.edges():
            for layer in mg[u][v]['multiplex']:
                g.add_edge(u,v,prefixs[i]+layer,mg[u][v]['multiplex'][layer])
    return g


def transfer_entropy(g1,g2,layers=None):
    te = {}
    if not layers:
        layers = set(g1.layers())&set(g2.layers())
    for layer1,layer2 in itertools.combinations(layers,2):
        if g1.is_directed() != g2.is_directed():
            raise Exception('Must both be directed or undirected!')
        if g1.is_directed():
            tg = mn.DiMultinet()
        else:
            tg = mn.Multinet()
        tg.add_layer(g1.sub_layer(layer1),'t1_'+layer1)
        tg.add_layer(g1.sub_layer(layer2),'t1_'+layer2)
        tg.add_layer(g2.sub_layer(layer1),'t2_'+layer1)
        tg.add_layer(g2.sub_layer(layer2),'t2_'+layer2)
        tlayers = ['t1_'+layer1,'t1_'+layer2,'t2_'+layer1,'t2_'+layer2]
        counts = extract_count(tg,tlayers)
        total = float(sum(counts.values()))
        probs = map(lambda x:x/total,counts.values())
        dist = dit.Distribution(counts.keys(),probs)
        cmia = dit.shannon.conditional_entropy(dist,[2],[0]) - dit.shannon.conditional_entropy(dist,[2],[0,1])
        cmib = dit.shannon.conditional_entropy(dist,[3],[1]) - dit.shannon.conditional_entropy(dist,[3],[0,1])
        te[(layer2,layer1)] = cmia
        te[(layer1,layer2)] = cmib

    return te
