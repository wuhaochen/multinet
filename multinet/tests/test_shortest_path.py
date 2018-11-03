from __future__ import division

import multinet as mn
import networkx as nx

g1 = nx.Graph()
dg1 = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('C', 'D')]
g1.add_nodes_from(nodes)
g1.add_edges_from(edges)
dg1.add_nodes_from(nodes)
dg1.add_edges_from(edges)

g2 = nx.Graph()
dg2 = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'C'), ('B', 'D')]
g2.add_nodes_from(nodes)
g2.add_edges_from(edges)
dg2.add_nodes_from(nodes)
dg2.add_edges_from(edges)

g3 = nx.Graph()
dg3 = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('E', 'A'), ('D', 'E')]
g3.add_nodes_from(nodes)
g3.add_edges_from(edges)
dg3.add_nodes_from(nodes)
dg3.add_edges_from(edges)

mg = mn.Multinet()
mg.add_layer(g1, '1')
mg.add_layer(g2, '2')
mg.add_layer(g3, '3')

dmg = mn.DiMultinet()
dmg.add_layer(dg1, '1')
dmg.add_layer(dg2, '2')
dmg.add_layer(dg3, '3')


class TestShortestPath(object):


    def test_all_pairs_k_layer_shortest_path_length_ud(self):
        all_layer_spl = mn.all_pairs_k_layer_shortest_path_length(mg, 3)
        assert len(all_layer_spl) == 20
        assert all_layer_spl[('A', 'B')] == 1
        assert all_layer_spl[('A', 'D')] == 2
        assert all_layer_spl[('A', 'E')] == 1
        assert all_layer_spl[('B', 'C')] == 2

        one_layer_spl = mn.all_pairs_k_layer_shortest_path_length(mg, 1)
        assert len(all_layer_spl) == 20
        assert one_layer_spl[('A', 'B')] == 1
        assert one_layer_spl[('A', 'D')] == 2
        assert one_layer_spl[('A', 'E')] == 1
        assert one_layer_spl[('B', 'C')] == float('inf')

        two_layer_spl = mn.all_pairs_k_layer_shortest_path_length(mg, -1)
        assert len(two_layer_spl) == 20
        assert two_layer_spl[('A', 'B')] == 1
        assert two_layer_spl[('A', 'D')] == 2
        assert two_layer_spl[('A', 'E')] == 1
        assert two_layer_spl[('B', 'C')] == 2


    def test_all_pairs_k_layer_shortest_path_length_d(self):
        all_layer_spl = mn.all_pairs_k_layer_shortest_path_length(dmg, 3)
        assert len(all_layer_spl) == 20
        assert all_layer_spl[('A', 'B')] == 1
        assert all_layer_spl[('A', 'D')] == 2
        assert all_layer_spl[('A', 'E')] == 3

        one_layer_spl = mn.all_pairs_k_layer_shortest_path_length(dmg, 1)
        assert len(all_layer_spl) == 20
        assert one_layer_spl[('A', 'B')] == 1
        assert one_layer_spl[('A', 'D')] == float('inf')
        assert one_layer_spl[('A', 'E')] == float('inf')

        two_layer_spl = mn.all_pairs_k_layer_shortest_path_length(dmg, -1)
        assert len(two_layer_spl) == 20
        assert two_layer_spl[('A', 'B')] == 1
        assert two_layer_spl[('A', 'D')] == 2
        assert two_layer_spl[('A', 'E')] == float('inf')


    def test_k_layer_reachability(self):
        assert mn.k_layer_reachability(mg, 3) == 1
        assert mn.k_layer_reachability(mg, 1) == 0.7
        assert mn.k_layer_reachability(mg, -1) == 1

        assert mn.k_layer_reachability(dmg, 3) == 1
        assert mn.k_layer_reachability(dmg, 1) == 0.35
        assert mn.k_layer_reachability(dmg, -1) == 0.9


    def test_harmonic_mean_shortest_path(self):
        result = mn.harmonic_mean_shortest_path_length(mg)
        assert result[('A', 'B')] == 1
        assert result[('A', 'D')] == 2

        result = mn.harmonic_mean_shortest_path_length(dmg)
        assert result[('A', 'B')] == 1
        assert result[('D', 'A')] == 2
        assert ('A', 'D') not in result