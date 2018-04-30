"""
Test the Multinet Class.
"""
import pytest
import multinet as mn
import networkx as nx


class TestMultinet(object):


    def test_build_multinet(self):
        """
        Test building Multinet objects.
        """
        mg = mn.Multinet()

        assert mg.is_directed() == False

        mg.add_edge(0, 1, 'L1')
        mg.add_edge(1, 2, 'L2')

        assert 'L1' in mg.layers()
        assert 'L2' in mg.layers()

        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2

        mg.remove_edge(0,1)
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 1
        assert mg.number_of_layers() == 2

        assert len(mg.empty_layers()) == 1

        mg.remove_empty_layers()

        assert mg.number_of_layers() == 1


    def test_aggregate_edge(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        assert mg[0][1]['multiplex']['L1'] == 5
        assert mg[1][2]['multiplex']['L2'] == 6

        mg.add_edge(0, 1, 'L1', weight=10)
        assert mg[0][1]['multiplex']['L1'] == 10

        mg.aggregate_edge(0, 1, 'L1', weight=5)
        assert mg[0][1]['multiplex']['L1'] == 15

        mg.aggregate_edge(2, 3, 'L2', weight=7)
        assert mg[2][3]['multiplex']['L2'] == 7


    def test_sub_layer(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        sg = mg.sub_layer('L1')
        assert type(sg) == nx.Graph
        assert sg.number_of_nodes() == 3
        assert sg.number_of_edges() == 1

        sg = mg.sub_layer('L2', remove_isolates=True)
        assert type(sg) == nx.Graph
        assert sg.number_of_nodes() == 2
        assert sg.number_of_edges() == 1


    def test_sub_layers(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        sg = mg.sub_layers(['L1', 'L2'])
        assert type(sg) == mn.Multinet
        assert sg.number_of_nodes() == 3
        assert sg.number_of_edges() == 2
        assert sg.number_of_layers() == 2

        sg = mg.sub_layers(['L2', 'L3'], remove_isolates=True)
        assert type(sg) == mn.Multinet
        assert sg.number_of_nodes() == 2
        assert sg.number_of_edges() == 1
        assert sg.number_of_layers() == 2


    def test_aggregated(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        ag = mg.aggregated()
        assert type(ag) == nx.Graph
        assert ag.number_of_nodes() == 3
        assert ag.number_of_edges() == 2

        assert ag[1][2]['weight'] == 8
        assert ag[1][2]['nlayer'] == 2


    def test_merge_layers(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.merge_layers(['L1', 'L2'])
        assert 'L1' not in mg.layers()
        assert 'L2' not in mg.layers()
        assert 'L1_L2' in mg.layers()
        assert mg.number_of_layers() == 2
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2

        assert mg[0][1]['multiplex']['L1_L2'] == 5
        assert mg[1][2]['multiplex']['L1_L2'] == 6

        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.merge_layers(['L2', 'L3'], new_name='LN')
        assert 'L2' not in mg.layers()
        assert 'L3' not in mg.layers()
        assert 'LN' in mg.layers()
        assert mg.number_of_layers() == 2
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2

        assert mg[0][1]['multiplex']['L1'] == 5
        assert mg[1][2]['multiplex']['LN'] == 8


    def test_add_layer(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        sg = nx.Graph()
        sg.add_edge(1, 2, weight=7)

        mg.add_layer(sg, 'L3')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 3

        assert mg[1][2]['multiplex']['L2'] == 6
        assert mg[1][2]['multiplex']['L3'] == 7


    def test_remove_layer(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.remove_layer('L3')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2

        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.remove_layer('L1')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 1
        assert mg.number_of_layers() == 2


class TestDiMultinet(object):


    def test_build_dimultinet(self):
        """
        Test building Multinet objects.
        """
        mg = mn.DiMultinet()

        assert mg.is_directed() == True

        mg.add_edge(0, 1, 'L1')
        mg.add_edge(1, 2, 'L2')

        assert 'L1' in mg.layers()
        assert 'L2' in mg.layers()

        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2

        mg.remove_edge(0,1)
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 1
        assert mg.number_of_layers() == 2

        assert len(mg.empty_layers()) == 1

        mg.remove_empty_layers()

        assert mg.number_of_layers() == 1


    def test_aggregate_edge(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        assert mg[0][1]['multiplex']['L1'] == 5
        assert mg[1][2]['multiplex']['L2'] == 6

        mg.add_edge(0, 1, 'L1', weight=10)
        assert mg[0][1]['multiplex']['L1'] == 10

        mg.aggregate_edge(0, 1, 'L1', weight=5)
        assert mg[0][1]['multiplex']['L1'] == 15

        mg.aggregate_edge(2, 3, 'L2', weight=7)
        assert mg[2][3]['multiplex']['L2'] == 7


    def test_sub_layer(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        sg = mg.sub_layer('L1')
        assert type(sg) == nx.DiGraph
        assert sg.number_of_nodes() == 3
        assert sg.number_of_edges() == 1

        sg = mg.sub_layer('L2', remove_isolates=True)
        assert type(sg) == nx.DiGraph
        assert sg.number_of_nodes() == 2
        assert sg.number_of_edges() == 1


    def test_sub_layers(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        sg = mg.sub_layers(['L1', 'L2'])
        assert type(sg) == mn.DiMultinet
        assert sg.number_of_nodes() == 3
        assert sg.number_of_edges() == 2
        assert sg.number_of_layers() == 2

        sg = mg.sub_layers(['L2', 'L3'], remove_isolates=True)
        assert type(sg) == mn.DiMultinet
        assert sg.number_of_nodes() == 2
        assert sg.number_of_edges() == 1
        assert sg.number_of_layers() == 2


    def test_aggregated(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        ag = mg.aggregated()
        assert type(ag) == nx.DiGraph
        assert ag.number_of_nodes() == 3
        assert ag.number_of_edges() == 2

        assert ag[1][2]['weight'] == 8
        assert ag[1][2]['nlayer'] == 2


    def test_merge_layers(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.merge_layers(['L1', 'L2'])
        assert 'L1' not in mg.layers()
        assert 'L2' not in mg.layers()
        assert 'L1_L2' in mg.layers()
        assert mg.number_of_layers() == 2
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2

        assert mg[0][1]['multiplex']['L1_L2'] == 5
        assert mg[1][2]['multiplex']['L1_L2'] == 6

        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.merge_layers(['L2', 'L3'], new_name='LN')
        assert 'L2' not in mg.layers()
        assert 'L3' not in mg.layers()
        assert 'LN' in mg.layers()
        assert mg.number_of_layers() == 2
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2

        assert mg[0][1]['multiplex']['L1'] == 5
        assert mg[1][2]['multiplex']['LN'] == 8


    def test_add_layer(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        sg = nx.DiGraph()
        sg.add_edge(1, 2, weight=7)

        mg.add_layer(sg, 'L3')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 3

        assert mg[1][2]['multiplex']['L2'] == 6
        assert mg[1][2]['multiplex']['L3'] == 7


    def test_remove_layer(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.remove_layer('L3')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2

        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(1, 2, 'L3', weight=2)

        mg.remove_layer('L1')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 1
        assert mg.number_of_layers() == 2
