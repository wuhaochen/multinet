import dit
from collections import Counter

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

def intersect(mg1,mg2,method="Merge"):
    pass

def union(mg1,mg2,method="Merge"):
    pass

def transfer_entropy(g1,g2,layers=None):
    if not layers:
        layers = set(g1.layers())&set(g2.layers())
    for layer1,layer2 in itertools.combination(layers,2):
        counts = extract_count(g1,g2,layer1,layer2)