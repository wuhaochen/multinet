import multinet as mn
import networkx as nx

g1 = nx.Graph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')]
g1.add_nodes_from(nodes)
g1.add_edges_from(edges)

g2 = nx.Graph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'A'), ('E', 'B')]
g2.add_nodes_from(nodes)
g2.add_edges_from(edges)

g3 = nx.Graph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('A', 'E'), ('B', 'D'), ('C', 'E')]
g3.add_nodes_from(nodes)
g3.add_edges_from(edges)

mg = mn.Multinet()

mg.add_layer(g1, '1')
mg.add_layer(g2, '2')
mg.add_layer(g3, '3')


class TestBipartite(object):


    def test_bipartize(self):
        bg = mn.bipartize(mg, 'n')
        assert (bg.number_of_nodes() ==
                mg.number_of_layers() +
                mg.number_of_nodes())
        bg = mn.bipartize(mg, 'e')
        assert (bg.number_of_nodes() ==
                mg.number_of_layers() +
                mg.number_of_edges())
