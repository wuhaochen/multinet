import networkx as nx

class Multinet(nx.DiGraph):
    '''
    Multiplex network class.
    '''
    
    def __init__(self):
        super(self.__class__,self).__init__()
        self.graph['layers'] = []

    def _add_layer(self,layer):
        if layer not in self.layers():
            self.graph['layers'].append(layer)
        
    def layers(self):
        return self.graph['layers']

    def add_edge(self, u, v, layer, weight=1.0):
        super(self.__class__,self).add_edge(u,v)

        self._add_layer(layer)
            
        if not self[u][v].has_key('multiplex'):
            self[u][v]['multiplex'] = {}
        self[u][v]['multiplex'][layer] = weight
