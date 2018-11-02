"""
A few multiplex configuration models.

"""
from __future__ import division

import random

import networkx as nx
import multinet as mn

from multinet.bipartite import bipartize
from multinet.bipartite import bipartite_sets
from multinet.bipartite import reconstruct_from_bipartite

def multiplex_configuration_bipartite(mg, seed=None):
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
    top, bottom = bipartite_sets(bg)

    top = list(top)
    bottom = list(bottom)

    degree_getter = lambda x: bg.degree(x)
    dtop = map(degree_getter,top)
    dbottom = map(degree_getter,bottom)

    rbg = nx.bipartite.configuration_model(
        dtop, dbottom, create_using=nx.Graph(), seed=seed)
    rtop,rbottom = bipartite_sets(rbg)

    keys = list(rtop)+list(rbottom)
    values = list(top)+list(bottom)
    mapping = dict(zip(keys,values))

    nrbg = nx.relabel_nodes(rbg,mapping)
    
    if mg.is_directed():
        create_using = mn.DiMultinet()
    else:
        create_using = mn.Multinet()
    nmg = reconstruct_from_bipartite(nrbg, create_using=create_using)

    return nmg


def multiplex_configuration_independent(mg, seed=None, include_all=False):
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

    r = random.Random()
    r.seed(seed)

    directed = mg.is_directed()
    if directed:
        nmg = mn.DiMultinet()
    else:
        nmg = mn.Multinet()

    remove_isolates = not include_all
    
    for layer in layers:
        sg = mg.sub_layer(layer, remove_isolates=remove_isolates)
        nodes = sg.nodes()
        if directed:
            in_degs = [sg.in_degree(n) for n in nodes]
            out_degs = [sg.out_degree(n) for n in nodes]
            rsg = nx.directed_configuration_model(
                in_degs, out_degs, create_using=nx.DiGraph(), seed=r)
        else:
            degs = [sg.degree(n) for n in nodes]
            rsg = nx.configuration_model(
                degs, create_using=nx.Graph(), seed=r)
        rnodes = rsg.nodes()
        mapping = dict(zip(rnodes, nodes))
        nrsg = nx.relabel_nodes(rsg, mapping)
        nmg.add_layer(nrsg ,layer)

    return nmg


def multiplex_erdos_renyi(mg, seed=None, include_all=True):
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

    r = random.Random()
    r.seed(seed)

    directed = mg.is_directed()
    if directed:
        nmg = mn.DiMultinet()
    else:
        nmg = mn.Multinet()

    remove_isolates = not include_all

    for layer in layers:
        sg = mg.sub_layer(layer, remove_isolates=remove_isolates)
        nodes = sg.nodes()
        nnode = sg.number_of_nodes()
        nedge = sg.number_of_edges()
        if directed:
            p = nedge / (nnode * (nnode - 1))
        else:
            p = 2 * nedge/ (nnode * (nnode - 1))
        rsg = nx.erdos_renyi_graph(
            nnode, p, seed=r, directed=directed)
        rnodes = rsg.nodes()
        mapping = dict(zip(rnodes, nodes))
        nrsg = nx.relabel_nodes(rsg, mapping)
        nmg.add_layer(nrsg, layer)

    return nmg
