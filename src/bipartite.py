import networkx as nx

from Multinet import Multinet

_layer_prefix = 'Layer_'

_prefix = lambda x: layer_prefix + str(x)

def _add_layer_nodes(bg,layers):
    layer_names = map(_prefix,layers)
    bg.add_nodes_from(layer_names, bipartite=0)
    
def bipartize_by_node(mg, weighted=True):
    bipartite_graph = nx.Graph()
    _add_layer_nodes(bg,mg.layers())
    
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
    bipartite_graph = nx.Graph()
    _add_layer_nodes(bg,mg.layers())
    
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
    bipartite_graph = nx.Graph()
    bipartite_graph.add_nodes_from(layer_names,bipartite = 0)
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
    top = set(n for n,d in bg.nodes(data=True) if d['bipartite']==0)
    bottom = set(bg) - top
    return (top,bottom)

def reconstruct_from_bipartite(bg):
    top,bottom = bipartite_sets(bg)
    mg = Multinet()

    remove_prefix = lambda x: x[len(_layer_prefix):]
    layers = map(remove_prefix,list(top))

    for nodes in bottom:
        mg.add_nodes_from(nodes)
        u = nodes[0]
        v = nodes[1]
        for layer in bg[nodes]:
            layer = remove_prefix(layer)
            mg.add_edge(u,v,layer)

    return mg
