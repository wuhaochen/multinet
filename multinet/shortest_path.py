"""Functions related to shortest paths.

"""
from __future__ import division

import itertools
import networkx as nx

def all_pairs_k_layer_shortest_path_length(mg, k):
    """Calculate all the k-layer shortest path lengths.

    Parameters:
    -----------
    mg: Multinet
        Multiplex network to calculate.

    k: int
        Number of layers allowed to use when k is positive.
        Number of layers not allowed to use when k is negative.
      

    Returns:
    --------
        A dictionary whose key is a source-destination pair
    and its value is the corresponding k-layer shortest path length.

    """
    shortest_path_lengths = {}
    layers = mg.layers()
    nodes = mg.nodes()

    for pair in itertools.permutations(nodes, 2):
        shortest_path_lengths[pair] = float('inf')

    # syntax sugar to allow convenient operation.
    if k <= 0:
        k = mg.number_of_layers() + k

    for subnet in itertools.combinations(layers, k):
        sg = mg.sub_layers(subnet)
        length = nx.all_pairs_shortest_path_length(sg)
        for src, shortests in length:
            for dst in shortests:
                if src == dst:
                    continue
                if shortests[dst] < shortest_path_lengths[(src, dst)]:
                    shortest_path_lengths[(src, dst)] = shortests[dst]

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
    lengths = all_pairs_k_layer_shortest_path_length(mg, k)
    from collections import Counter
    lc = Counter(lengths.values())
    unreachable = lc[float('inf')]
    total = sum(lc.values())

    return 1-(unreachable/total)


def k_layer_diameter(mg,k):
    """k-layer diameter

    Parameters:
    -----------
    mg: Multinet
        Multiplex network to calculate.

    k: int
        Number of layers allowed to use.

    """
    lengths = all_pairs_k_layer_shortest_path_length(mg,k)
    from collections import Counter
    lc = Counter(lengths.values())
    reachable = filter(lambda x:x<float('inf'),lc.keys())
    if len(reachable) > 0:
        return max(reachable)
    else:
        return 0


def harmonic_mean_shortest_path_length(mg, source=None, target=None):
    """Harmonic mean shortest path length in multiplex network.
        The inverse of harmonic mean of shortest path length in each layer
    between two nodes.
        $$L(u, v) = 1 / \sum_l (1 / L_l(u, v))$$
        $L_l(u, v)$ is the shortest path length between node $u$ and $v$ in
    layer $l$.

    Parameters:
    -----------
    mg: Multinet
        Multiplex network of interest.

    source: node or list
        Node of a list of nodes as source.

    target: node or list
        Node of a list of nodes as target.

    Returns:
    --------
        A dict keyed by (source, target) pair.
    """
    #TODO: implement for specified source and target.
    if not (source and target):
        from collections import Counter
        sum_harmonic = Counter()
        for layer in mg.layers():
            sg = mg.sub_layer(layer)
            shortest_paths_length = nx.all_pairs_shortest_path_length(sg)
            for u, spl in shortest_paths_length:
                for v in spl:
                    if u != v:
                        sum_harmonic[(u,v)] += 1./spl[v]
        ret = {}
        for pair in sum_harmonic:
            ret[pair] = 1./sum_harmonic[pair]
        return ret