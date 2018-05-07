import multinet as mn
import networkx as nx

g1 = nx.Graph()
dg1 = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')]
g1.add_nodes_from(nodes)
g1.add_edges_from(edges)
dg1.add_nodes_from(nodes)
dg1.add_edges_from(edges)

g2 = nx.Graph()
dg2 = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'A'), ('E', 'B')]
g2.add_nodes_from(nodes)
g2.add_edges_from(edges)
dg2.add_nodes_from(nodes)
dg2.add_edges_from(edges)

g3 = nx.Graph()
dg3 = nx.DiGraph()
nodes = ['A', 'B', 'C', 'D', 'E']
edges = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('A', 'E'), ('B', 'D'), ('C', 'E')]
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


class TestExtractCount(object):


    def test_extract_count(self):
        count = mn.extract_count(mg, ['1', '2'])
        assert len(count) == 4
        assert count['00'] == 0
        assert count['01'] == 5
        assert count['10'] == 5
        assert count['11'] == 0

        count = mn.extract_count(mg, ['1', '2'], False)
        assert len(count) == 4
        assert count['00'] == 5
        assert count['01'] == 5
        assert count['10'] == 5
        assert count['11'] == 0

        count = mn.extract_count(dmg, ['1', '2'])
        assert len(count) == 4
        assert count['00'] == 10
        assert count['01'] == 5
        assert count['10'] == 5
        assert count['11'] == 0

        count = mn.extract_count(dmg, ['1', '2'], False)
        assert len(count) == 4
        assert count['00'] == 15
        assert count['01'] == 5
        assert count['10'] == 5
        assert count['11'] == 0


class TestMutualInformation(object):


    def test_mutual_infomation(self):
        assert mn.mutual_information(mg, ['1', '2']) == 1


class TestTransferEntropy(object):
    pass
