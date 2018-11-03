import random

import multinet as mn
import networkx as nx

nlayers = 5
nnodes = 20

mg = mn.Multinet()
for layer in range(nlayers):
    p = random.uniform(0.3,0.6)
    layer_name = '%d' % layer
    g = nx.erdos_renyi_graph(nnodes, p)
    mg.add_layer(g, layer_name)

dmg = mn.DiMultinet()
for layer in range(nlayers):
    p = random.uniform(0.3,0.6)
    layer_name = '%d' % layer
    g = nx.erdos_renyi_graph(nnodes, p)
    mg.add_layer(g, layer_name)


class TestErdosRenyi(object):


    def test_undirected(self):
        seed = 42

        rmg = mn.multiplex_erdos_renyi(mg, seed=seed)
        rmg = mn.multiplex_erdos_renyi(mg)


    def test_directed(self):
        seed = 42

        rmg = mn.multiplex_erdos_renyi(dmg, seed=seed)
        rmg = mn.multiplex_erdos_renyi(dmg)


class TestIndependentConfig(object):


    def test_undirected(self):
        seed = 42
        rmg = mn.multiplex_configuration_independent(mg, seed=seed)
        rmg = mn.multiplex_configuration_independent(mg)


    def test_directed(self):
        seed = 42
        rmg = mn.multiplex_configuration_independent(dmg, seed=seed)
        rmg = mn.multiplex_configuration_independent(dmg)
