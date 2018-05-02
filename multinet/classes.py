"""Multiplex network class.

"""

import networkx as nx


class Multinet(nx.Graph):
    """
    Undirected Multiplex network class.
    """
    
    def __init__(self):
        """Initialize a Multinet with empty layer list.

        """
        super(self.__class__,self).__init__()
        self.graph['layers'] = []


    def _add_layer(self,layer):
        """Add one layer to the layer list.

        Parameters:
        -----------
        layer: str
          layer to be added to the layer list.

        """
        if layer not in self.layers():
            self.graph['layers'].append(layer)


    def _remove_layer(self,layer):
        """Remove one layer from the layer list.

        Parameters:
        -----------
        layer: str
          layer to be removed from the layer list.

        """
        self.graph['layers'].remove(layer)


    def layers(self):
        """Return all the layers in the Multinet.

        """
        return self.graph['layers']


    def number_of_layers(self):
        """Return number of layers in the Multinet.

        """
        return len(self.graph['layers'])


    def _init_edge(self, u, v, layer):
        """Initialize one edge in the Multinet for one layer.
        Used by add_edge() and aggregate_edge().

        Parameters:
        -----------
        u, v:
          Nodes the edge connects.

        layer:
          Layer the edge sit on.
        
        """
        super(self.__class__,self).add_edge(u,v)

        self._add_layer(layer)
            
        if 'multiplex' not in self[u][v]:
            self[u][v]['multiplex'] = {}
        if layer not in self[u][v]['multiplex']:
            self[u][v]['multiplex'][layer] = 0.0


    def add_edge(self, u, v, layer, weight=1.0):
        """Add an edge to the Multinet.

        If the edge already exist, set the weight to the new one.

        Parameters:
        -----------
        u, v:
          Nodes the edge connects.

        layer:
          Layer the edge sit on.
        
        weight: float (default 1.0)
          The weight of the edge.
        
        """
        self._init_edge(u, v, layer)
        self[u][v]['multiplex'][layer] = weight


    def aggregate_edge(self, u, v, layer, weight):
        """Aggregate an edge to the Multinet.

        If the edge already exist, add the weight to the existing one.

        Parameters:
        -----------
        u, v:
          Nodes the edge connects.

        layer:
          Layer the edge sit on.
        
        weight: float (default 1.0)
          The weight of the edge.
        
        """

        self._init_edge(u, v, layer)
        self[u][v]['multiplex'][layer] += weight


    def sub_layers(self, layers, remove_isolates=False):
        """Return a new Multinet instance that only contains layers specified.

        Parameters:
        -----------
        layers: container
          The list of layers that is to be remained.
          The layers that is not in the original multiplex network will be ignored.

        remove_isolates: bool (default False)
          Remove the isolated nodes in the new multiplex network.
        
        """
        layers = set(layers) & set(self.layers())

        import copy
        g = copy.deepcopy(self)
        to_remove = []
        for u,v in g.edges():
            new_weight = {}
            for layer in layers:
                if layer in g[u][v]['multiplex']:
                    new_weight[layer] = g[u][v]['multiplex'][layer]
            if len(new_weight) == 0:
                to_remove.append((u, v))
            else:
                g[u][v]['multiplex'] = new_weight
        g.remove_edges_from(to_remove)
        g.graph['layers'] = list(layers)

        if remove_isolates:
            g.remove_nodes_from(list(nx.isolates(g)))

        return g


    def sub_layer(self, layer, remove_isolates=False):
        """Return a new DiGraph instance that only contains one layer.

        Parameters:
        -----------
        layer: str
          The layer intended to be extract.

        remove_isolates: bool (default False)
          Remove the isolated nodes in the new graph.
        
        """
        if layer not in self.layers():
            raise Exception('layer does not exist.')
        
        g = nx.Graph()
        g.add_nodes_from(self)
        for u,v in self.edges():
            edge = self[u][v]
            if layer in edge['multiplex']:
                weight = edge['multiplex'][layer]
                g.add_edge(u,v,weight=weight)
        if remove_isolates:
            g.remove_nodes_from(list(nx.isolates(g)))
        return g


    def aggregated(self):
        """Return a new DiGraph instance that represents the aggregated network.
        """
        g = nx.Graph()
        g.add_nodes_from(self)
        for u,v in self.edges():
            g.add_edge(u,v)
            g[u][v]['weight'] = sum(self[u][v]['multiplex'].values())
            g[u][v]['nlayer'] = len(self[u][v]['multiplex'])
        return g
        
        
    def merge_layers(self, layers, new_name=None):
        """Merge layers together with new name.

        Parameters:
        -----------
        layers:
          The layers to be merged.

        new_name: str or None
          The name of the merged layer. If remains None, the new name will be the merged layers joined with underline.
        
        """
        if not new_name:
            new_name = '_'.join(layers)
            
        for layer in layers:
            self._remove_layer(layer)

        self._add_layer(new_name)

        for u,v in self.edges():
            new_weight = 0.0
            for layer in layers:
                if layer in self[u][v]['multiplex']:
                    new_weight += self[u][v]['multiplex'].pop(layer)
            if new_weight != 0:
                self[u][v]['multiplex'][new_name] = new_weight


    def add_layer(self, layer_graph, layer_name):
        """Add a new layer from a DiGraph.
        The existing edge will be replaced by the new one.

        Parameters:
        -----------
        layer_graph: nx.DiGraph
          The layers to be added.

        layer_name: str
          The name of the new layer.
        
        
        """
        self.add_nodes_from(layer_graph)
        self._add_layer(layer_name)

        for u, v in layer_graph.edges():
            if 'weight' in layer_graph[u][v]:
                weight = layer_graph[u][v]['weight']
            else:
                weight = 1.0
            self.add_edge(u,v,layer_name,weight)


    def empty_layers(self):
        """Return a list of all empty layers.
        
        """
        layers = set(self.layers())
        nonempty = set()

        for u,v in self.edges():
            for layer in self[u][v]['multiplex']:
                nonempty.add(layer)

        return list(layers-nonempty)


    def remove_empty_layers(self):
        """Remove all empty layers.

        """
        to_remove = self.empty_layers()
        for layer in to_remove:
            self._remove_layer(layer)


    def remove_layer(self, layer):
        """Remove one specific layer.

        """
        edges_to_remove = list()
        
        for u,v in self.edges():
            if layer in self[u][v]['multiplex']:
                self[u][v]['multiplex'].pop(layer)
            if len(self[u][v]['multiplex']) == 0:
                edges_to_remove.append((u, v))

        self.remove_edges_from(edges_to_remove)

        self._remove_layer(layer)


