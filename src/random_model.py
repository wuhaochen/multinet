"""
A few multiplex configuration models.

"""
import networkx as nx

from Multinet import Multinet
from bipartite import bipartize
from bipartite import bipartite_sets
from bipartite import reconstruct_from_bipartite

def multiplex_configuration_bipartite(mg,seed=None):
    """Bipartite configuration model.
    First convert the multiplex network to a bipartite graph using layer-edge view. Then run a configuraion model on the bipartite graph and reconstruct a multiplex network.
    This configuration model will preserve the aggregated network and the number of layers each edge sits on.

    Parameters
    ----------
    mg : Multinet
      Multiplex network to be configured.

    seed : object
      Seed for the configuration model.

    Return
    ------
    A new Multinet instance.

    """
    bg = bipartize(mg,'e')
    top,bottom = bipartite_sets(bg)

    top = list(top)
    bottom = list(bottom)

    degree_getter = lambda x: bg.degree(x)
    dtop = map(degree_getter,top)
    dbottom = map(degree_getter,bottom)

    rbg = nx.bipartite.configuration_model(dtop,dbottom,create_using=nx.Graph(),seed=seed)
    rtop,rbottom = bipartite_sets(rbg)

    keys = list(rtop)+list(rbottom)
    values = list(top)+list(bottom)
    mapping = dict(zip(keys,values))

    nrbg = nx.relabel_nodes(rbg,mapping)
    nmg = reconstruct_from_bipartite(nrbg)

    return nmg

def _random_int_list(length,a=0,b=1000000,seed=None):
    """Return a list of uniform random intergers.

    Parameters:
    -----------
    length: int
      The list length.

    a, b: int
      The range of the generated integers.

    seed: object
      The seed for the random number generator.
    """
    import random
    random.seed(seed)
    l = []
    for i in range(length):
        l.append(random.randint(a,b))
    return l
    
def multiplex_configuration_independent(mg,seed=None):
    """Run configuration model independently for each layer.

    Parameters
    ----------
    mg : Multinet
      Multiplex network to be configured.

    seed : object
      Seed for the configuration model.

    Return
    ------
    A new Multinet instance.


    """
    layers = mg.layers()
    nl = len(layers)

    seeds = _random_int_list(nl,seed=seed)
    
    nmg = Multinet()
    for layer in layers:
        sg = mg.sub_layer(layer,remove_isolates=True)
        nodes = sg.in_degree().keys()
        in_degs = sg.in_degree().values()
        out_degs = sg.out_degree().values()
        rsg = nx.directed_configuration_model(in_degs,out_degs,create_using=nx.DiGraph(),seed=seeds.pop())
        rnodes = rsg.nodes()
        mapping = dict(zip(rnodes,nodes))
        nrsg = nx.relabel_nodes(rsg,mapping)
        nmg.add_layer(nrsg,layer)

    return nmg

def multiplex_erdos_renyi(mg,seed=None,include_all=True):
    """Return a Multinet such that each layer is an Erdos-Renyi network with same p as the original Multinet given.

    Parameters
    ----------
    mg : Multinet
      Multiplex network to be configured.

    seed : object
      Seed for the model.

    Return
    ------
    A new Multinet instance.


    """
    layers = mg.layers()
    nl = len(layers)

    seeds = _random_int_list(nl,seed=seed)
    
    nmg = Multinet()
    for layer in layers:
        sg = mg.sub_layer(layer,remove_isolates=not include_all)
        nodes = sg.nodes()
        nnode = sg.number_of_nodes()
        nedge = sg.number_of_edges()
        p = float(nedge)/pow(nnode,2)
        rsg = nx.erdos_renyi_graph(nnode,p,seed=seeds.pop(),directed=True)
        rnodes = rsg.nodes()
        mapping = dict(zip(rnodes,nodes))
        nrsg = nx.relabel_nodes(rsg,mapping)
        nmg.add_layer(nrsg,layer)

    return nmg

    
