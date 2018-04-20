"""Project a multiplex network to a bipartite graph.
"""
from __future__ import division

import networkx as nx

from multinet.Multinet import Multinet

#These following lines provide utilities to add and remove prefix to the layer node. In case of a node might have same name as a layer.
_layer_prefix = 'Layer_'

_prefix = lambda x: _layer_prefix + str(x)
_remove_prefix = lambda x: x[len(_layer_prefix):]

def _add_layer_nodes(bg,layers):
    """Add nodes represents the layers in multiplex network to the bipartite graph

    Parameters:
    -----------
    bg: nx.Graph
      Bipartite graph to operate on.

    layers: list
      A list of layers.

    """
    layer_names = map(_prefix,layers)
    bg.add_nodes_from(layer_names, bipartite=0)
    
def bipartize_by_node(mg, weighted=True):
    """Project a Multinet to a bipartite graph using layer-node view.

    Parameters:
    -----------
    mg: Multinet
      Mulitplex network to project.

    weighted: bool
      Whether or not use the weight information in the multiplex network.

    """
    bipartite_graph = nx.Graph()
    _add_layer_nodes(bipartite_graph,mg.layers())
    
    bipartite_graph.add_nodes_from(mg,bipartite = 1)
    for layer in mg.layers():
        sg = mg.sub_layer(layer,remove_isolates=True)
        for node in sg.nodes():
            if weighted:
                w = sg.degree(node,weight='weight')
            else:
                w = sg.degree(node)
            if w > 0:
                bipartite_graph.add_edge(_prefix(layer),node,weight=w)

    return bipartite_graph
    
def bipartize_by_edge(mg, weighted=True):
    """Project a Multinet to a bipartite graph using layer-edge view.

    Parameters:
    -----------
    mg: Multinet
      Mulitplex network to project.

    weighted: bool
      Whether or not use the weight information in the multiplex network.

    """
    bipartite_graph = nx.Graph()
    _add_layer_nodes(bipartite_graph,mg.layers())
    
    bipartite_graph.add_nodes_from(mg.edges(),bipartite = 1)
    for u,v in mg.edges():
        layers = mg[u][v]['multiplex']
        for layer in layers:
            if weighted:
                w = layers[layer]
            else:
                w = 1.0
            bipartite_graph.add_edge(_prefix(layer),(u,v),weight=w)

    return bipartite_graph

def bipartize(mg,mode,weighted=True):
    """Project a Multinet to a bipartite graph using layer-edge view.

    Parameters:
    -----------
    mg: Multinet
      Mulitplex network to project.

    mode: str
      Whether using layer-node view or layer-edge view.

    weighted: bool
      Whether or not use the weight information in the multiplex network.

    """
    if isinstance(mode,basestring):
        mstr = mode.lower()
        if mstr in set(['nodes','node','vertices','vertex','n','v']):
            return bipartize_by_node(mg,weighted)
        elif mstr in set(['edges','edge','arcs','arc','e','a']):
            return bipartize_by_edge(mg,weighted)
        else:
            raise Exception("Mode does not exist!")
    else:
        raise Exception("Mode must be string!")
        
def bipartite_sets(bg):
    """Return two nodes sets of a bipartite graph.

    Parameters:
    -----------
    bg: nx.Graph
      Bipartite graph to operate on.

    """
    top = set(n for n,d in bg.nodes(data=True) if d['bipartite']==0)
    bottom = set(bg) - top
    return (top,bottom)

def reconstruct_from_bipartite(bg):
    """Reconstruct a multiplex network from a layer-edge bipartite graph.

    Parameters:
    -----------
    bg: nx.Graph
      A layer-edge bipartite graph that used to reconstruct the multiplex network.

    """
    top,bottom = bipartite_sets(bg)
    mg = Multinet()

    layers = map(_remove_prefix,list(top))

    for nodes in bottom:
        mg.add_nodes_from(nodes)
        u = nodes[0]
        v = nodes[1]
        for layer in bg[nodes]:
            layer = _remove_prefix(layer)
            mg.add_edge(u,v,layer)

    return mg

def attach_importance(bg):
    """New measure working in progress.
    """
    for node in bg.nodes():
        bg.node[node]['imp'] = 0.0
    
    import itertools
    for u,v in itertools.combinations(bg.nodes(),2):
        common = set(bg[u]) & set(bg[v])
        for node in common:
            bg.node[node]['imp'] += 1/len(common)

    for node in bg.nodes():
        bg.node[node]['nimp'] = bg.node[node]['imp']/bg.degree(node)
