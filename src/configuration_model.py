import networkx as nx

from Multinet import Multinet
from bipartite import bipartize
from bipartite import bipartite_sets
from bipartite import reconstruct_from_bipartite

def multiplex_configuration_bipartite(mg,seed=None):
    bg = bipartize(mg,'e')
    top,bottom = bipartite_sets(bg)

    top = list(top)
    bottom = list(bottom)

    degree_getter = lambda x: bg.degree(x)
    dtop = map(degree_getter,top)
    dbottom = map(degree_getter,bottom)

    rbg = nx.bipartite_configuration_model(dtop,dbottom,create_using=nx.Graph(),seed=seed)
    rtop,rbottom = bipartite_sets(rbg)

    keys = list(rtop)+list(rbottom)
    values = list(top)+list(bottom)
    mapping = dict(zip(keys,values))

    nrbg = nx.relabel_nodes(rbg,mapping)
    nmg = reconstruct_from_bipartite(nrbg)

    return nmg

def _random_int_list(length,a=0,b=1000000,seed=None):
    import random
    random.seed(seed)
    l = []
    for i in range(length):
        l.append(random.randint(a,b))
    return l
    
def multiplex_configuration_independent(mg,seed=None):
    layers = get_layer_list(mg)
    nl = len(layers)

    seeds = _random_int_list(nl,seed=seed)
    
    nmg = nx.DiGraph()
    for layer in layers:
        sg = sub_layer(mg,layer,keep_isolated=False)
        nodes = sg.in_degree().keys()
        in_degs = sg.in_degree().values()
        out_degs = sg.out_degree().values()
        rsg = nx.directed_configuration_model(in_degs,out_degs,create_using=nx.DiGraph(),seed=seeds.pop())
        rnodes = rsg.nodes()
        mapping = dict(zip(rnodes,nodes))
        nrsg = nx.relabel_nodes(rsg,mapping)
        add_layer(nmg,nrsg,layer)

    return nmg