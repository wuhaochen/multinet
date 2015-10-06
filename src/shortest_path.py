"""Functions related to shortest paths.

"""
import itertools
from __future__ import division

def all_pairs_k_layer_shortest_path_length(mg,k):
    """Calculate all the k-layer shortest path lengths.

    Parameters:
    -----------
    mg: Multinet
      Multiplex network to calculate.

    k: int
      Number of layers allowed to use.

    Returns:
    --------
    A dictionary whose key is a source-destination pair and its value is the corresponding k-layer shortest path.

    """
    shortest_path_lengths = {}
    layers = mg.layers()
    nodes = mg.nodes()
    
    for pair in itertools.permutations(nodes,2):
        shortest_path_lengths[pair] = float('inf')
    for subnet in itertools.combinations(layers,k):
        sg = sub_layers(g,subnet)
        length = nx.all_pairs_shortest_path_length(sg)
        for src in length:
            for dst in length[src]:
                if src == dst:
                    continue
                if length[src][dst] < shortest_path_lengths[(src,dst)]:
                    shortest_path_lengths[(src,dst)] = length[src][dst]
                    
    return shortest_path_lengths

def k_layer_reachability(mg,k):
    """k-layer reachability

    Parameters:
    -----------
    mg: Multinet
      Multiplex network to calculate.

    k: int
      Number of layers allowed to use.

    """
    lengths = all_pairs_shortest_path_length(mg,k)
    from collections import Counter
    lc = Counter(lengths.values())
    unreachable = lc[float('inf')]
    total = sum(lc.values())

    return 1-(unreachable/total)