class DiMultinet(nx.DiGraph):
    """
    Directed Multiplex network class.
    TODO: Use multiple inheritance to reuse code from Multinet.
    """
    
    def __init__(self):
        """Initialize a Multinet with empty layer list.

        """
        super(self.__class__,self).__init__()
        self.graph['layers'] = []


    def _add_layer(self,layer):
        """Add one layer to the layer list.

        Parameters:
        -----------
        layer: str
          layer to be added to the layer list.

        """
        if layer not in self.layers():
            self.graph['layers'].append(layer)


    def _remove_layer(self,layer):
        """Remove one layer from the layer list.

        Parameters:
        -----------
        layer: str
          layer to be removed from the layer list.

        """
        self.graph['layers'].remove(layer)
        

    def layers(self):
        """Return all the layers in the DiMultinet.

        """
        return self.graph['layers']


    def number_of_layers(self):
        """Return number of layers in the DiMultinet.

        """
        return len(self.graph['layers'])
        

    def _init_edge(self, u, v, layer):
        """Initialize one edge in the Multinet for one layer.
        Used by add_edge() and aggregate_edge().

        Parameters:
        -----------
        u, v:
          Nodes the edge connects.

        layer:
          Layer the edge sit on.
        
        """
        super(self.__class__,self).add_edge(u,v)

        self._add_layer(layer)
            
        if 'multiplex' not in self[u][v]:
            self[u][v]['multiplex'] = {}
        if layer not in self[u][v]['multiplex']:
            self[u][v]['multiplex'][layer] = 0.0


    def add_edge(self, u, v, layer, weight=1.0):
        """Add an edge to the DiMultinet.

        If the edge already exist, set the weight to the new one.

        Parameters:
        -----------
        u, v:
          Nodes the edge connects.

        layer:
          Layer the edge sit on.
        
        weight: float (default 1.0)
          The weight of the edge.
        
        """
        self._init_edge(u, v, layer)
        self[u][v]['multiplex'][layer] = weight


    def aggregate_edge(self, u, v, layer, weight):
        """Aggregate an edge to the DiMultinet.
        
        If the edge already exist, add the weight to the existing one.

        Parameters:
        -----------
        u, v:
          Nodes the edge connects.

        layer:
          Layer the edge sit on.
        
        weight: float (default 1.0)
          The weight of the edge.
        
        """

        self._init_edge(u, v, layer)
        self[u][v]['multiplex'][layer] += weight


    def sub_layers(self, layers, remove_isolates=False):
        """Return a new DiMultinet instance that only contains layers specified.

        Parameters:
        -----------
        layers: container
          The list of layers that is to be remained.
          The layers that is not in the original multiplex network will be ignored.

        remove_isolates: bool (default False)
          Remove the isolated nodes in the new multiplex network.
        
        """
        layers = set(layers)&set(self.layers())

        import copy
        g = copy.deepcopy(self)
        to_remove = []
        for u,v in g.edges():
            new_weight = {}
            for layer in layers:
                if layer in g[u][v]['multiplex']:
                    new_weight[layer] = g[u][v]['multiplex'][layer]
            if len(new_weight) == 0:
                to_remove.append((u,v))
            else:
                g[u][v]['multiplex'] = new_weight
        g.remove_edges_from(to_remove)
        g.graph['layers'] = list(layers)

        if remove_isolates:
            g.remove_nodes_from(list(nx.isolates(g)))

        return g


    def sub_layer(self, layer, remove_isolates=False):
        """Return a new DiGraph instance that only contains one layer.

        Parameters:
        -----------
        layer: str
          The layer intended to be extract.

        remove_isolates: bool (default False)
          Remove the isolated nodes in the new graph.
        
        """
        if layer not in self.layers():
            raise Exception('layer does not exist.')
        
        g = nx.DiGraph()
        g.add_nodes_from(self)
        for u,v in self.edges():
            edge = self[u][v]
            if layer in edge['multiplex']:
                weight = edge['multiplex'][layer]
                g.add_edge(u,v,weight=weight)
        if remove_isolates:
            g.remove_nodes_from(list(nx.isolates(g)))
        return g


    def aggregated(self):
        """Return a new DiGraph instance that represents the aggregated network.
        """
        g = nx.DiGraph()
        g.add_nodes_from(self)
        for u,v in self.edges():
            g.add_edge(u,v)
            g[u][v]['weight'] = sum(self[u][v]['multiplex'].values())
            g[u][v]['nlayer'] = len(self[u][v]['multiplex'])
        return g
        
        
    def merge_layers(self, layers, new_name=None):
        """Merge layers together with new name.

        Parameters:
        -----------
        layers:
          The layers to be merged.

        new_name: str or None
          The name of the merged layer. If remains None, the new name will be the merged layers joined with underline.
        
        """
        if not new_name:
            new_name = '_'.join(layers)
            
        for layer in layers:
            self._remove_layer(layer)

        self._add_layer(new_name)

        for u,v in self.edges():
            new_weight = 0.0
            for layer in layers:
                if layer in self[u][v]['multiplex']:
                    new_weight += self[u][v]['multiplex'].pop(layer)
            if new_weight != 0:
                self[u][v]['multiplex'][new_name] = new_weight


    def add_layer(self,layer_graph,layer_name):
        """Add a new layer from a DiGraph.
        The existing edge will be replaced by the new one.

        Parameters:
        -----------
        layer_graph: nx.DiGraph
          The layers to be added.

        layer_name: str
          The name of the new layer.
        
        
        """
        self.add_nodes_from(layer_graph)
        self._add_layer(layer_name)

        for u,v in layer_graph.edges():
            if 'weight' in layer_graph[u][v]:
                weight = layer_graph[u][v]['weight']
            else:
                weight = 1.0
            self.add_edge(u,v,layer_name,weight)


    def empty_layers(self):
        """Return a list of all empty layers.
        
        """
        layers = set(self.layers())
        nonempty = set()

        for u,v in self.edges():
            for layer in self[u][v]['multiplex']:
                nonempty.add(layer)

        return list(layers-nonempty)


    def remove_empty_layers(self):
        """Remove all empty layers.

        """
        to_remove = self.empty_layers()
        for layer in to_remove:
            self._remove_layer(layer)


    def remove_layer(self, layer):
        """Remove one specific layer.

        """
        edges_to_remove = list()
        
        for u,v in self.edges():
            if layer in self[u][v]['multiplex']:
                self[u][v]['multiplex'].pop(layer)
            if len(self[u][v]['multiplex']) == 0:
                edges_to_remove.append((u, v))

        self.remove_edges_from(edges_to_remove)

        self._remove_layer(layer)


    def to_undirected(self):
        """ Transform DiMultinet to Multinet.
        """
        import copy
        g = Multinet()
        g.add_nodes_from(self.nodes())
        g.graph['layers'] = self.layers()
        for u,v in self.edges():
            for layer in self[u][v]['multiplex']:
                g.aggregate_edge(u,v,layer,self[u][v]['multiplex'][layer])
        return g
