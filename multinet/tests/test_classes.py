"""
Test the Multinet Class.
"""
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
        mg.add_edge(0, 1, 'L2')
        mg.add_edge(1, 0, 'L2')
        mg.add_edge(1, 2, 'L2')

        assert 'L1' in mg.layers()
        assert 'L2' in mg.layers()

        assert len(mg.edgelets) == 3

        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2
        assert mg.number_of_edgelets() == 3

        # Remove non-existed edge.
        mg.remove_edgelet(2, 3, 'L3')

        mg.remove_edgelet(0, 1, 'L2')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2
        assert mg.number_of_edgelets() == 2

        mg.remove_edgelet(0, 1, 'L1')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 1
        assert mg.number_of_layers() == 2
        assert mg.number_of_edgelets() == 1

        assert len(mg.empty_layers()) == 1

        mg.remove_empty_layers()

        assert mg.number_of_layers() == 1


    def test_aggregate_edge(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        assert mg[0][1][mg.cid]['L1'] == 5
        assert mg[1][2][mg.cid]['L2'] == 6

        mg.add_edge(0, 1, 'L1', weight=10)
        assert mg[0][1][mg.cid]['L1'] == 10

        mg.aggregate_edge(0, 1, 'L1', weight=5)
        assert mg[0][1][mg.cid]['L1'] == 15

        mg.aggregate_edge(2, 3, 'L2', weight=7)
        assert mg[2][3][mg.cid]['L2'] == 7


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

        assert mg[0][1][mg.cid]['L1_L2'] == 5
        assert mg[1][2][mg.cid]['L1_L2'] == 6

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

        assert mg[0][1][mg.cid]['L1'] == 5
        assert mg[1][2][mg.cid]['LN'] == 8


    def test_add_layer(self):
        mg = mn.Multinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        sg = nx.Graph()
        sg.add_edge(1, 2, weight=7)
        sg.add_edge(2, 3)

        mg.add_layer(sg, 'L3')
        assert mg.number_of_nodes() == 4
        assert mg.number_of_edges() == 3
        assert mg.number_of_layers() == 3

        assert mg[1][2][mg.cid]['L2'] == 6
        assert mg[1][2][mg.cid]['L3'] == 7
        assert mg[2][3][mg.cid]['L3'] == 1


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
        mg.add_edge(0, 1, 'L2')
        mg.add_edge(1, 0, 'L2')
        mg.add_edge(1, 2, 'L2')

        assert 'L1' in mg.layers()
        assert 'L2' in mg.layers()

        assert len(mg.edgelets) == 4

        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 3
        assert mg.number_of_layers() == 2
        assert mg.number_of_edgelets() == 4

        # Remove non-existed edge.
        mg.remove_edgelet(2, 3, 'L3')

        mg.remove_edgelet(0, 1, 'L2')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 3
        assert mg.number_of_layers() == 2
        assert mg.number_of_edgelets() == 3

        mg.remove_edgelet(0, 1, 'L1')
        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 2
        assert mg.number_of_layers() == 2
        assert mg.number_of_edgelets() == 2

        assert len(mg.empty_layers()) == 1

        mg.remove_empty_layers()

        assert mg.number_of_layers() == 1


    def test_aggregate_edge(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        assert mg[0][1][mg.cid]['L1'] == 5
        assert mg[1][2][mg.cid]['L2'] == 6

        mg.add_edge(0, 1, 'L1', weight=10)
        assert mg[0][1][mg.cid]['L1'] == 10

        mg.aggregate_edge(0, 1, 'L1', weight=5)
        assert mg[0][1][mg.cid]['L1'] == 15

        mg.aggregate_edge(2, 3, 'L2', weight=7)
        assert mg[2][3][mg.cid]['L2'] == 7


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

        assert mg[0][1][mg.cid]['L1_L2'] == 5
        assert mg[1][2][mg.cid]['L1_L2'] == 6

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

        assert mg[0][1][mg.cid]['L1'] == 5
        assert mg[1][2][mg.cid]['LN'] == 8


    def test_add_layer(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)

        sg = nx.Graph()
        sg.add_edge(1, 2, weight=7)
        sg.add_edge(2, 3)

        mg.add_layer(sg, 'L3')
        assert mg.number_of_nodes() == 4
        assert mg.number_of_edges() == 3
        assert mg.number_of_layers() == 3

        assert mg[1][2][mg.cid]['L2'] == 6
        assert mg[1][2][mg.cid]['L3'] == 7
        assert mg[2][3][mg.cid]['L3'] == 1


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


    def test_to_undirected(self):
        mg = mn.DiMultinet()

        mg.add_edge(0, 1, 'L1', weight=5)
        mg.add_edge(1, 2, 'L2', weight=6)
        mg.add_edge(2, 1, 'L3', weight=2)

        assert mg.number_of_nodes() == 3
        assert mg.number_of_edges() == 3
        assert mg.number_of_layers() == 3

        nmg = mg.to_undirected()
        assert nmg.number_of_nodes() == 3
        assert nmg.number_of_edges() == 2
        assert nmg.number_of_layers() == 3
