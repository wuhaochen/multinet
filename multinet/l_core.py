"""Calculate the l-core of a multiplex network.
"""

import networkx as nx

def l_core(mg, l):
    """Return the l-core of mg.

    """
    import copy
    core = copy.deepcopy(mg)

    for u,v in mg.edges():
        if len(mg[u][v][mg.cid]) < l:
            core.remove_edge(u,v)

    core.remove_nodes_from(nx.isolates(core))
    core.remove_empty_layers()

    return core
