import dit
from collections import Counter
from Multinet import Multinet

def extract_count(g,layers):
    c = Counter()
    for u,v in g.edges():
        word = ''
        for layer in layers:
            if layer in g[u][v]['multiplex']:
                word += '1'
            else:
                word += '0'
        c[word] += 1

    nnode = g.number_of_nodes()
    nedge = g.number_of_edges()
    if g.is_directed():
        non_edge = nnode*(nnode-1)-nedge
    else:
        non_edge = nnode*(nnode-1)/2-nedge
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

def intersect(mgs,prefixs):
    if len(mgs) != len(prefixs):
        raise Exception("Length does not match.'")
    if len(mgs) < 1:
        return None
    g = Multinet()
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

def union(mgs,prefixs):
    if len(mgs) != len(prefixs):
        raise Exception("Length does not match.'")
    if len(mgs) < 1:
        return None
    g = Multinet()
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
    if not layers:
        layers = set(g1.layers())&set(g2.layers())
    for layer1,layer2 in itertools.combination(layers,2):
        counts = extract_count(g1,g2,layer1,layer2)